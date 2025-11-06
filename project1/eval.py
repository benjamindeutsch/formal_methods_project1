import sys
import subprocess
from pathlib import Path
from collections import Counter
import re

HERE = Path(__file__).parent
INSTANCE_DIR = HERE / "instances" / "eval_instances"
OUT_DIR = HERE / "eval_outputs"
script_path = HERE / "backbone_deutsch_12215881.py"

instances = list(INSTANCE_DIR.iterdir())

for instance_path in instances:

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
        continue

    #write output to file located OUT_DIR
    OUT_DIR.mkdir(exist_ok=True)
    out_path = OUT_DIR / f"{instance_path.stem}.out"
    out_path.write_text(completed.stdout)