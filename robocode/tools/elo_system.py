#!/usr/bin/env python3
"""
Elo Rating System for Robocode bots
"""

import json
import math
from pathlib import Path
from typing import Dict, Tuple, Optional
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
ELO_FILE = PROJECT_ROOT / "data" / "elo_ratings.json"


def load_ratings() -> Dict:
    """Load Elo ratings from file"""
    if ELO_FILE.exists():
        with open(ELO_FILE) as f:
            return json.load(f)
    return {
        "k_factor": 32,
        "initial_rating": 1500,
        "ratings": {}
    }


def save_ratings(data: Dict):
    """Save Elo ratings to file"""
    ELO_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ELO_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def get_rating(bot_name: str, data: Dict = None) -> int:
    """Get current rating for a bot"""
    if data is None:
        data = load_ratings()

    if bot_name in data["ratings"]:
        return data["ratings"][bot_name]["elo"]
    return data["initial_rating"]


def expected_score(rating_a: int, rating_b: int) -> float:
    """Calculate expected score for player A against player B"""
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))


def update_elo(
    winner: str,
    loser: str,
    winner_score: int = None,
    loser_score: int = None,
    k_factor: int = None
) -> Tuple[int, int]:
    """
    Update Elo ratings after a match.

    Args:
        winner: Name of winning bot
        loser: Name of losing bot
        winner_score: Optional score for margin calculation
        loser_score: Optional score for margin calculation
        k_factor: Optional override for K-factor

    Returns:
        Tuple of (new_winner_rating, new_loser_rating)
    """
    data = load_ratings()
    k = k_factor or data["k_factor"]

    # Get current ratings
    rating_winner = get_rating(winner, data)
    rating_loser = get_rating(loser, data)

    # Calculate expected scores
    exp_winner = expected_score(rating_winner, rating_loser)
    exp_loser = expected_score(rating_loser, rating_winner)

    # Calculate score margin bonus (optional)
    margin_bonus = 1.0
    if winner_score is not None and loser_score is not None:
        total = winner_score + loser_score
        if total > 0:
            # Larger margins give slightly bigger Elo changes
            margin_ratio = (winner_score - loser_score) / total
            margin_bonus = 1 + margin_ratio * 0.5  # Up to 1.5x

    # Update ratings
    # Winner gets actual score of 1, loser gets 0
    new_winner = round(rating_winner + k * margin_bonus * (1 - exp_winner))
    new_loser = round(rating_loser + k * margin_bonus * (0 - exp_loser))

    # Ensure minimum rating
    new_loser = max(100, new_loser)

    # Update data
    if winner not in data["ratings"]:
        data["ratings"][winner] = {"elo": new_winner, "battles": 0, "type": "evolved"}
    else:
        data["ratings"][winner]["elo"] = new_winner

    if loser not in data["ratings"]:
        data["ratings"][loser] = {"elo": new_loser, "battles": 0, "type": "evolved"}
    else:
        data["ratings"][loser]["elo"] = new_loser

    # Increment battle counts
    data["ratings"][winner]["battles"] = data["ratings"][winner].get("battles", 0) + 1
    data["ratings"][loser]["battles"] = data["ratings"][loser].get("battles", 0) + 1

    # Add timestamp
    data["ratings"][winner]["last_battle"] = datetime.now().isoformat()
    data["ratings"][loser]["last_battle"] = datetime.now().isoformat()

    save_ratings(data)

    return new_winner, new_loser


def get_leaderboard(limit: int = 20) -> list:
    """Get top bots by Elo rating"""
    data = load_ratings()
    sorted_bots = sorted(
        data["ratings"].items(),
        key=lambda x: x[1]["elo"],
        reverse=True
    )
    return sorted_bots[:limit]


def get_matchup(bot: str, opponent_pool: list = None) -> Optional[str]:
    """
    Find a good opponent for a bot based on Elo.
    Prefers opponents within 200 Elo points.
    """
    data = load_ratings()
    bot_rating = get_rating(bot, data)

    if opponent_pool is None:
        # Use all known bots
        opponent_pool = [name for name in data["ratings"].keys() if name != bot]

    if not opponent_pool:
        return None

    # Sort by Elo distance
    candidates = []
    for opp in opponent_pool:
        opp_rating = get_rating(opp, data)
        distance = abs(bot_rating - opp_rating)
        candidates.append((opp, distance, opp_rating))

    # Sort by distance, prefer closer matches
    candidates.sort(key=lambda x: x[1])

    # Return closest match, but add some randomness for variety
    import random
    if len(candidates) > 3:
        return random.choice(candidates[:3])[0]
    return candidates[0][0]


def print_leaderboard(limit: int = 20):
    """Print formatted leaderboard"""
    leaderboard = get_leaderboard(limit)

    print(f"\n{'Rank':<6}{'Bot':<30}{'Elo':<8}{'Battles':<10}{'Type':<10}")
    print("-" * 64)

    for i, (name, stats) in enumerate(leaderboard, 1):
        bot_type = stats.get("type", "unknown")
        battles = stats.get("battles", 0)
        print(f"{i:<6}{name:<30}{stats['elo']:<8}{battles:<10}{bot_type:<10}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python elo_system.py leaderboard       - Show leaderboard")
        print("  python elo_system.py rating <bot>      - Get bot rating")
        print("  python elo_system.py update <w> <l>    - Record match result")
        print("  python elo_system.py matchup <bot>     - Find good opponent")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == 'leaderboard':
        print_leaderboard()

    elif cmd == 'rating':
        if len(sys.argv) < 3:
            print("Usage: python elo_system.py rating <bot>")
            sys.exit(1)
        bot = sys.argv[2]
        rating = get_rating(bot)
        print(f"{bot}: Elo {rating}")

    elif cmd == 'update':
        if len(sys.argv) < 4:
            print("Usage: python elo_system.py update <winner> <loser>")
            sys.exit(1)
        winner, loser = sys.argv[2], sys.argv[3]
        new_w, new_l = update_elo(winner, loser)
        print(f"Updated ratings:")
        print(f"  {winner}: {new_w}")
        print(f"  {loser}: {new_l}")

    elif cmd == 'matchup':
        if len(sys.argv) < 3:
            print("Usage: python elo_system.py matchup <bot>")
            sys.exit(1)
        bot = sys.argv[2]
        opponent = get_matchup(bot)
        if opponent:
            print(f"Suggested opponent for {bot}: {opponent}")
        else:
            print("No suitable opponent found")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
