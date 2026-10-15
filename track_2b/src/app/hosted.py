"""Infomaniak-only HTTPS adapter. Credentials never reach browser or traces.

Hosted identity is provider-reported, not local weight attestation. Fail closed
on a missing v1.5 model, mismatching response ID, truncation or schema failure.
"""
import hashlib
import json
import re
import time
import urllib.request
from datetime import datetime, timezone
from model_probe import parse_response

MODEL = 'swiss-ai/Apertus-v1.5-70B'
MAX_RESPONSE = 256 * 1024


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError('Inference redirects are forbidden')


class InfomaniakClient:
    def __init__(self, product_id, token):
        if not re.fullmatch(r'[1-9][0-9]{0,15}', str(product_id)) or not token or '\n' in token or '\r' in token:
            raise ValueError('Configure a valid AI Services product ID and server-side token')
        self.base_url = f'https://api.infomaniak.com/2/ai/{product_id}/openai/v1'
        self._token = token
        self._opener = urllib.request.build_opener(NoRedirect())
        models = self.request('/models')
        if not isinstance(models, dict) or not any(isinstance(m, dict) and m.get('id') == MODEL for m in models.get('data', [])):
            raise ValueError('Configured provider does not advertise the required Apertus v1.5 70B model')
        self.identity = {'backing_checkpoint': MODEL, 'v1_5_verified': True,
                         'evidence_class': 'PROVIDER_REPORTED_MODEL_ID_NOT_WEIGHT_ATTESTATION'}

    def request(self, path, payload=None):
        data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode()
        headers = {'Authorization': 'Bearer ' + self._token, 'Content-Type': 'application/json', 'User-Agent': 'StimmFolgen/0.3'}
        req = urllib.request.Request(self.base_url + path, data=data, headers=headers)
        with self._opener.open(req, timeout=120) as response:
            content = response.read(MAX_RESPONSE + 1)
            if len(content) > MAX_RESPONSE:
                raise ValueError('Provider response exceeds limit')
        return json.loads(content)

    def call(self, prompt, validator, version, max_tokens):
        if len(prompt) > 30000:
            raise ValueError('Prompt exceeds bounded evidence budget')
        payload = {'model': MODEL, 'temperature': 0, 'max_completion_tokens': max_tokens,
                   'stream': False, 'reasoning_effort': 'none',
                   'messages': [{'role': 'system', 'content': 'Answer only from supplied public evidence. No voting advice. Return JSON.'},
                                {'role': 'user', 'content': prompt}]}
        start = time.monotonic()
        raw = self.request('/chat/completions', payload)
        if not isinstance(raw, dict) or not isinstance(raw.get('choices'), list) or not raw['choices'] or not isinstance(raw['choices'][0], dict):
            raise ValueError('Malformed provider response')
        trace = {'evidence_class': 'ACTUAL_HOSTED_MODEL_ATTEMPT_UNREVIEWED',
                 'observed_at_utc': datetime.now(timezone.utc).isoformat(),
                 'model': MODEL, 'provider': 'INFOMANIAK', 'identity_basis': self.identity,
                 'raw_request': payload, 'raw_api_response': raw, 'prompt_version': version,
                 'request_sha256': hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest(),
                 'response_sha256': hashlib.sha256(json.dumps(raw, sort_keys=True).encode()).hexdigest(),
                 'latency_seconds': time.monotonic() - start, 'model_inference_performed': bool(raw.get('choices'))}
        if raw.get('model') != MODEL or raw['choices'][0].get('finish_reason') != 'stop':
            raise ValueError('Provider model mismatch or truncated completion')
        try:
            answer = parse_response(raw)
            trace.update(parsed_candidate=answer, validation=validator(answer, None, False, None))
        except (ValueError, KeyError, TypeError, IndexError):
            trace['validation'] = {'mechanical_pass': False, 'errors': ['invalid_completion']}
        return trace
