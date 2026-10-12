"""Independent reference comparison for bounded propositions, not an LLM self-judge.

This module never enters the inference prompt. It is evaluation-only; human review
and source publication-date review remain distinct, required release checks.
"""
from source_spans import digest


def validate_reference(reference, catalog):
    if reference.get('source_sha256') != catalog['source_sha256'] or reference.get('knowledge_basis') != catalog['as_of']:
        raise ValueError('Reference edition/time-frame mismatch')
    for fact in reference['facts']:
        for anchor in fact['support']:
            if not any(s['pdf_page'] == anchor['pdf_page'] and s['text'] == anchor['exact_text'] and
                       s['text_sha256'] == anchor['text_sha256'] for s in catalog['spans']):
                raise ValueError('Independent semantic reference does not resolve to pinned source')
    return reference


def evaluate_semantics(answer, catalog, reference, *, expected_outcomes, required_predicates=(),
                       required_missing=(), allowed_predicates=None, required_values=None):
    validate_reference(reference, catalog)
    errors, checks = [], []
    if not isinstance(answer, dict):
        return {'semantic_reference_pass': False, 'errors': ['not_object'], 'checks': [], 'human_semantic_reviewed': False}
    if answer.get('outcome') not in expected_outcomes:
        errors.append('wrong_outcome_for_question')
    missing = answer.get('missing_facts', [])
    if not isinstance(missing, list) or not set(required_missing).issubset({x for x in missing if isinstance(x, str)}):
        errors.append('required_refusal_reason_missing')
    claims = answer.get('claims', [])
    if not isinstance(claims, list):
        errors.append('claims_not_array')
        claims = []
    observed = set()
    by_id = {s['span_id']: s for s in catalog['spans']}
    for i, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f'claim_{i}:not_object')
            continue
        predicate = claim.get('predicate')
        if isinstance(predicate, str):
            observed.add(predicate)
        candidates = [f for f in reference['facts'] if f['predicate'] == predicate and
                      f['kind'] == claim.get('kind') and f['actor'] == claim.get('actor') and
                      digest(f['value']) == digest(claim.get('value'))]
        ids = claim.get('span_ids', [])
        cited = [by_id[x] for x in ids if isinstance(x, str) and x in by_id] if isinstance(ids, list) else []
        supported = any(any(s['pdf_page'] == a['pdf_page'] and s['text'] == a['exact_text'] and
                            s['text_sha256'] == a['text_sha256'] for s in cited for a in fact['support'])
                        for fact in candidates)
        valid = bool(candidates) and supported
        if allowed_predicates is not None and predicate not in allowed_predicates:
            valid = False
        if not valid:
            errors.append(f'claim_{i}:unsupported_meaning_value_kind_actor_or_span')
        checks.append({'predicate': predicate, 'reference_match': valid})
    if not set(required_predicates).issubset(observed):
        errors.append('required_proposition_missing')
    for predicate, expected in (required_values or {}).items():
        if not any(isinstance(c, dict) and c.get('predicate') == predicate and
                   digest(c.get('value')) == digest(expected) for c in claims):
            errors.append('required_value_missing:' + predicate)
    return {'semantic_reference_pass': not errors, 'errors': errors, 'checks': checks,
            'reference_version': reference['reference_version'], 'reference_sha256': digest(reference),
            'human_semantic_reviewed': False, 'scope': reference['scope'],
            'reference_authoring': reference['authoring'], 'publication_state': 'CANDIDATE_UNREVIEWED' if not errors else 'WITHHELD'}
