"""Bounded AHV Gate 0 release check, independent of UI and recorded pass flags."""
import hashlib
import json
from pathlib import Path
from source_spans import authenticate_catalog, digest, validate_selection
from semantic_eval import evaluate_semantics
from publication_availability import admit_frame, verify_capture
from verify_span_evidence import verify as verify_traces
from verify_semantic_review_packet import verify as verify_packet
from span_probe import TRIALS
from local_model import SUPPORTED


def human_approvals(packet, review_dir):
    bundle=json.loads((packet/'review-bundle.json').read_text())
    manifest_sha=hashlib.sha256((packet/'manifest.json').read_bytes()).hexdigest()
    accepted={}
    for item in bundle['propositions']:
        decision=json.loads((review_dir/(item['review_id']+'.json')).read_text())
        for key in ('source_sha256','catalog_sha256','semantic_reference_sha256','trace_commit'):
            if decision.get(key)!=bundle[key]:raise ValueError('Stale human review binding: '+item['review_id'])
        if (decision.get('packet_manifest_sha256')!=manifest_sha or decision.get('decision')!='ACCEPT' or
            decision.get('original_candidate')!=item['candidate'] or not isinstance(decision.get('accepted_wording'),str) or
            not decision['accepted_wording'].strip() or not decision.get('authorization_verbatim')):
            raise ValueError('Incomplete human statement approval: '+item['review_id'])
        accepted[item['review_id']]=decision
    return accepted


def verify_recorded_identity(trace):
    """Check a preserved identity against the pinned v1.5 profile; not a live runtime attestation."""
    identity=trace.get('local_identity',{})
    profile=SUPPORTED['swiss-ai/Apertus-v1.5-8B']
    expected={'model_id':profile['model_id'],'backing_checkpoint':'swiss-ai/Apertus-v1.5-8B',
              'source_revision':profile['revision'],'declared_upstream_revision':profile['declared_upstream_revision'],
              'served_alias':'default_model','v1_5_verified':True}
    if (any(identity.get(k)!=v for k,v in expected.items()) or
        identity.get('artifacts',{}).get('model.safetensors',{}).get('sha256')!=profile['weights_sha256'] or
        identity.get('quantization')!={'group_size':64,'bits':4,'mode':'affine'}):
        raise ValueError('Recorded checkpoint identity differs from pinned v1.5 conversion')


def clear_gate(pdf, evidence, packet, review_dir):
    verify_packet(packet,pdf)
    integrity=verify_traces(evidence,pdf)
    if integrity['authenticated_actual_inference_traces']!=8:raise ValueError('Expected eight genuine release completions')
    source=json.loads((evidence/'source.json').read_text())
    run=evidence/'run-release-v6'
    catalog=json.loads((run/'source-spans.json').read_text());authenticate_catalog(catalog,source,pdf)
    reference=json.loads((run/'semantic-reference-used.json').read_text())
    approval=human_approvals(packet,review_dir)
    if any(d['semantic_reference_sha256']!=digest(reference) for d in approval.values()):raise ValueError('Reviewed oracle changed')
    summary=json.loads((run/'summary.json').read_text())
    witness=json.loads((packet/'publication-availability.json').read_text())
    availability=verify_capture(pdf,pdf,pdf,witness['cdx_capture'],witness['archive_replay_headers'])
    frame=summary.get('public_case_as_of')
    if not frame or not admit_frame(availability,frame):raise ValueError('Public case frame not admitted')
    if summary.get('source_content_cutoff')!=source['editorial_cutoff']:raise ValueError('Content cutoff conflated with public frame')
    for path in run.glob('*.json'):
        trace=json.loads(path.read_text())
        if 'raw_request' not in trace:continue
        verify_recorded_identity(trace)
        if not any('PUBLIC CASE FRAME: '+str(frame) in m.get('content','') for m in trace['raw_request'].get('messages',[])):
            raise ValueError('Recorded public frame missing from actual request: '+path.name)
        if (trace.get('v1_5_verified') is not True or trace.get('model_inference_performed') is not True or
            trace.get('public_case_as_of')!=frame or trace.get('public_availability_verified') is not True or
            trace.get('source_content_cutoff')!=source['editorial_cutoff']):
            raise ValueError('Release trace identity/frame mismatch: '+path.name)
    for name,_,_,outcomes,required,missing,allowed in TRIALS[1:]:
        trace=json.loads((run/(name+'.json')).read_text());candidate=trace.get('canonical_candidate')
        mechanical=validate_selection(candidate,catalog)
        semantic=evaluate_semantics(candidate,catalog,reference,expected_outcomes=outcomes,
            required_predicates=required,required_missing=missing,allowed_predicates=allowed,
            required_values=reference['cases'][name]['required_values'])
        if not mechanical['mechanical_pass'] or not semantic['semantic_reference_pass']:
            raise ValueError('Release trial failed: '+name)
    if summary.get('bounded_machine_suite_pass') is not True:raise ValueError('Recorded machine suite failed')
    return {'gate0_status':'PASS_BOUNDED_AHV','scope':'One reviewed historical AHV case; not general policy accuracy or submission-wide readiness',
        'source_sha256':source['sha256'],'catalog_sha256':catalog['catalog_sha256'],'semantic_reference_sha256':digest(reference),
        'public_case_as_of':frame,'source_content_cutoff':source['editorial_cutoff'],
        'available_by_utc':availability['available_by_utc'],'public_availability_verified':True,
        'human_reviewed_statement_ids':sorted(approval),'raw_trials_human_approved':False,
        'machine_control_trials_pass':7,'actual_release_model_completions':8,
        'frontend_authorized_for_bounded_case':True,'current_runtime_live_inference':False,
        'approval_record_sha256':{k:hashlib.sha256((review_dir/(k+'.json')).read_bytes()).hexdigest() for k in approval}}
