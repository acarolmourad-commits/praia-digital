"""Fail-closed reader for the P0 asking-price indicator contract.

A market asking-price median is NOT an individual property appraisal. Even a
future available indicator does not authorize multiplying it into a valuation.
"""
import json
from pathlib import Path
import unicodedata

CONTRACT_PATH = Path(__file__).resolve().parents[1] / 'assets/data/property-indicators.json'
EXPECTED = {'schema_version': 1, 'metric_id': 'asking_price_m2_median_apartment',
            'metric_kind': 'asking_price', 'unit': 'BRL/m2',
            'aggregation': 'median', 'property_type': 'apartment'}


def normalized(value):
    return ' '.join(''.join(c for c in unicodedata.normalize('NFKD',value)
                            if not unicodedata.combining(c)).casefold().replace('-',' ').split())


def assessment_unavailable(city, property_type):
    result = {'status': 'unavailable', 'reason': 'valuation_model_unvalidated',
              'message': 'Avaliação indisponível: não há modelo validado de avaliação individual. Mediana de anúncios não é preço de transação nem avaliação do imóvel.',
              'faixa_min': None, 'faixa_max': None, 'sugestao': None,
              'indicator': {**EXPECTED, 'city': city, 'value': None, 'status': 'unavailable',
                            'period_start': None, 'period_end': None, 'sample_size': None,
                            'source_urls': [], 'sample_reference': None}}
    if normalized(property_type) != 'apartamento':
        result['reason'] = 'unsupported_property_type'
        return result
    try:
        contract = json.loads(CONTRACT_PATH.read_text(encoding='utf-8'))
        if not isinstance(contract,dict) or any(type(contract.get(k)) is not type(v) or contract.get(k)!=v for k,v in EXPECTED.items()):
            raise ValueError('contract identity mismatch')
        if contract.get('status') != 'unavailable' or not isinstance(contract.get('data'),list):
            raise ValueError('contract status is not approved by P0')
        rows=contract['data']
        names=[]
        for row in rows:
            if not isinstance(row,dict) or not isinstance(row.get('city'),str) or not row['city'].strip():
                raise ValueError('invalid city')
            names.append(normalized(row['city']))
            # P0 approved state is strictly unavailable; never leak unverified values.
            if (row.get('status')!='unavailable' or row.get('value','missing') is not None
                or row.get('period_start','missing') is not None or row.get('period_end','missing') is not None
                or row.get('sample_size','missing') is not None or row.get('source_urls')!=[]
                or row.get('sample_reference','missing') is not None):
                raise ValueError('invalid unavailable record')
        if len(names)!=len(set(names)) or not names:
            raise ValueError('duplicate or empty cities')
        matches=[row for row in rows if normalized(row['city'])==normalized(city)]
        if not matches:
            result['reason']='unknown_city'
            return result
        result['indicator'].update(matches[0])
        result['reason']='indicator_unavailable'
        return result
    except (OSError, ValueError, TypeError, KeyError):
        result['reason']='indicator_contract_invalid_or_missing'
        return result
