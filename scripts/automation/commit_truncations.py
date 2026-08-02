#!/usr/bin/env python3
import subprocess
import os

os.chdir('C:/Users/Carolina/praia-digital')

# Unstage everything
subprocess.run(['git', 'reset', 'HEAD'], check=True)

# Get all modified files
result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True, check=True)
files = []
for line in result.stdout.strip().split('\n'):
    if line.startswith(' M '):
        files.append(line[4:])

print(f"Total modified files: {len(files)}")

# Commit in batches of 10
batch_size = 10
for i in range(0, len(files), batch_size):
    batch = files[i:i+batch_size]
    subprocess.run(['git', 'add'] + batch, check=True)
    msg = f"fix: truncate long titles and meta descriptions (batch {i//batch_size + 1})"
    result = subprocess.run(['git', 'commit', '-m', msg], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✓ Batch {i//batch_size + 1}: committed {len(batch)} files")
    else:
        print(f"✗ Batch {i//batch_size + 1} failed: {result.stderr[:200]}")

print("Done")
