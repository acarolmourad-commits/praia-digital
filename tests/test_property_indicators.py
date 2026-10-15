import importlib.util,json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'api'))
import property_indicators as indicators
from main import app
from fastapi.testclient import TestClient
client=TestClient(app)

def payload(**kw): return {'cidade':'Santos','tipo':'Apartamento','area':70,'quartos':2,**kw}
def no_estimate(data):
    assert data['status']=='unavailable'
    assert all(data[k] is None for k in ['faixa_min','faixa_max','sugestao'])
    assert data['indicator']['value'] is None

@pytest.mark.parametrize('city',[r['city'] for r in json.loads(indicators.CONTRACT_PATH.read_text())['data']])
def test_all_contract_cities(city):
    r=client.post('/avaliar',json=payload(cidade=city));assert r.status_code==200
    d=r.json();no_estimate(d);assert d['reason']=='indicator_unavailable'
    assert d['indicator']['city']==city
    for k,v in indicators.EXPECTED.items(): assert d['indicator'][k]==v

@pytest.mark.parametrize('city',['guaruja','Praia-Grande','  SANTOS  '])
def test_city_aliases(city): assert client.post('/avaliar',json=payload(cidade=city)).json()['reason']=='indicator_unavailable'

@pytest.mark.parametrize('city',['Atlantida','Outra'])
def test_no_city_fallback(city):
    d=client.post('/avaliar',json=payload(cidade=city)).json();no_estimate(d);assert d['reason']=='unknown_city'

@pytest.mark.parametrize('kind',['Casa','Cobertura','Flat','Terreno'])
def test_no_type_multiplier(kind):
    d=client.post('/avaliar',json=payload(tipo=kind)).json();no_estimate(d);assert d['reason']=='unsupported_property_type'

@pytest.mark.parametrize('overrides',[{'area':0},{'area':-1},{'quartos':-1},{'cidade':''},{'tipo':''},{'area':1000001},{'quartos':1001}])
def test_invalid_input(overrides): assert client.post('/avaliar',json=payload(**overrides)).status_code==422

def test_finite_area_required():
    from main import AvaliacaoRequest
    from pydantic import ValidationError
    for area in [float('inf'),float('nan')]:
        with pytest.raises(ValidationError): AvaliacaoRequest(**payload(area=area))

@pytest.mark.parametrize('case',['missing','json','identity','data','duplicate','value','period','source','status','sample','nulltype'])
def test_malformed_contract_fails_closed(tmp_path,monkeypatch,case):
    good=json.loads(indicators.CONTRACT_PATH.read_text()); p=tmp_path/'indicators.json'
    if case=='json': p.write_text('{')
    elif case!='missing':
        if case=='identity': good['unit']='USD/m2'
        if case=='data': good['data']={}
        if case=='duplicate': good['data'].append(good['data'][0].copy())
        if case=='value': good['data'][0]['value']=7200
        if case=='period': good['data'][0]['period_start']='2026-01-01'
        if case=='source': good['data'][0]['source_urls']=['invented']
        if case=='status': good['status']='available'
        if case=='sample': good['data'][0]['sample_size']=10
        if case=='nulltype': good=None
        p.write_text(json.dumps(good))
    monkeypatch.setattr(indicators,'CONTRACT_PATH',p)
    d=client.post('/avaliar',json=payload()).json();no_estimate(d)
    assert d['reason']=='indicator_contract_invalid_or_missing'
