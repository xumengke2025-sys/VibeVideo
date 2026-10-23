"""Resume frozen production inputs with fault-tolerant process telemetry.

Only inventory errors are caught. Render/encode errors still stop for inspection.
This launcher deliberately lives outside the frozen rendering source directory.
"""
import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('snow_film_pipeline', ROOT / 'src/film_pipeline.py')
pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline)

original_inventory = pipeline.blender_pids
def safe_inventory():
    try:
        return original_inventory()
    except subprocess.TimeoutExpired:
        print('Process inventory timed out; render ownership remains with GPU queue.', flush=True)
        return []
pipeline.blender_pids = safe_inventory

parser = argparse.ArgumentParser()
parser.add_argument('--wait-pid', type=int)
parser.add_argument('mode', choices=['sample', 'full'])
args = parser.parse_args()
if args.wait_pid:
    while pipeline.alive(args.wait_pid):
        print(f'Waiting for existing owned queue PID {args.wait_pid}', flush=True)
        time.sleep(30)
sys.argv = [str(ROOT / 'src/film_pipeline.py'), args.mode,
            '--version', 'film-v8', '--engine', 'EEVEE', '--samples', '64', '--batch-size', '12']
pipeline.main()
