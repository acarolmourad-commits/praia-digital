"""Build the navigation for the three revised pages in an isolated preview."""
import argparse
import importlib.util
import shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('output',type=Path)
args=parser.parse_args()
preview=args.output.resolve()
if preview==ROOT: raise ValueError('Use a separate preview directory')
pages=['bairros/index.html','blog/riviera-sao-lourenco-seguranca-infraestrutura-valorizacao-2026.html','blog/estudo-rental-yield-apartamentos-1-2-dormitorios-praia-grande-2026.html','partials/header.html']
for rel in pages:
    target=preview/rel;target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ROOT/rel,target)
spec=importlib.util.spec_from_file_location('navigation',ROOT/'scripts/build-navigation.py')
nav=importlib.util.module_from_spec(spec);spec.loader.exec_module(nav)
report=nav.build(preview)
assert len(report['included'])==3,report
print(report)
