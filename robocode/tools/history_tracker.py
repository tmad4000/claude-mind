#!/usr/bin/env python3
"""
History Tracker - Archives bots and battles for later review

Saves:
- Battle results with full statistics
- Bot genomes by generation
- LLM advisor recommendations
- Evolution timeline
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

PROJECT_ROOT = Path(__file__).parent.parent

# Archive directories
ARCHIVE_DIR = PROJECT_ROOT / "data" / "history"
BATTLES_ARCHIVE = ARCHIVE_DIR / "battles"
BOTS_ARCHIVE = ARCHIVE_DIR / "bots"
TIMELINE_FILE = ARCHIVE_DIR / "timeline.json"


def ensure_dirs():
    """Create archive directories if they don't exist"""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    BATTLES_ARCHIVE.mkdir(exist_ok=True)
    BOTS_ARCHIVE.mkdir(exist_ok=True)


def load_timeline() -> List[Dict]:
    """Load evolution timeline"""
    if TIMELINE_FILE.exists():
        with open(TIMELINE_FILE) as f:
            return json.load(f)
    return []


def save_timeline(timeline: List[Dict]):
    """Save evolution timeline"""
    ensure_dirs()
    with open(TIMELINE_FILE, 'w') as f:
        json.dump(timeline, f, indent=2)


def archive_battle(
    bot1: str,
    bot2: str,
    result: Dict,
    generation: int,
    context: str = None
) -> str:
    """Archive a battle result with full details"""
    ensure_dirs()

    timestamp = datetime.now().isoformat()
    battle_id = f"battle_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

    battle_record = {
        "id": battle_id,
        "timestamp": timestamp,
        "generation": generation,
        "context": context,  # e.g., "evaluation", "tournament"
        "bot1": bot1,
        "bot2": bot2,
        "result": result
    }

    # Save individual battle
    battle_file = BATTLES_ARCHIVE / f"{battle_id}.json"
    with open(battle_file, 'w') as f:
        json.dump(battle_record, f, indent=2)

    # Add to timeline
    timeline = load_timeline()
    timeline.append({
        "type": "battle",
        "id": battle_id,
        "timestamp": timestamp,
        "generation": generation,
        "summary": f"{result.get('winner', 'Unknown')} beat {result.get('loser', 'Unknown')}"
    })
    save_timeline(timeline)

    return battle_id


def archive_bot(bot: Dict, generation: int) -> str:
    """Archive a bot's genome and source code"""
    ensure_dirs()

    bot_id = bot["id"]
    gen_dir = BOTS_ARCHIVE / f"gen{generation:03d}"
    gen_dir.mkdir(exist_ok=True)

    # Save genome
    genome_file = gen_dir / f"{bot_id}_genome.json"
    with open(genome_file, 'w') as f:
        json.dump({
            "id": bot_id,
            "name": bot.get("name"),
            "generation": generation,
            "genome": bot.get("genome"),
            "parent_ids": bot.get("parent_ids", []),
            "llm_advice": bot.get("llm_advice"),
            "created": bot.get("created"),
            "stats": bot.get("stats", {})
        }, f, indent=2)

    # Copy source file if it exists
    source_file = PROJECT_ROOT / "bots" / "generated" / f"{bot_id}.java"
    if source_file.exists():
        dest_file = gen_dir / f"{bot_id}.java"
        shutil.copy(source_file, dest_file)

    return str(genome_file)


def archive_generation(population: List[Dict], generation: int, best_bot: Dict = None):
    """Archive an entire generation"""
    ensure_dirs()

    # Archive all bots
    for bot in population:
        archive_bot(bot, generation)

    # Add generation event to timeline
    timeline = load_timeline()
    timeline.append({
        "type": "generation",
        "generation": generation,
        "timestamp": datetime.now().isoformat(),
        "population_size": len(population),
        "best_bot": best_bot["id"] if best_bot else None,
        "best_elo": best_bot["stats"].get("elo") if best_bot else None
    })
    save_timeline(timeline)


def archive_llm_advice(bot_id: str, analysis: Dict, advice: Dict, generation: int):
    """Archive LLM advisor recommendations"""
    ensure_dirs()

    advice_file = ARCHIVE_DIR / "llm_advice.json"

    # Load existing advice
    if advice_file.exists():
        with open(advice_file) as f:
            advice_log = json.load(f)
    else:
        advice_log = []

    advice_log.append({
        "timestamp": datetime.now().isoformat(),
        "generation": generation,
        "bot_id": bot_id,
        "analysis_summary": analysis.get("summary", {}),
        "problems": analysis.get("problems", []),
        "advice": advice
    })

    with open(advice_file, 'w') as f:
        json.dump(advice_log, f, indent=2)

    # Add to timeline
    timeline = load_timeline()
    timeline.append({
        "type": "llm_advice",
        "timestamp": datetime.now().isoformat(),
        "generation": generation,
        "bot_id": bot_id,
        "summary": advice.get("summary", "Strategic advice given")
    })
    save_timeline(timeline)


def get_generation_summary(generation: int) -> Dict:
    """Get summary of a generation from archives"""
    gen_dir = BOTS_ARCHIVE / f"gen{generation:03d}"

    if not gen_dir.exists():
        return {"error": f"Generation {generation} not found"}

    bots = []
    for genome_file in gen_dir.glob("*_genome.json"):
        with open(genome_file) as f:
            bots.append(json.load(f))

    # Sort by Elo
    bots.sort(key=lambda b: b.get("stats", {}).get("elo", 1500), reverse=True)

    return {
        "generation": generation,
        "bot_count": len(bots),
        "bots": bots,
        "top_3": bots[:3] if len(bots) >= 3 else bots
    }


def get_evolution_summary() -> Dict:
    """Get overall evolution summary"""
    timeline = load_timeline()

    generations = [e for e in timeline if e["type"] == "generation"]
    battles = [e for e in timeline if e["type"] == "battle"]
    advice_events = [e for e in timeline if e["type"] == "llm_advice"]

    # Find best bot across all generations
    best_elo = 0
    best_bot = None
    for gen in generations:
        if gen.get("best_elo", 0) > best_elo:
            best_elo = gen["best_elo"]
            best_bot = gen["best_bot"]

    return {
        "total_generations": len(generations),
        "total_battles": len(battles),
        "total_llm_advice": len(advice_events),
        "best_bot": best_bot,
        "best_elo": best_elo,
        "timeline_entries": len(timeline)
    }


def export_for_viewer() -> Dict:
    """Export data for the evolution viewer HTML"""
    timeline = load_timeline()

    # Get all generations
    generations = []
    for gen_dir in sorted(BOTS_ARCHIVE.glob("gen*")):
        gen_num = int(gen_dir.name[3:])
        summary = get_generation_summary(gen_num)
        if "error" not in summary:
            generations.append(summary)

    # Get recent battles
    recent_battles = []
    for battle_file in sorted(BATTLES_ARCHIVE.glob("*.json"))[-50:]:
        with open(battle_file) as f:
            recent_battles.append(json.load(f))

    # Get LLM advice log
    advice_file = ARCHIVE_DIR / "llm_advice.json"
    llm_advice = []
    if advice_file.exists():
        with open(advice_file) as f:
            llm_advice = json.load(f)

    return {
        "generated": datetime.now().isoformat(),
        "summary": get_evolution_summary(),
        "generations": generations,
        "recent_battles": recent_battles,
        "llm_advice": llm_advice,
        "timeline": timeline[-100:]  # Last 100 events
    }


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python history_tracker.py summary       - Show evolution summary")
        print("  python history_tracker.py generation N  - Show generation N details")
        print("  python history_tracker.py timeline      - Show recent timeline")
        print("  python history_tracker.py export        - Export data for viewer")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == 'summary':
        summary = get_evolution_summary()
        print(json.dumps(summary, indent=2))

    elif cmd == 'generation':
        if len(sys.argv) < 3:
            print("Usage: python history_tracker.py generation N")
            sys.exit(1)
        gen = int(sys.argv[2])
        summary = get_generation_summary(gen)
        print(json.dumps(summary, indent=2))

    elif cmd == 'timeline':
        timeline = load_timeline()
        for event in timeline[-20:]:
            print(f"[{event['timestamp'][:19]}] {event['type']}: {event.get('summary', event.get('generation', ''))}")

    elif cmd == 'export':
        data = export_for_viewer()
        export_file = ARCHIVE_DIR / "viewer_data.json"
        with open(export_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Exported to {export_file}")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
