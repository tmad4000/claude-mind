#!/usr/bin/env python3
"""
Bot Generator - Compose modular bot templates into complete robots
"""

import json
import os
import random
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "bots" / "templates"
GENERATED_DIR = PROJECT_ROOT / "bots" / "generated"
COMPILED_DIR = PROJECT_ROOT / "bots" / "compiled"
ROBOCODE_DIR = PROJECT_ROOT / "robocode-install"


# Default parameter ranges for evolution
PARAM_RANGES = {
    "PARAM_PREFERRED_DISTANCE": (150, 400),
    "PARAM_MOVE_DISTANCE": (50, 200),
    "PARAM_DIRECTION_CHANGE_RATE": (0.01, 0.1),
    "PARAM_DIRECTION_CHANGE_INTERVAL": (10, 50),
    "PARAM_RANDOM_CHANGE_RATE": (0.01, 0.05),
    "PARAM_MAX_TURN_ANGLE": (30, 90),
    "PARAM_FIRE_POWER_CLOSE": (2.5, 3.0),
    "PARAM_FIRE_POWER_MEDIUM": (1.5, 2.5),
    "PARAM_FIRE_POWER_FAR": (0.5, 1.5),
    "PARAM_RADAR_LOCK_EXTRA": (5, 20),
}

# Available modules
MOVEMENT_MODULES = ["Perpendicular", "Random", "BasicSurfer"]
GUN_MODULES = ["HeadOn", "Linear", "GuessFactor"]
RADAR_MODULES = ["Spin", "Lock"]

# Colors for bots
COLORS = [
    "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF",
    "#FF8000", "#8000FF", "#0080FF", "#FF0080", "#80FF00", "#00FF80",
    "#800000", "#008000", "#000080", "#808000", "#800080", "#008080"
]


def load_template(name: str) -> str:
    """Load a template file"""
    with open(TEMPLATES_DIR / name) as f:
        return f.read()


def load_module(module_type: str, module_name: str) -> str:
    """Load a module (movement, gun, or radar)"""
    path = TEMPLATES_DIR / module_type / f"{module_name}.java"
    with open(path) as f:
        return f.read()


def generate_parameters(genome: Optional[Dict] = None) -> Dict[str, float]:
    """Generate or use provided parameters"""
    params = {}
    for name, (min_val, max_val) in PARAM_RANGES.items():
        if genome and name in genome.get("parameters", {}):
            params[name] = genome["parameters"][name]
        else:
            params[name] = random.uniform(min_val, max_val)
    return params


def format_parameters(params: Dict[str, float]) -> str:
    """Format parameters as Java code"""
    lines = []
    for name, value in params.items():
        if isinstance(value, float):
            lines.append(f"    private static final double {name} = {value:.4f};")
        else:
            lines.append(f"    private static final double {name} = {value};")
    return "\n".join(lines)


def create_genome(
    movement: str = None,
    gun: str = None,
    radar: str = None,
    parameters: Dict = None
) -> Dict:
    """Create a bot genome"""
    return {
        "movement_module": movement or random.choice(MOVEMENT_MODULES),
        "gun_module": gun or random.choice(GUN_MODULES),
        "radar_module": radar or random.choice(RADAR_MODULES),
        "parameters": parameters or generate_parameters(),
        "body_color": random.choice(COLORS),
        "gun_color": random.choice(COLORS),
        "radar_color": random.choice(COLORS)
    }


def generate_bot(bot_name: str, genome: Dict) -> str:
    """Generate complete bot Java code from genome"""
    # Load base template
    template = load_template("BaseAdvancedBot.java")

    # Load modules
    movement_code = load_module("movement", genome["movement_module"])
    gun_code = load_module("gun", genome["gun_module"])
    radar_code = load_module("radar", genome["radar_module"])

    # Generate parameters
    params = generate_parameters(genome)
    params_code = format_parameters(params)

    # Substitute into template
    code = template
    code = code.replace("{{BOT_NAME}}", bot_name)
    code = code.replace("{{PARAMETERS}}", params_code)
    code = code.replace("{{MOVEMENT_CODE}}", movement_code)
    code = code.replace("{{GUN_CODE}}", gun_code)
    code = code.replace("{{RADAR_CODE}}", radar_code)
    code = code.replace("{{BODY_COLOR}}", genome.get("body_color", "#FF0000"))
    code = code.replace("{{GUN_COLOR}}", genome.get("gun_color", "#00FF00"))
    code = code.replace("{{RADAR_COLOR}}", genome.get("radar_color", "#0000FF"))

    return code


def save_bot(bot_name: str, code: str) -> Path:
    """Save bot to generated directory"""
    # Create sample package directory (Robocode recognizes sample package)
    package_dir = GENERATED_DIR / "sample"
    package_dir.mkdir(parents=True, exist_ok=True)

    # Save file
    file_path = package_dir / f"{bot_name}.java"
    with open(file_path, 'w') as f:
        f.write(code)

    return file_path


def compile_bot(bot_name: str) -> bool:
    """Compile a generated bot"""
    source_file = GENERATED_DIR / "sample" / f"{bot_name}.java"

    if not source_file.exists():
        print(f"Source file not found: {source_file}")
        return False

    # Create output directory
    output_dir = COMPILED_DIR / "sample"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build classpath
    robocode_jar = ROBOCODE_DIR / "libs" / "robocode.jar"

    # Compile with Java 8 target (Robocode compatibility)
    cmd = [
        "javac",
        "-source", "8",
        "-target", "8",
        "-cp", str(robocode_jar),
        "-d", str(COMPILED_DIR),
        str(source_file)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Compilation failed for {bot_name}:")
        print(result.stderr)
        return False

    return True


def install_bot(bot_name: str, genome: Dict = None) -> bool:
    """Copy compiled bot to Robocode robots directory with all required files"""
    import shutil

    # Source files
    class_file = COMPILED_DIR / "sample" / f"{bot_name}.class"
    source_file = GENERATED_DIR / "sample" / f"{bot_name}.java"

    if not class_file.exists():
        print(f"Class file not found: {class_file}")
        return False

    # Create destination directory
    dest_dir = ROBOCODE_DIR / "robots" / "sample"
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Copy class file
    shutil.copy(class_file, dest_dir / f"{bot_name}.class")

    # Copy source file
    if source_file.exists():
        shutil.copy(source_file, dest_dir / f"{bot_name}.java")

    # Create properties file (required by Robocode)
    props_content = f"""#Robot Properties
robot.description=Evolved bot: {genome.get('movement_module', 'Unknown')} + {genome.get('gun_module', 'Unknown')}
robot.webpage=
robocode.version=1.10.1
robot.java.source.included=true
robot.author.name=Evolution System
robot.classname=sample.{bot_name}
robot.name={bot_name}
"""
    with open(dest_dir / f"{bot_name}.properties", 'w') as f:
        f.write(props_content)

    # Delete robot.database to force Robocode to rescan
    db_file = ROBOCODE_DIR / "robots" / "robot.database"
    if db_file.exists():
        db_file.unlink()

    return True


def create_and_compile_bot(bot_name: str, genome: Dict = None) -> bool:
    """Full pipeline: generate, save, compile, and install a bot"""
    if genome is None:
        genome = create_genome()

    # Generate code
    code = generate_bot(bot_name, genome)

    # Save
    save_bot(bot_name, code)

    # Compile
    if not compile_bot(bot_name):
        return False

    # Install (pass genome for properties file)
    if not install_bot(bot_name, genome):
        return False

    print(f"Successfully created bot: sample.{bot_name}")
    return True


def mutate_genome(genome: Dict, mutation_rate: float = 0.3) -> Dict:
    """Create a mutated copy of a genome"""
    new_genome = genome.copy()
    new_genome["parameters"] = genome["parameters"].copy()

    # Possibly mutate modules
    if random.random() < mutation_rate:
        new_genome["movement_module"] = random.choice(MOVEMENT_MODULES)
    if random.random() < mutation_rate:
        new_genome["gun_module"] = random.choice(GUN_MODULES)
    if random.random() < mutation_rate:
        new_genome["radar_module"] = random.choice(RADAR_MODULES)

    # Mutate parameters
    for name, (min_val, max_val) in PARAM_RANGES.items():
        if random.random() < mutation_rate:
            # Add noise to current value
            current = new_genome["parameters"].get(name, (min_val + max_val) / 2)
            noise = (max_val - min_val) * random.uniform(-0.2, 0.2)
            new_val = max(min_val, min(max_val, current + noise))
            new_genome["parameters"][name] = new_val

    # New colors
    if random.random() < 0.5:
        new_genome["body_color"] = random.choice(COLORS)
        new_genome["gun_color"] = random.choice(COLORS)
        new_genome["radar_color"] = random.choice(COLORS)

    return new_genome


def crossover_genomes(parent1: Dict, parent2: Dict) -> Dict:
    """Create offspring from two parent genomes"""
    child = {}

    # Random module selection from parents
    child["movement_module"] = random.choice([parent1["movement_module"], parent2["movement_module"]])
    child["gun_module"] = random.choice([parent1["gun_module"], parent2["gun_module"]])
    child["radar_module"] = random.choice([parent1["radar_module"], parent2["radar_module"]])

    # Average parameters with some randomness
    child["parameters"] = {}
    for name in PARAM_RANGES:
        p1_val = parent1["parameters"].get(name, PARAM_RANGES[name][0])
        p2_val = parent2["parameters"].get(name, PARAM_RANGES[name][0])

        # Weighted average with random weight
        weight = random.random()
        child["parameters"][name] = weight * p1_val + (1 - weight) * p2_val

    # New colors
    child["body_color"] = random.choice(COLORS)
    child["gun_color"] = random.choice(COLORS)
    child["radar_color"] = random.choice(COLORS)

    return child


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python bot_generator.py create <name>     - Create a random bot")
        print("  python bot_generator.py test              - Create and test a bot")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == 'create':
        if len(sys.argv) < 3:
            name = f"Evo_{datetime.now().strftime('%H%M%S')}"
        else:
            name = sys.argv[2]

        genome = create_genome()
        print(f"Creating bot: {name}")
        print(f"  Movement: {genome['movement_module']}")
        print(f"  Gun: {genome['gun_module']}")
        print(f"  Radar: {genome['radar_module']}")

        if create_and_compile_bot(name, genome):
            print(f"Bot created successfully: sample.{name}")
        else:
            print("Failed to create bot")
            sys.exit(1)

    elif cmd == 'test':
        # Create a test bot
        name = "TestBot"
        genome = create_genome(
            movement="Perpendicular",
            gun="Linear",
            radar="Lock"
        )

        print("Creating test bot with:")
        print(f"  Movement: {genome['movement_module']}")
        print(f"  Gun: {genome['gun_module']}")
        print(f"  Radar: {genome['radar_module']}")

        if create_and_compile_bot(name, genome):
            print("\nBot created! Testing against sample.Walls...")

            # Import battle runner and test
            from battle_runner import run_1v1
            result = run_1v1(f"sample.{name}", "sample.Walls")
            print(json.dumps(result, indent=2))
        else:
            print("Failed to create bot")
            sys.exit(1)

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
