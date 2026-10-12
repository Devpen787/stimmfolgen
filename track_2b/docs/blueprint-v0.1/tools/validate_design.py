#!/usr/bin/env python3
"""Verify authored schemas / synthetic fixture / simple foreign keys.
NOT a model eval, app test, cryptographic audit, or evidence validation."""
from pathlib import Path
import json, sys
from jsonschema import Draft202012Validator, FormatChecker
p=Path(__file__).resolve().parents[1]
schema=json.loads((p/'schemas/public_case.schema.json').read_text())
private=json.loads((p/'schemas/private_vault.schema.json').read_text())
fixture=json.loads((p/'fixtures/synthetic_case.json').read_text())
for x in [schema,private]: Draft202012Validator.check_schema(x)
Draft202012Validator(schema,format_checker=FormatChecker()).validate(fixture)
proposal=fixture['proposal']['id'];docs={x['id'] for x in fixture['documents']};spans={x['id'] for x in fixture['source_spans']};uncertainties={x['id'] for x in fixture['uncertainties']}
assert all(x['document_id'] in docs for x in fixture['source_spans'])
assert all(x['proposal_id']==proposal for x in fixture['impacts'])
assert all(set(x['source_span_ids']) <= spans and set(x['uncertainty_ids']) <= uncertainties for x in fixture['impacts'])
assert fixture['generated_by']['apertus_inference_verified'] is False
print('PASS: structural JSON schemas, synthetic fixture, and referenced IDs.')
print('NOT TESTED: Apertus, real referendums, semantic source support, UI, privacy security.')
