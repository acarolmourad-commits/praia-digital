#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wrapper de compatibilidade: content_loop -> content_engine.
"""
import subprocess
import sys
from pathlib import Path

REPO = Path('.').resolve()
result = subprocess.run(
    [sys.executable, 'scripts/automation/content_engine.py'] + sys.argv[1:],
    cwd=REPO
)
sys.exit(result.returncode)
