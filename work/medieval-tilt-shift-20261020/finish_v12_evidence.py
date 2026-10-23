"""Wait for the existing encoder, then extract current encoded evidence."""
from pathlib import Path
import subprocess
import sys
import time

root = Path(__file__).resolve().parent
report = root / 'delivery/engineering-check-v12.json'
start = time.time()
print('Waiting for encode/decode report', flush=True)
while not report.exists():
    if time.time() - start > 1800:
        raise TimeoutError('No completed encoding report after 30 minutes')
    time.sleep(5)
subprocess.run([sys.executable, '-X', 'utf8', str(root / 'finalize_delivery_v12.py')], check=True)
