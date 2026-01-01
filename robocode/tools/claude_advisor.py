#!/usr/bin/env python3
"""
Claude Advisor - LLM-driven strategy improvement for Robocode bots

Analyzes battle performance and uses Claude to propose strategic improvements:
- Identifies weaknesses from battle statistics
- Proposes module changes or parameter tweaks
- Can invent new module variants
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).parent.parent

# Import sibling modules
sys.path.insert(0, str(Path(__file__).parent))
from battle_runner import run_battle, run_1v1
from bot_generator import MOVEMENT_MODULES, GUN_MODULES, RADAR_MODULES

# Files
POPULATION_FILE = PROJECT_ROOT / "data" / "population.json"
ADVICE_LOG = PROJECT_ROOT / "data" / "advisor_log.json"


def load_population() -> Dict:
    """Load current population"""
    with open(POPULATION_FILE) as f:
        return json.load(f)


def load_advice_log() -> List[Dict]:
    """Load previous advice"""
    if ADVICE_LOG.exists():
        with open(ADVICE_LOG) as f:
            return json.load(f)
    return []


def save_advice_log(log: List[Dict]):
    """Save advice log"""
    with open(ADVICE_LOG, 'w') as f:
        json.dump(log, f, indent=2)


def run_detailed_battle(bot_name: str, opponent: str, rounds: int = 10) -> Dict:
    """Run a detailed battle and return full statistics"""
    results, _ = run_battle([bot_name, opponent], rounds=rounds, save_results=False)

    if len(results) < 2:
        return {"error": "Battle failed"}

    # Find our bot and opponent in results
    bot_result = next((r for r in results if r['name'] == bot_name), None)
    opp_result = next((r for r in results if r['name'] == opponent), None)

    if not bot_result or not opp_result:
        return {"error": "Could not find results for bots"}

    return {
        "bot": bot_name,
        "opponent": opponent,
        "rounds": rounds,
        "won": bot_result['rank'] == 1,
        "bot_stats": bot_result,
        "opponent_stats": opp_result,
        "analysis": {
            "survival_ratio": bot_result['survival'] / max(opp_result['survival'], 1),
            "damage_ratio": bot_result['bullet_damage'] / max(opp_result['bullet_damage'], 1),
            "accuracy_index": bot_result['bullet_damage'] / max(bot_result['total_score'], 1),
            "ram_reliance": bot_result['ram_damage'] / max(bot_result['total_score'], 1),
            "firsts_ratio": bot_result['firsts'] / max(rounds, 1)
        }
    }


def analyze_bot_performance(bot: Dict, opponents: List[str] = None) -> Dict:
    """Run detailed battles and analyze performance patterns"""

    if opponents is None:
        opponents = ["sample.Walls", "sample.SpinBot", "sample.Fire", "sample.Corners"]

    bot_name = bot["name"]
    genome = bot["genome"]

    battles = []
    for opp in opponents:
        result = run_detailed_battle(bot_name, opp, rounds=5)
        if "error" not in result:
            battles.append(result)

    if not battles:
        return {"error": "All battles failed"}

    # Aggregate analysis
    wins = sum(1 for b in battles if b['won'])
    total = len(battles)

    avg_survival = sum(b['analysis']['survival_ratio'] for b in battles) / total
    avg_damage = sum(b['analysis']['damage_ratio'] for b in battles) / total
    avg_firsts = sum(b['analysis']['firsts_ratio'] for b in battles) / total

    # Identify problem areas
    problems = []

    if avg_survival < 0.8:
        problems.append("LOW_SURVIVAL: Bot dies too quickly. Consider better evasion.")

    if avg_damage < 0.7:
        problems.append("LOW_DAMAGE: Not hitting enemy enough. Consider better targeting.")

    if avg_firsts < 0.4:
        problems.append("LOW_WIN_RATE: Not finishing fights. May need combined improvements.")

    # Check for specific opponent struggles
    for battle in battles:
        if not battle['won']:
            opp = battle['opponent']
            if 'SpinBot' in opp:
                problems.append(f"LOSES_TO_SPINNER: Struggles against circular movement ({opp})")
            elif 'Walls' in opp:
                problems.append(f"LOSES_TO_WALL_HUGGER: Struggles against wall tactics ({opp})")

    return {
        "bot_id": bot["id"],
        "bot_name": bot_name,
        "genome": genome,
        "battles": battles,
        "summary": {
            "wins": wins,
            "total": total,
            "win_rate": wins / total if total > 0 else 0,
            "avg_survival_ratio": avg_survival,
            "avg_damage_ratio": avg_damage,
            "avg_firsts_ratio": avg_firsts
        },
        "problems": problems
    }


def build_advisor_prompt(analysis: Dict, population_context: List[Dict] = None) -> str:
    """Build a prompt for Claude to analyze and propose improvements"""

    genome = analysis["genome"]
    summary = analysis["summary"]
    problems = analysis["problems"]

    # Available modules (these are already lists)
    movement_options = MOVEMENT_MODULES
    gun_options = GUN_MODULES
    radar_options = RADAR_MODULES

    prompt = f"""You are a Robocode strategy advisor. Analyze this bot's performance and propose specific improvements.

## Current Bot Configuration

**ID**: {analysis['bot_id']}
**Elo**: {analysis.get('elo', 'Unknown')}

**Modules**:
- Movement: {genome['movement_module']}
- Gun: {genome['gun_module']}
- Radar: {genome['radar_module']}

**Key Parameters**:
- Preferred Distance: {genome['parameters'].get('PARAM_PREFERRED_DISTANCE', 200):.0f}
- Move Distance: {genome['parameters'].get('PARAM_MOVE_DISTANCE', 150):.0f}
- Fire Power Close/Med/Far: {genome['parameters'].get('PARAM_FIRE_POWER_CLOSE', 3):.1f}/{genome['parameters'].get('PARAM_FIRE_POWER_MEDIUM', 2):.1f}/{genome['parameters'].get('PARAM_FIRE_POWER_FAR', 1):.1f}

## Performance Analysis

**Win Rate**: {summary['win_rate']:.0%} ({summary['wins']}/{summary['total']})
**Survival Ratio**: {summary['avg_survival_ratio']:.2f} (>1 = outlives enemy)
**Damage Ratio**: {summary['avg_damage_ratio']:.2f} (>1 = deals more damage)

## Identified Problems

{chr(10).join('- ' + p for p in problems) if problems else '- No major problems identified'}

## Battle Details

"""

    for battle in analysis.get('battles', []):
        result = "WON" if battle['won'] else "LOST"
        opp = battle['opponent'].split('.')[-1]
        prompt += f"vs {opp}: {result} (survival: {battle['analysis']['survival_ratio']:.2f}, damage: {battle['analysis']['damage_ratio']:.2f})\n"

    prompt += f"""

## Available Options

**Movement Modules**: {', '.join(movement_options)}
**Gun Modules**: {', '.join(gun_options)}
**Radar Modules**: {', '.join(radar_options)}

## Your Task

Based on this analysis, propose ONE specific improvement. Choose from:

1. **Module Change**: Switch to a different movement, gun, or radar module
2. **Parameter Adjustment**: Modify specific parameters (with exact values)
3. **Strategy Insight**: Explain why current approach fails against certain enemies

Respond in this JSON format:
```json
{{
  "recommendation_type": "module_change" | "parameter_adjustment" | "strategy_insight",
  "confidence": 0.0-1.0,
  "summary": "One sentence summary",
  "changes": {{
    "movement_module": "Optional: new module name",
    "gun_module": "Optional: new module name",
    "radar_module": "Optional: new module name",
    "parameters": {{
      "PARAM_NAME": new_value
    }}
  }},
  "reasoning": "Detailed explanation of why this should help"
}}
```

Focus on the most impactful single change. Be specific and actionable.
"""

    return prompt


def get_claude_advice(prompt: str) -> Optional[Dict]:
    """Call Claude CLI to get strategic advice"""
    import re

    try:
        # Use claude CLI with print flag for text output
        result = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "text"],
            capture_output=True,
            text=True,
            timeout=180  # 3 min timeout
        )

        if result.returncode != 0:
            print(f"Claude CLI error: {result.stderr}")
            return None

        output = result.stdout

        if not output.strip():
            print("Claude returned empty response")
            return None

        # Try to extract JSON from markdown code block
        json_match = re.search(r'```json\s*(.*?)\s*```', output, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON from code block: {e}")

        # Try to find bare JSON object
        json_match = re.search(r'\{[^{}]*"recommendation_type"[^{}]*\}', output, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass

        # Try a more permissive JSON extraction
        brace_start = output.find('{')
        if brace_start >= 0:
            # Find matching closing brace
            depth = 0
            for i, c in enumerate(output[brace_start:], brace_start):
                if c == '{':
                    depth += 1
                elif c == '}':
                    depth -= 1
                    if depth == 0:
                        try:
                            return json.loads(output[brace_start:i+1])
                        except json.JSONDecodeError:
                            pass
                        break

        print(f"Could not parse Claude response. First 500 chars: {output[:500]}")
        return None

    except subprocess.TimeoutExpired:
        print("Claude CLI timeout")
        return None
    except Exception as e:
        print(f"Error calling Claude: {e}")
        return None


def advise_bot(bot: Dict, opponents: List[str] = None) -> Optional[Dict]:
    """Full advisory cycle for a single bot"""

    print(f"\n=== Analyzing {bot['id']} ===")

    # Run performance analysis
    analysis = analyze_bot_performance(bot, opponents)

    if "error" in analysis:
        print(f"Analysis failed: {analysis['error']}")
        return None

    print(f"Performance: {analysis['summary']['win_rate']:.0%} win rate")
    print(f"Problems: {len(analysis['problems'])} identified")

    # Build prompt and get advice
    prompt = build_advisor_prompt(analysis)
    print("Consulting Claude for strategic advice...")

    advice = get_claude_advice(prompt)

    if advice:
        print(f"Recommendation: {advice.get('summary', 'No summary')}")
        print(f"Confidence: {advice.get('confidence', 0):.0%}")

        # Log the advice
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "bot_id": bot["id"],
            "analysis_summary": analysis["summary"],
            "problems": analysis["problems"],
            "advice": advice
        }

        log = load_advice_log()
        log.append(log_entry)
        save_advice_log(log)

        return {
            "bot": bot,
            "analysis": analysis,
            "advice": advice
        }

    return None


def apply_advice(bot: Dict, advice: Dict) -> Dict:
    """Apply Claude's advice to create an improved genome"""

    import copy
    genome = copy.deepcopy(bot["genome"])
    changes = advice.get("changes", {})

    # Apply module changes (MOVEMENT_MODULES etc are lists)
    if "movement_module" in changes and changes["movement_module"]:
        new_module = changes["movement_module"]
        if new_module in MOVEMENT_MODULES:
            genome["movement_module"] = new_module

    if "gun_module" in changes and changes["gun_module"]:
        new_module = changes["gun_module"]
        if new_module in GUN_MODULES:
            genome["gun_module"] = new_module

    if "radar_module" in changes and changes["radar_module"]:
        new_module = changes["radar_module"]
        if new_module in RADAR_MODULES:
            genome["radar_module"] = new_module

    # Apply parameter changes
    if "parameters" in changes:
        for param, value in changes["parameters"].items():
            if param in genome["parameters"]:
                genome["parameters"][param] = float(value)

    return genome


def advise_population(top_n: int = 3) -> List[Dict]:
    """Advise the top N bots in the population"""

    pop_data = load_population()
    bots = pop_data.get("bots", [])

    if not bots:
        print("No bots in population")
        return []

    # Sort by Elo
    bots.sort(key=lambda b: b["stats"].get("elo", 1500), reverse=True)

    results = []
    for bot in bots[:top_n]:
        result = advise_bot(bot)
        if result:
            results.append(result)

    return results


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python claude_advisor.py analyze <bot_id>  - Analyze a specific bot")
        print("  python claude_advisor.py advise <bot_id>   - Get advice for a bot")
        print("  python claude_advisor.py top [n]           - Advise top N bots")
        print("  python claude_advisor.py log               - Show advice log")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == 'analyze':
        if len(sys.argv) < 3:
            print("Usage: python claude_advisor.py analyze <bot_id>")
            sys.exit(1)

        bot_id = sys.argv[2]
        pop_data = load_population()
        bot = next((b for b in pop_data["bots"] if b["id"] == bot_id), None)

        if not bot:
            print(f"Bot not found: {bot_id}")
            sys.exit(1)

        analysis = analyze_bot_performance(bot)
        print(json.dumps(analysis, indent=2))

    elif cmd == 'advise':
        if len(sys.argv) < 3:
            print("Usage: python claude_advisor.py advise <bot_id>")
            sys.exit(1)

        bot_id = sys.argv[2]
        pop_data = load_population()
        bot = next((b for b in pop_data["bots"] if b["id"] == bot_id), None)

        if not bot:
            print(f"Bot not found: {bot_id}")
            sys.exit(1)

        result = advise_bot(bot)
        if result:
            print("\n=== Full Result ===")
            print(json.dumps(result["advice"], indent=2))

    elif cmd == 'top':
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        results = advise_population(n)
        print(f"\nAdvised {len(results)} bots")

    elif cmd == 'log':
        log = load_advice_log()
        print(f"Advice log ({len(log)} entries):")
        for entry in log[-10:]:
            print(f"\n[{entry['timestamp'][:16]}] {entry['bot_id']}")
            if 'advice' in entry:
                print(f"  {entry['advice'].get('summary', 'No summary')}")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
