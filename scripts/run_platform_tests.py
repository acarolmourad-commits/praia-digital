#!/usr/bin/env python3
"""Run only the root platform suite with external network and CRM disabled.

Dependency installation must happen before this command. The lead test uses
ASGI TestClient and writes only the synthetic QA record in the ephemeral CI
checkout. This runner never invokes deployment, publishers or production URLs.
"""
from pathlib import Path
import os
import socket
import sys
import urllib.request

ROOT=Path(__file__).resolve().parents[1]

def main():
    os.chdir(ROOT)
    for key in ['BREVO_API_KEY','BREVO_CONTACT_LIST_ID_AVALIACAO_PRATICA']:
        os.environ.pop(key,None)
    def denied(*args,**kwargs):
        raise RuntimeError('External networking is forbidden in platform tests')
    socket.socket.connect=denied
    socket.socket.connect_ex=denied
    urllib.request.urlopen=denied
    sys.path.insert(0,str(ROOT))
    import pytest
    return int(pytest.main(['-q',str(ROOT/'tests'),'-ra','-W','error::DeprecationWarning']))

if __name__=='__main__':
    raise SystemExit(main())
