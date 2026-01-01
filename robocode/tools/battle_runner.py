#!/usr/bin/env python3
"""
Battle Runner - Execute Robocode battles headlessly and parse results
"""

import json
import os
import subprocess
import tempfile
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
ROBOCODE_DIR = PROJECT_ROOT / "robocode-install"
CONFIG_FILE = PROJECT_ROOT / "config" / "robocode.json"
RESULTS_DIR = PROJECT_ROOT / "battles" / "results"


def load_config() -> dict:
    """Load Robocode configuration"""
    with open(CONFIG_FILE) as f:
        return json.load(f)


def create_battle_file(
    robots: List[str],
    rounds: int = 10,
    width: int = 800,
    height: int = 600
) -> str:
    """Create a temporary battle file"""
    content = f"""#Battle Properties
robocode.battleField.width={width}
robocode.battleField.height={height}
robocode.battle.numRounds={rounds}
robocode.battle.gunCoolingRate=0.1
robocode.battle.rules.inactivityTime=450
robocode.battle.selectedRobots={','.join(robots)}
"""
    # Create temp file
    fd, path = tempfile.mkstemp(suffix='.battle', prefix='evo_')
    with os.fdopen(fd, 'w') as f:
        f.write(content)
    return path


def parse_results(results_file: str) -> List[Dict]:
    """Parse Robocode results file into structured data"""
    results = []

    with open(results_file) as f:
        lines = f.readlines()

    # Skip header lines, find data
    for line in lines:
        # Match result lines like: "1st: sample.Walls	5236 (45%)	1700..."
        match = re.match(
            r'(\d+)(?:st|nd|rd|th):\s+(\S+)\s+(\d+)\s+\((\d+)%\)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*',
            line.strip()
        )
        if match:
            results.append({
                'rank': int(match.group(1)),
                'name': match.group(2),
                'total_score': int(match.group(3)),
                'score_percent': int(match.group(4)),
                'survival': int(match.group(5)),
                'survival_bonus': int(match.group(6)),
                'bullet_damage': int(match.group(7)),
                'bullet_bonus': int(match.group(8)),
                'ram_damage': int(match.group(9)),
                'ram_bonus': int(match.group(10)),
                'firsts': int(match.group(11)),
                'seconds': int(match.group(12)),
                'thirds': int(match.group(13))
            })

    return results


def run_battle(
    robots: List[str],
    rounds: int = 10,
    width: int = 800,
    height: int = 600,
    save_results: bool = True
) -> Tuple[List[Dict], str]:
    """
    Run a battle between specified robots

    Args:
        robots: List of robot names (e.g., ['sample.Corners', 'sample.Walls'])
        rounds: Number of rounds
        width: Battlefield width
        height: Battlefield height
        save_results: Whether to save results to file

    Returns:
        Tuple of (parsed results, results file path)
    """
    config = load_config()

    # Create battle file
    battle_file = create_battle_file(robots, rounds, width, height)

    # Create results file
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = RESULTS_DIR / f"battle_{timestamp}.txt"

    # Build command using the shell script approach
    cmd = f"""cd "{ROBOCODE_DIR}" && ./robocode.sh -battle "{battle_file}" -nodisplay -results "{results_file}" """

    try:
        # Run battle
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        # Parse results
        if results_file.exists():
            parsed = parse_results(str(results_file))
        else:
            parsed = []

    finally:
        # Cleanup temp battle file
        if os.path.exists(battle_file):
            os.remove(battle_file)

    # Remove results file if not saving
    if not save_results and results_file.exists():
        os.remove(results_file)
        results_file = None

    return parsed, str(results_file) if results_file else None


def run_1v1(robot1: str, robot2: str, rounds: int = 10) -> Dict:
    """
    Run a 1v1 battle and return winner info

    Returns dict with:
        - winner: name of winning robot
        - loser: name of losing robot
        - winner_score: winner's total score
        - loser_score: loser's total score
        - margin: score difference
    """
    results, _ = run_battle([robot1, robot2], rounds=rounds, save_results=False)

    if len(results) < 2:
        return {'error': 'Battle failed', 'results': results}

    winner = results[0]
    loser = results[1]

    return {
        'winner': winner['name'],
        'loser': loser['name'],
        'winner_score': winner['total_score'],
        'loser_score': loser['total_score'],
        'margin': winner['total_score'] - loser['total_score'],
        'winner_firsts': winner['firsts'],
        'loser_firsts': loser['firsts']
    }


def get_available_robots() -> List[str]:
    """Get list of available robots in the Robocode installation"""
    robots_dir = ROBOCODE_DIR / "robots"
    robots = []

    # Find all .java files and extract package.ClassName
    for java_file in robots_dir.rglob("*.java"):
        rel_path = java_file.relative_to(robots_dir)
        # Convert path to package name: sample/Corners.java -> sample.Corners
        package_class = str(rel_path.with_suffix('')).replace('/', '.').replace('\\', '.')
        robots.append(package_class)

    return sorted(robots)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python battle_runner.py list              - List available robots")
        print("  python battle_runner.py run <r1> <r2>     - Run 1v1 battle")
        print("  python battle_runner.py test              - Run test battle")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == 'list':
        robots = get_available_robots()
        print(f"Available robots ({len(robots)}):")
        for r in robots:
            print(f"  {r}")

    elif cmd == 'run':
        if len(sys.argv) < 4:
            print("Usage: python battle_runner.py run <robot1> <robot2>")
            sys.exit(1)

        r1, r2 = sys.argv[2], sys.argv[3]
        print(f"Running battle: {r1} vs {r2}")
        result = run_1v1(r1, r2)
        print(f"Winner: {result['winner']} ({result['winner_score']})")
        print(f"Loser: {result['loser']} ({result['loser_score']})")
        print(f"Margin: {result['margin']}")

    elif cmd == 'test':
        print("Running test battle: sample.Walls vs sample.Corners")
        result = run_1v1('sample.Walls', 'sample.Corners')
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
