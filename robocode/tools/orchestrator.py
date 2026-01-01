#!/usr/bin/env python3
"""
Evolution Orchestrator - Main loop for evolving Robocode bots
"""

import json
import random
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).parent.parent

# Import our modules
from bot_generator import (
    create_genome, create_and_compile_bot, mutate_genome, crossover_genomes,
    MOVEMENT_MODULES, GUN_MODULES, RADAR_MODULES
)
from battle_runner import run_1v1, run_battle
from elo_system import update_elo, get_rating, get_leaderboard, load_ratings, save_ratings
from claude_advisor import advise_bot, apply_advice, analyze_bot_performance
from history_tracker import archive_battle, archive_generation, archive_llm_advice


# Files
POPULATION_FILE = PROJECT_ROOT / "data" / "population.json"
STATE_FILE = PROJECT_ROOT / "data" / "evolution_state.json"
CONFIG_FILE = PROJECT_ROOT / "config" / "evolution.json"


def load_config() -> Dict:
    """Load evolution configuration"""
    with open(CONFIG_FILE) as f:
        return json.load(f)


def load_population() -> Dict:
    """Load current population"""
    if POPULATION_FILE.exists():
        with open(POPULATION_FILE) as f:
            return json.load(f)
    return {"generation": 0, "population_size": 0, "bots": []}


def save_population(data: Dict):
    """Save population to file"""
    with open(POPULATION_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def load_state() -> Dict:
    """Load evolution state"""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "session_id": None,
        "timestamp": None,
        "last_heartbeat": None,
        "status": "idle",
        "generation": 0,
        "total_battles": 0,
        "best_bot": None,
        "current_task": None,
        "activity_feed": [],
        "agent_builders": [],
        "meta_state": {}
    }


def save_state(data: Dict):
    """Save evolution state"""
    data["last_heartbeat"] = datetime.now().isoformat()
    with open(STATE_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def update_heartbeat(task_description: str = None):
    """Update heartbeat for dashboard monitoring"""
    state = load_state()
    state["last_heartbeat"] = datetime.now().isoformat()
    if task_description:
        state["current_task"] = {"description": task_description, "timestamp": datetime.now().isoformat()}
    save_state(state)


def log_activity(message: str, activity_type: str = "info"):
    """Add to activity feed"""
    state = load_state()
    activity = {
        "timestamp": datetime.now().isoformat(),
        "type": activity_type,
        "message": message
    }
    state["activity_feed"] = [activity] + state.get("activity_feed", [])[:50]  # Keep last 50
    save_state(state)


def initialize_population(size: int = 10) -> List[Dict]:
    """Create initial random population"""
    population = []

    for i in range(size):
        bot_name = f"Evo_Gen0_{i:03d}"
        genome = create_genome()

        print(f"Creating {bot_name}: {genome['movement_module']} + {genome['gun_module']}")

        if create_and_compile_bot(bot_name, genome):
            bot = {
                "id": bot_name,
                "name": f"sample.{bot_name}",
                "genome": genome,
                "created": datetime.now().isoformat(),
                "generation": 0,
                "parent_ids": [],
                "stats": {"battles": 0, "wins": 0}
            }
            population.append(bot)
        else:
            print(f"Failed to create {bot_name}")

    return population


def evaluate_bot(bot: Dict, opponents: List[str], battles_per_opponent: int = 3, generation: int = 0) -> Dict:
    """Evaluate a bot against opponents and update its stats"""
    bot_name = bot["name"]
    total_score = 0
    total_wins = 0
    total_battles = 0

    for opp in opponents:
        for _ in range(battles_per_opponent):
            result = run_1v1(bot_name, opp, rounds=5)

            if "error" in result:
                print(f"  Battle error: {result}")
                continue

            total_battles += 1

            # Archive the battle
            archive_battle(bot_name, opp, result, generation, context="evaluation")

            if result["winner"] == bot_name:
                total_wins += 1
                update_elo(bot_name, opp, result["winner_score"], result["loser_score"])
            else:
                update_elo(opp, bot_name, result["winner_score"], result["loser_score"])

            total_score += result.get("winner_score" if result["winner"] == bot_name else "loser_score", 0)

    # Update bot stats
    bot["stats"]["battles"] = bot["stats"].get("battles", 0) + total_battles
    bot["stats"]["wins"] = bot["stats"].get("wins", 0) + total_wins
    bot["stats"]["elo"] = get_rating(bot_name)

    return bot


def select_parents(population: List[Dict], num_parents: int = 2) -> List[Dict]:
    """Tournament selection to choose parents"""
    tournament_size = 3
    selected = []

    for _ in range(num_parents):
        # Random tournament
        tournament = random.sample(population, min(tournament_size, len(population)))
        # Sort by Elo
        tournament.sort(key=lambda b: b["stats"].get("elo", 1500), reverse=True)
        selected.append(tournament[0])

    return selected


def create_llm_improved_bot(parent: Dict, generation: int, bot_index: int) -> Optional[Dict]:
    """Use Claude advisor to create an improved version of a bot"""
    new_name = f"Evo_Gen{generation}_{bot_index:03d}"

    print(f"  Getting Claude advice for {parent['id']}...")
    update_heartbeat(f"Claude advising on {parent['id']}")

    result = advise_bot(parent)

    if result and result.get("advice"):
        advice = result["advice"]
        analysis = result.get("analysis", {})
        confidence = advice.get("confidence", 0)

        # Archive the LLM advice
        archive_llm_advice(parent["id"], analysis, advice, generation)

        if confidence >= 0.5:  # Only apply high-confidence advice
            improved_genome = apply_advice(parent, advice)
            log_activity(f"Claude advised: {advice.get('summary', 'improvement')}", "llm_advice")

            if create_and_compile_bot(new_name, improved_genome):
                return {
                    "id": new_name,
                    "name": f"sample.{new_name}",
                    "genome": improved_genome,
                    "created": datetime.now().isoformat(),
                    "generation": generation,
                    "parent_ids": [parent["id"]],
                    "llm_advice": advice.get("summary", ""),
                    "stats": {"battles": 0, "wins": 0}
                }

    return None


def create_next_generation(population: List[Dict], generation: int, config: Dict, use_llm: bool = True) -> List[Dict]:
    """Create next generation through LLM advice, selection, crossover, and mutation"""
    new_population = []
    pop_size = config["population_size"]

    # Elitism: Keep top 2 bots
    sorted_pop = sorted(population, key=lambda b: b["stats"].get("elo", 1500), reverse=True)
    elites = sorted_pop[:2]

    for elite in elites:
        # Clone elite with new name
        new_name = f"Evo_Gen{generation}_{len(new_population):03d}"
        genome = elite["genome"].copy()

        if create_and_compile_bot(new_name, genome):
            bot = {
                "id": new_name,
                "name": f"sample.{new_name}",
                "genome": genome,
                "created": datetime.now().isoformat(),
                "generation": generation,
                "parent_ids": [elite["id"]],
                "stats": {"battles": 0, "wins": 0}
            }
            new_population.append(bot)

    # LLM-guided improvement: Get Claude advice for top bots
    if use_llm:
        print("\n--- LLM-Guided Improvement Phase ---")
        log_activity("Starting LLM-guided improvement phase", "llm_phase")

        # Try to create LLM-improved versions of top 3 bots
        for parent in sorted_pop[:3]:
            if len(new_population) >= pop_size:
                break

            improved = create_llm_improved_bot(parent, generation, len(new_population))
            if improved:
                new_population.append(improved)
                print(f"  Created LLM-improved bot: {improved['id']}")

    # Fill remaining slots through traditional crossover and mutation
    while len(new_population) < pop_size:
        new_name = f"Evo_Gen{generation}_{len(new_population):03d}"

        if random.random() < config["crossover"]["rate"] and len(population) >= 2:
            # Crossover
            parents = select_parents(population, 2)
            child_genome = crossover_genomes(parents[0]["genome"], parents[1]["genome"])
            parent_ids = [parents[0]["id"], parents[1]["id"]]
        else:
            # Mutation only
            parent = select_parents(population, 1)[0]
            child_genome = mutate_genome(parent["genome"], config["mutation"]["rate"])
            parent_ids = [parent["id"]]

        if create_and_compile_bot(new_name, child_genome):
            bot = {
                "id": new_name,
                "name": f"sample.{new_name}",
                "genome": child_genome,
                "created": datetime.now().isoformat(),
                "generation": generation,
                "parent_ids": parent_ids,
                "stats": {"battles": 0, "wins": 0}
            }
            new_population.append(bot)

    return new_population


def run_generation(generation: int, population: List[Dict], config: Dict) -> List[Dict]:
    """Run a single generation of evolution"""
    print(f"\n=== Generation {generation} ===")
    log_activity(f"Starting generation {generation}", "evolution")
    update_heartbeat(f"Running generation {generation}")

    # Get benchmark opponents
    benchmarks = ["sample.Walls", "sample.Corners", "sample.SpinBot", "sample.Fire"]

    # Evaluate each bot
    for i, bot in enumerate(population):
        print(f"\nEvaluating {bot['id']} ({i+1}/{len(population)})")
        update_heartbeat(f"Evaluating {bot['id']}")
        evaluate_bot(bot, benchmarks, battles_per_opponent=2, generation=generation)
        print(f"  Elo: {bot['stats'].get('elo', 1500)}, Wins: {bot['stats']['wins']}/{bot['stats']['battles']}")

    # Sort by Elo
    population.sort(key=lambda b: b["stats"].get("elo", 1500), reverse=True)

    # Log best bot
    best = population[0]
    print(f"\nBest bot: {best['id']} (Elo: {best['stats'].get('elo', 1500)})")
    log_activity(f"Gen {generation} best: {best['id']} (Elo: {best['stats'].get('elo', 1500)})", "milestone")

    # Archive the generation
    archive_generation(population, generation, best)

    # Update state
    state = load_state()
    state["generation"] = generation
    state["best_bot"] = {
        "id": best["id"],
        "elo": best["stats"].get("elo", 1500),
        "genome": f"{best['genome']['movement_module']} + {best['genome']['gun_module']}"
    }
    save_state(state)

    return population


def run_evolution(num_generations: int = 5):
    """Main evolution loop"""
    config = load_config()

    # Initialize state
    state = load_state()
    state["session_id"] = f"evo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    state["timestamp"] = datetime.now().isoformat()
    state["status"] = "running"
    save_state(state)

    log_activity("Evolution started", "start")

    # Load or create population
    pop_data = load_population()

    if not pop_data["bots"]:
        print("Initializing population...")
        update_heartbeat("Initializing population")
        population = initialize_population(config["population_size"])
        pop_data = {
            "generation": 0,
            "population_size": len(population),
            "bots": population
        }
        save_population(pop_data)
    else:
        population = pop_data["bots"]
        print(f"Resuming from generation {pop_data['generation']} with {len(population)} bots")

    current_gen = pop_data["generation"]

    # Run generations
    for gen in range(current_gen, current_gen + num_generations):
        population = run_generation(gen, population, config)

        # Save progress
        pop_data["generation"] = gen
        pop_data["bots"] = population
        save_population(pop_data)

        # Create next generation
        if gen < current_gen + num_generations - 1:
            print(f"\nCreating generation {gen + 1}...")
            update_heartbeat(f"Creating generation {gen + 1}")
            population = create_next_generation(population, gen + 1, config)
            pop_data["bots"] = population
            pop_data["generation"] = gen + 1
            save_population(pop_data)

    # Finalize
    state = load_state()
    state["status"] = "completed"
    save_state(state)

    log_activity("Evolution completed", "complete")

    # Print final leaderboard
    print("\n=== Final Leaderboard ===")
    from elo_system import print_leaderboard
    print_leaderboard(15)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python orchestrator.py run [generations]  - Run evolution")
        print("  python orchestrator.py init               - Initialize population")
        print("  python orchestrator.py status             - Show current status")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == 'run':
        gens = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        run_evolution(gens)

    elif cmd == 'init':
        config = load_config()
        pop = initialize_population(config["population_size"])
        save_population({
            "generation": 0,
            "population_size": len(pop),
            "bots": pop
        })
        print(f"Initialized population with {len(pop)} bots")

    elif cmd == 'status':
        state = load_state()
        pop = load_population()

        print(f"Status: {state['status']}")
        print(f"Generation: {state.get('generation', 0)}")
        print(f"Population: {len(pop.get('bots', []))} bots")

        if state.get("best_bot"):
            print(f"Best bot: {state['best_bot']['id']} (Elo: {state['best_bot']['elo']})")

        print("\nRecent activity:")
        for act in state.get("activity_feed", [])[:5]:
            print(f"  [{act['timestamp'][:19]}] {act['message']}")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
