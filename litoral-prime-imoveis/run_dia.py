"""Launcher do runner do dia para evitar erro de import."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
from run_vendas_do_dia import run
run()
