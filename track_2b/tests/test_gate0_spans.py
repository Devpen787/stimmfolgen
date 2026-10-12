"""Synthetic adversarial controls; no mocked answer is reported as actual inference."""
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src/gate0'))
import source_spans
import semantic_eval
import span_probe

class SpanProtocolTests(unittest.TestCase):
    def setUp(self):
        self.span={'span_id':'sp-fixture', 'identity_sha256':'fixture-only', 'pdf_page':9,
            'text':'Die Initiative fordert 13 statt 12 jährliche Zahlungen.',
            'text_sha256':hashlib.sha256('Die Initiative fordert 13 statt 12 jährliche Zahlungen.'.encode()).hexdigest(),
            'actor':'GOVERNMENT'}
        self.catalog={'source_sha256':'synthetic-only','as_of':'2023-11-29','spans':[self.span]}
        self.claim={'predicate':'PAYMENT_FREQUENCY','kind':'DIRECT_PROVISION','actor':'GOVERNMENT',
            'value':{'before':12,'after':13},'span_ids':['sp-fixture']}
        self.answer={'outcome':'SUPPORTED','claims':[self.claim],'missing_facts':[],'personal_financing_chf':None}
        self.reference={'reference_version':'unit-only','source_sha256':'synthetic-only','knowledge_basis':'2023-11-29',
            'authoring':'Synthetic test fixture, not human ground truth','scope':'unit fixture',
            'facts':[{'predicate':'PAYMENT_FREQUENCY','kind':'DIRECT_PROVISION','actor':'GOVERNMENT',
                'value':{'before':12,'after':13},'support':[{'pdf_page':9,'exact_text':self.span['text'],'text_sha256':self.span['text_sha256']}]}]}

    def semantics(self,answer=None,**kwargs):
        return semantic_eval.evaluate_semantics(answer or self.answer,self.catalog,self.reference,
            expected_outcomes=('SUPPORTED',),required_predicates=('PAYMENT_FREQUENCY',),**kwargs)

    def test_exact_source_text_resolved_without_generated_quote(self):
        resolved=source_spans.resolve_citations(self.answer,self.catalog)
        self.assertEqual(resolved[0]['citations'][0]['text'],self.span['text'])
        self.assertNotIn('quote',self.claim)

    def test_unknown_span_rejected(self):
        self.claim['span_ids']=['sp-invented']
        self.assertFalse(source_spans.validate_selection(self.answer,self.catalog)['mechanical_pass'])
        self.assertEqual(source_spans.resolve_citations(self.answer,self.catalog),[])

    def test_generated_quote_and_narrative_forbidden(self):
        for field in ('quote','statement','pdf_page','as_of'):
            with self.subTest(field=field):
                a=copy.deepcopy(self.answer);a['claims'][0][field]='invented'
                self.assertFalse(source_spans.validate_selection(a,self.catalog)['mechanical_pass'])

    def test_real_span_does_not_prove_reversed_meaning(self):
        self.claim['value']={'before':13,'after':12}
        self.assertTrue(source_spans.validate_selection(self.answer,self.catalog)['mechanical_pass'])
        self.assertFalse(self.semantics()['semantic_reference_pass'])

    def test_kind_promoting_prediction_to_provision_rejected(self):
        self.claim['kind']='COST_PROJECTION'
        self.assertTrue(source_spans.validate_selection(self.answer,self.catalog)['mechanical_pass'])
        self.assertFalse(self.semantics()['semantic_reference_pass'])

    def test_wrong_actor_rejected_even_with_valid_span(self):
        self.claim['actor']='COMMITTEE'
        self.assertFalse(source_spans.validate_selection(self.answer,self.catalog)['mechanical_pass'])
        self.assertFalse(self.semantics()['semantic_reference_pass'])

    def test_topically_related_committee_span_does_not_support_government_budget_forecast(self):
        self.span.update(actor='COMMITTEE')
        self.claim.update(predicate='BUDGET_TAX_OR_CUTS',kind='ATTRIBUTED_PREDICTION',actor='COMMITTEE',value={'value':True})
        self.assertTrue(source_spans.validate_selection(self.answer,self.catalog)['mechanical_pass'])
        self.assertFalse(self.semantics()['semantic_reference_pass'])

    def test_wrong_cost_horizon_and_amount_rejected(self):
        fact=self.reference['facts'][0]
        fact.update(predicate='ADDITIONAL_ANNUAL_COST',kind='COST_PROJECTION',value={'amount_chf':4100000000,'horizon':'INTRODUCTION'})
        self.claim.update(predicate='ADDITIONAL_ANNUAL_COST',kind='COST_PROJECTION',value={'amount_chf':5000000000,'horizon':'INTRODUCTION'})
        r=semantic_eval.evaluate_semantics(self.answer,self.catalog,self.reference,expected_outcomes=('SUPPORTED',))
        self.assertFalse(r['semantic_reference_pass'])
        self.claim['value']={'amount_chf':4100000000,'horizon':'FIVE_YEARS'}
        self.assertFalse(semantic_eval.evaluate_semantics(self.answer,self.catalog,self.reference,expected_outcomes=('SUPPORTED',))['semantic_reference_pass'])

    def test_supported_later_horizon_cannot_answer_introduction_question(self):
        self.reference['facts'][0].update(predicate='ADDITIONAL_ANNUAL_COST',kind='COST_PROJECTION',value={'amount_chf':5000000000,'horizon':'FIVE_YEARS'})
        self.claim.update(predicate='ADDITIONAL_ANNUAL_COST',kind='COST_PROJECTION',value={'amount_chf':5000000000,'horizon':'FIVE_YEARS'})
        r=semantic_eval.evaluate_semantics(self.answer,self.catalog,self.reference,expected_outcomes=('SUPPORTED',),
            required_values={'ADDITIONAL_ANNUAL_COST':{'amount_chf':4100000000,'horizon':'INTRODUCTION'}})
        self.assertFalse(r['semantic_reference_pass'])

    def test_abstention_has_typed_reason_and_financing_citation(self):
        self.answer.update(outcome='INSUFFICIENT_EVIDENCE',missing_facts=['FINANCING_METHOD','FINANCING_RATE'])
        self.assertTrue(source_spans.validate_selection(self.answer,self.catalog)['mechanical_pass'])
        self.answer['missing_facts']=[]
        self.assertFalse(source_spans.validate_selection(self.answer,self.catalog)['mechanical_pass'])

    def test_zero_is_not_unknown_personal_financing(self):
        self.answer['personal_financing_chf']=0
        self.assertFalse(source_spans.validate_selection(self.answer,self.catalog)['mechanical_pass'])

    def test_numeric_boolean_confusion_is_rejected_independently(self):
        self.reference['facts'][0].update(predicate='FINANCING_SPECIFIED',kind='UNRESOLVED',value={'value':False})
        self.claim.update(predicate='FINANCING_SPECIFIED',kind='UNRESOLVED',value={'value':0})
        r=semantic_eval.evaluate_semantics(self.answer,self.catalog,self.reference,expected_outcomes=('SUPPORTED',))
        self.assertFalse(r['semantic_reference_pass'])
        self.assertFalse(source_spans.validate_selection(self.answer,self.catalog)['mechanical_pass'])

    def test_mutated_reference_source_fails_closed(self):
        self.reference['facts'][0]['support'][0]['exact_text']='Employees must pay CHF 100'
        with self.assertRaises(ValueError):self.semantics()

    def test_future_reference_frame_fails_closed(self):
        self.reference['knowledge_basis']='2026-10-12'
        with self.assertRaises(ValueError):self.semantics()

    def test_valid_reference_still_not_human_reviewed(self):
        r=self.semantics()
        self.assertTrue(r['semantic_reference_pass'])
        self.assertFalse(r['human_semantic_reviewed'])
        self.assertEqual(r['publication_state'],'CANDIDATE_UNREVIEWED')

    def test_malformed_candidates_do_not_crash(self):
        for a in (None,[],{}, {'claims':[{'predicate':[],'kind':{},'actor':[],'value':[],'span_ids':[{}]}]},
                  {'claims':[None]}, {'claims':'not-list'}):
            with self.subTest(candidate=a):
                self.assertFalse(source_spans.validate_selection(a,self.catalog)['mechanical_pass'])

    def test_flat_adapter_preserves_wrong_counts_for_independent_rejection(self):
        raw={'outcome':'SUPPORTED','span_ids':['sp-fixture'],'current_payments':13,'proposed_payments':12}
        candidate=span_probe.adapt_answer(raw,self.catalog,'PAYMENT_FREQUENCY','direct_provision')
        self.assertEqual(candidate['claims'][0]['value'],{'before':13,'after':12})
        self.assertFalse(self.semantics(candidate)['semantic_reference_pass'])

    def test_flat_adapter_does_not_repair_money_units_or_extra_fields(self):
        raw={'outcome':'SUPPORTED','span_ids':['sp-fixture'],'amount_chf':4.1,'horizon':'INTRODUCTION'}
        candidate=span_probe.adapt_answer(raw,self.catalog,'ADDITIONAL_ANNUAL_COST','cost_projection')
        self.assertEqual(candidate['claims'][0]['value']['amount_chf'],4.1)
        self.assertFalse(source_spans.validate_selection(candidate,self.catalog)['mechanical_pass'])
        raw['quote']='invented'
        self.assertIsNone(span_probe.adapt_answer(raw,self.catalog,'ADDITIONAL_ANNUAL_COST','cost_projection'))

    def test_adapter_keeps_unknown_or_mixed_source_attribution_withheld(self):
        raw={'outcome':'SUPPORTED','span_ids':['sp-invented'],'current_payments':12,'proposed_payments':13}
        candidate=span_probe.adapt_answer(raw,self.catalog,'PAYMENT_FREQUENCY','direct_provision')
        self.assertIsNone(candidate['claims'][0]['actor'])
        self.assertFalse(source_spans.validate_selection(candidate,self.catalog)['mechanical_pass'])

    def test_budget_adapter_never_corrects_model_actor_to_reference(self):
        self.span['actor']='COMMITTEE'
        raw={'outcome':'SOURCE_CONFLICT','span_ids':['sp-fixture'],'actor':'COMMITTEE'}
        candidate=span_probe.adapt_answer(raw,self.catalog,'BUDGET_TAX_OR_CUTS','actor_mixup')
        self.assertEqual(candidate['claims'][0]['actor'],'COMMITTEE')
        self.assertTrue(source_spans.validate_selection(candidate,self.catalog)['mechanical_pass'])
        self.assertFalse(semantic_eval.evaluate_semantics(candidate,self.catalog,self.reference,
            expected_outcomes=('SOURCE_CONFLICT',))['semantic_reference_pass'])

    def test_neutral_attribution_uses_source_actor_not_a_fixed_government_answer(self):
        for actor in ('GOVERNMENT','COMMITTEE'):
            with self.subTest(actor=actor):
                self.span['actor']=actor
                self.assertTrue(span_probe.validate_attribution({'span_ids':['sp-fixture'],'actor':actor},
                    self.catalog,'BUDGET_TAX_OR_CUTS')['mechanical_pass'])
                other='COMMITTEE' if actor=='GOVERNMENT' else 'GOVERNMENT'
                self.assertFalse(span_probe.validate_attribution({'span_ids':['sp-fixture'],'actor':other},
                    self.catalog,'BUDGET_TAX_OR_CUTS')['mechanical_pass'])

    def test_neutral_prompt_contains_both_speakers_and_no_user_premise_or_oracle(self):
        c={'as_of':'2023-11-29','spans':[
            {'span_id':'sp-neutral-a','actor':'COMMITTEE','pdf_page':14,'text':'Steuern steigen nach unserer Prognose.'},
            {'span_id':'sp-neutral-b','actor':'GOVERNMENT','pdf_page':16,'text':'Der Bund kann Ausgaben kürzen.'}]}
        text=span_probe.attribution_prompt(c,[14,16],'BUDGET_TAX_OR_CUTS')
        self.assertIn('sp-neutral-a',text);self.assertIn('sp-neutral-b',text)
        self.assertNotIn('Attribute this budget forecast to the committee',text)
        self.assertNotIn('semantic_reference',text)
        self.assertNotIn('sp-92f4ef4f294b8ca65441',text)
        c['spans'][0]['actor']='GOVERNMENT';c['spans'][1]['actor']='COMMITTEE'
        swapped=span_probe.attribution_prompt(c,[14,16],'BUDGET_TAX_OR_CUTS')
        self.assertNotEqual(text,swapped)
        self.assertIn('"actor": "COMMITTEE", "text": "Der Bund',swapped)

    def test_neutral_grounding_cannot_admit_unknown_ids_empty_or_mixed_actors(self):
        other=copy.deepcopy(self.span);other.update(span_id='sp-other',actor='COMMITTEE')
        self.catalog['spans'].append(other)
        for raw in ({'span_ids':[],'actor':None},{'span_ids':['sp-invented'],'actor':'GOVERNMENT'},
                    {'span_ids':['sp-fixture','sp-other'],'actor':'GOVERNMENT'},
                    {'span_ids':['sp-fixture'],'actor':'GOVERNMENT','quote':'made up'}):
            with self.subTest(raw=raw):
                self.assertFalse(span_probe.validate_attribution(raw,self.catalog,'BUDGET_TAX_OR_CUTS')['mechanical_pass'])

    def test_actor_comparison_handles_both_actors_without_fixed_expected_answer(self):
        for actual in ('GOVERNMENT','COMMITTEE'):
            for requested in ('GOVERNMENT','COMMITTEE'):
                with self.subTest(actual=actual,requested=requested):
                    self.span['actor']=actual
                    raw={'actor':actual,'span_ids':['sp-fixture']}
                    answer=span_probe.compare_attribution(raw,{'claimed_actor':requested},self.catalog,'BUDGET_TAX_OR_CUTS')
                    self.assertEqual(answer['outcome'],'SUPPORTED' if actual==requested else 'SOURCE_CONFLICT')
                    self.assertEqual(answer['actor'],actual)
                    self.assertEqual(answer['span_ids'],raw['span_ids'])

    def test_actor_comparison_withholds_unknown_intent_and_invalid_grounding(self):
        grounding={'actor':'GOVERNMENT','span_ids':['sp-fixture']}
        for intent in (None,{}, {'claimed_actor':None},{'claimed_actor':['COMMITTEE']},
                       {'claimed_actor':'COMMITTEE','answer':'GOVERNMENT'}):
            self.assertIsNone(span_probe.compare_attribution(grounding,intent,self.catalog,'BUDGET_TAX_OR_CUTS'))
        self.assertIsNone(span_probe.compare_attribution({'actor':'COMMITTEE','span_ids':['sp-fixture']},
            {'claimed_actor':'COMMITTEE'},self.catalog,'BUDGET_TAX_OR_CUTS'))

    def test_valid_actor_comparison_still_fails_independent_meaning_for_unrelated_span(self):
        raw=span_probe.compare_attribution({'actor':'GOVERNMENT','span_ids':['sp-fixture']},
            {'claimed_actor':'COMMITTEE'},self.catalog,'BUDGET_TAX_OR_CUTS')
        candidate=span_probe.adapt_answer(raw,self.catalog,'BUDGET_TAX_OR_CUTS','actor_mixup')
        self.assertTrue(source_spans.validate_selection(candidate,self.catalog)['mechanical_pass'])
        self.assertFalse(semantic_eval.evaluate_semantics(candidate,self.catalog,self.reference,
            expected_outcomes=('SOURCE_CONFLICT',))['semantic_reference_pass'])

    def test_sentence_ranges_do_not_split_13th_or_decimal(self):
        text='Die 13. AHV-Rente kostet 4,1 Milliarden Franken.2 Davon trägt der Bund einen Anteil.'
        parts=[text[a:b] for a,b in source_spans.sentence_ranges(text)]
        self.assertEqual(parts[0],'Die 13. AHV-Rente kostet 4,1 Milliarden Franken.2')
        self.assertEqual(len(parts),2)

    def test_catalog_is_deterministic_and_mutations_reauthenticate_against_pdf(self):
        text='Die Initiative fordert 13 statt 12 jährliche Zahlungen.'
        report={'sha256':'fixture-only','as_of':'2023-11-29','extraction_version':'blocks-v3','selected_pages':[
            {'pdf_page':9,'expected_role':'FEDERAL_COUNCIL_DETAIL','page_url':'https://example.invalid/#page=9','text':text,
             'raw_text_blocks':[{'block_number':1,'raw_text':text,'bbox':[100,0,300,40]}]}]}
        with mock.patch.object(source_spans,'validate_report'):
            c=source_spans.build_catalog(report,b'fixture')
            self.assertEqual(c,source_spans.build_catalog(report,b'fixture'))
            c['spans'][0]['text']='An invented quotation'
            with self.assertRaises(ValueError):source_spans.authenticate_catalog(c,report,b'fixture')
            original=source_spans.build_catalog(report,b'fixture')
            report['as_of']='2026-10-12'
            changed=source_spans.build_catalog(report,b'fixture')
            self.assertNotEqual(original['spans'][0]['span_id'],changed['spans'][0]['span_id'])

if __name__=='__main__':unittest.main()
