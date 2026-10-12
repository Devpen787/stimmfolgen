"""Content-addressed source spans; no model-generated quotations or semantic labels."""
import hashlib
import json
import re
from source_probe import normalize, validate_report

VERSION = 'source-sentences-v1'

def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

def sentence_ranges(text):
    # Keep numbered AHV names (13.) and decimal numerals intact; retain attached footnotes.
    start = 0
    for match in re.finditer(r'(?<!\d)[.!?](?:[12])?(?=\s+[A-ZÄÖÜ])', text):
        end = match.end()
        if text[start:end].strip():
            yield start, end
        start = end
        while start < len(text) and text[start].isspace():
            start += 1
    if text[start:].strip():
        yield start, len(text)

def build_catalog(report, pdf_data):
    validate_report(report, pdf_data)
    if report.get('extraction_version') != 'blocks-v3':
        raise ValueError('Span catalogs require authenticated blocks-v3 source metadata')
    spans = []
    for page in report['selected_pages']:
        cursor = 0
        for block in page['raw_text_blocks']:
            text = normalize(block['raw_text'])
            offset = page['text'].find(text, cursor)
            if offset < 0:
                raise ValueError('Block does not resolve to extracted page')
            cursor = offset + len(text)
            if len(text) < 40:
                continue
            for begin, end in sentence_ranges(text):
                quote = text[begin:end]
                if len(quote) < 20:
                    continue
                identity = {'document_sha256': report['sha256'], 'extraction_version': report['extraction_version'],
                    'segmentation_version': VERSION, 'pdf_page': page['pdf_page'], 'block_number': block['block_number'],
                    'start': offset + begin, 'end': offset + end, 'text_sha256': hashlib.sha256(quote.encode()).hexdigest(),
                    'role': page['expected_role'], 'knowledge_cutoff_at': report['as_of']}
                sha = digest(identity)
                spans.append({**identity, 'span_id': 'sp-' + sha[:20], 'identity_sha256': sha,
                    'text': quote, 'bbox': [round(v, 4) for v in block['bbox']], 'page_url': page['page_url'],
                    'available_at': None, 'actor': 'COMMITTEE' if page['pdf_page'] == 14 else 'GOVERNMENT'})
    if len({s['span_id'] for s in spans}) != len(spans):
        raise ValueError('Duplicate span identifiers')
    content = {'catalog_version': VERSION, 'source_sha256': report['sha256'], 'as_of': report['as_of'],
               'public_availability_verified': False, 'spans': spans}
    return {**content, 'catalog_sha256': digest(content)}

def authenticate_catalog(catalog, report, pdf_data):
    rebuilt = build_catalog(report, pdf_data)
    if catalog != rebuilt:
        raise ValueError('Catalog content/identity does not match original PDF')
    return catalog

PREDICATES = {
    'PAYMENT_FREQUENCY': {'before': int, 'after': int},
    'ADDITIONAL_ANNUAL_COST': {'amount_chf': int, 'horizon': str},
    'FINANCING_SPECIFIED': {'value': bool},
    'BUDGET_TAX_OR_CUTS': {'value': bool},
}
KINDS = {'DIRECT_PROVISION', 'COST_PROJECTION', 'ATTRIBUTED_PREDICTION', 'UNRESOLVED'}
MISSING = {'FINANCING_METHOD', 'FINANCING_RATE', 'SOURCE_SUPPORT', 'PRE_VOTE_EVIDENCE'}

def validate_selection(answer, catalog):
    errors, checks = [], []
    if not isinstance(answer, dict):
        return {'mechanical_pass': False, 'errors': ['not_object'], 'checks': [], 'publication_state': 'WITHHELD'}
    expected_keys = {'outcome', 'claims', 'missing_facts', 'personal_financing_chf'}
    if set(answer) != expected_keys:
        errors.append('unexpected_or_missing_top_level_field')
    if answer.get('outcome') not in ('SUPPORTED', 'INSUFFICIENT_EVIDENCE', 'SOURCE_CONFLICT'):
        errors.append('invalid_outcome')
    if 'personal_financing_chf' not in answer or answer['personal_financing_chf'] is not None:
        errors.append('unsupported_personal_financing')
    missing = answer.get('missing_facts')
    if not isinstance(missing, list) or not all(isinstance(v, str) and v in MISSING for v in missing):
        errors.append('invalid_missing_facts')
    if answer.get('outcome') in ('INSUFFICIENT_EVIDENCE', 'SOURCE_CONFLICT') and not missing:
        errors.append('abstention_requires_missing_fact')
    claims = answer.get('claims')
    if not isinstance(claims, list):
        errors.append('claims_not_array')
        claims = []
    if answer.get('outcome') == 'SUPPORTED' and not claims:
        errors.append('empty_supported_answer')
    reference = {s['span_id']: s for s in catalog['spans']}
    for i, claim in enumerate(claims):
        local = []
        if not isinstance(claim, dict) or set(claim) != {'predicate', 'kind', 'actor', 'value', 'span_ids'}:
            errors.append(f'claim_{i}:invalid_fields_generated_text_is_forbidden')
            checks.append({'valid': False, 'errors': ['invalid_fields']})
            continue
        predicate = claim['predicate']
        schema = PREDICATES.get(predicate) if isinstance(predicate, str) else None
        value = claim['value']
        if schema is None or not isinstance(value, dict) or set(value) != set(schema) or any(type(value[k]) is not t for k, t in schema.items()):
            local.append('invalid_typed_proposition')
        elif predicate == 'ADDITIONAL_ANNUAL_COST' and value['horizon'] not in ('INTRODUCTION', 'FIVE_YEARS'):
            local.append('invalid_horizon')
        if not isinstance(claim['kind'], str) or claim['kind'] not in KINDS:
            local.append('invalid_kind')
        if claim['actor'] not in ('GOVERNMENT', 'COMMITTEE'):
            local.append('invalid_actor')
        ids = claim['span_ids']
        if not isinstance(ids, list) or not ids or not all(isinstance(v, str) for v in ids):
            local.append('invalid_span_references')
            ids = []
        else:
            if len(ids) != len(set(ids)):
                local.append('duplicate_span_reference')
            for span_id in ids:
                span = reference.get(span_id)
                if not span:
                    local.append('unknown_span_id')
                elif span['actor'] != claim['actor']:
                    local.append('actor_does_not_match_source')
        errors += [f'claim_{i}:{error}' for error in local]
        checks.append({'valid': not local, 'errors': local, 'span_ids': ids})
    return {'mechanical_pass': not errors, 'errors': errors, 'checks': checks,
            'publication_state': 'CANDIDATE_UNREVIEWED' if not errors else 'WITHHELD',
            'semantic_support_verified': False}

def resolve_citations(answer, catalog):
    validation = validate_selection(answer, catalog)
    if not validation['mechanical_pass']:
        return []
    reference = {s['span_id']: s for s in catalog['spans']}
    return [{'predicate': c['predicate'], 'citations': [reference[ref] for ref in c['span_ids']]} for c in answer['claims']]
