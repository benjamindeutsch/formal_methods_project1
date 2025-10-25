# python
import sys
import subprocess
from pathlib import Path
from collections import Counter
import re

HERE = Path(__file__).parent
INSTANCE_DIR = HERE / "instances" / "test_instances"
SOLUTION_DIR = HERE / "instances" / "test_solutions"

def _gather_pairs():
    pairs = []
    if not INSTANCE_DIR.exists():
        print(f"Instance directory {INSTANCE_DIR} does not exist.")
        return pairs
    for inst in sorted(INSTANCE_DIR.iterdir()):
        if not inst.is_file():
            continue
        sol = SOLUTION_DIR / (inst.stem + ".out")
        if not sol.exists():
            continue
        pairs.append((inst, sol))
    return pairs

TEST_PAIRS = _gather_pairs()

def _tokenize(text: str):
    return re.findall(r'\S+', text or "")

def test_backbone_outputs_match(instance_path: Path, solution_path: Path):
    script_path = HERE / "backbone_deutsch_12215881.py"
    assert script_path.exists(), f"Script not found at {script_path}"

    print(f"Testing instance: {instance_path.name}")

    completed = subprocess.run(
        [sys.executable, str(script_path), str(instance_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    print(f"Return code: {completed.returncode}")

    if completed.returncode != 0:
        print(f"Script failed with return code {completed.returncode}")
        print(f"STDERR:\n{completed.stderr}")
        return

    actual_text = completed.stdout

    expected_text = solution_path.read_text()

    actual_tokens = _tokenize(actual_text)
    expected_tokens = _tokenize(expected_text)

    actual_counter = Counter(actual_tokens)
    expected_counter = Counter(expected_tokens)

    if(dict(actual_counter)==dict(expected_counter)):
        print(f"Test passed for instance {instance_path.name}")
    else:
        print(f"Test failed for instance {instance_path.name}")
        print("Expected tokens and counts:")
        for token, count in expected_counter.items():
            print(f"{token}: {count}")
        print("Actual tokens and counts:")
        for token, count in actual_counter.items():
            print(f"{token}: {count}")

for instance_path, solution_path in TEST_PAIRS:
    test_backbone_outputs_match(instance_path, solution_path)