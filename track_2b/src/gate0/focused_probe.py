#!/usr/bin/env python3
"""Template-guided development probes, not independent classification/refusal accuracy."""
import argparse
import json
from pathlib import Path
from model_probe import run_inference

TRIALS = (
    ('provision',9,'DIRECT_PROVISION','SUPPORTED','Was verlangt die Initiative bezüglich der Anzahl jährlicher AHV-Altersrentenauszahlungen?'),
    ('projection',11,'COST_PROJECTION','SUPPORTED','Welche zusätzlichen jährlichen Kosten werden bei Einführung prognostiziert? Ein Kostenvoranschlag ist hier eine belegbare Prognose, keine sichere Zukunft.'),
    ('refusal',11,'UNRESOLVED','INSUFFICIENT_EVIDENCE','Welchen exakten zusätzlichen CHF-Jahresbetrag müsste eine angestellte Person definitiv bezahlen? Verweigere eine Zahl, wenn die Finanzierungsformel nicht beschlossen ist.'),
)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-report', type=Path, required=True)
    parser.add_argument('--source-pdf', type=Path, required=True)
    parser.add_argument('--local-model-report', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    report=json.loads(args.source_report.read_text())
    identity=json.loads(args.local_model_report.read_text())
    pdf=args.source_pdf.read_bytes()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    all_valid=True
    for name,page,kind,outcome,task in TRIALS:
        source=next(p for p in report['selected_pages'] if p['pdf_page']==page)
        shape={'outcome':outcome,'claims':[{'kind':kind,'statement':'','pdf_page':page,'quote':'','attribution':source['expected_role'],'as_of':'2023-11-29'}],'unknowns':[],'personal_financing_chf':None}
        prompt=('Arbeite nur mit der Quelle unten, Wissensstand 29.11.2023. '+task+'\nFülle ausschließlich die beiden leeren Strings statement und quote im folgenden JSON aus. statement muss den Quellensatz sinngemäß richtig wiedergeben. quote muss GENAU EINEN kurzen zusammenhängenden Satz wortgetreu aus der Quelle kopieren. Nicht zwei getrennte Sätze zusammenkleben! Ergänze unknowns nur um konkrete Wissenslücken. Die übrigen Metadaten und null bleiben unverändert. SUPPORTED bedeutet, dass der Text die Aussage macht; eine Prognose bleibt eine Prognose, keine Garantie. Keine Abstimmungsempfehlung. Nur JSON, keine Einleitung.\n'+json.dumps(shape,ensure_ascii=False)+'\nQUELLE, PDF Seite '+str(page)+'\n'+source['text'])
        print('Running focused v1.5 trial',name,flush=True)
        result=run_inference(report,identity['served_alias'],identity['base_url'],'',local_identity=identity,prompt=prompt,require_coverage=False,expected_outcome=outcome,max_tokens=400,source_pdf_data=pdf)
        result['prompt_version']='gate0-v4-single-page-template'
        result['trial_id']=name
        result['prompt_limit']='Metadata/kind/outcome supplied in template; not independent classification, attribution selection or model refusal-choice accuracy'
        (args.out_dir/(name+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        passed=result.get('validation',{}).get('mechanical_pass',False)
        all_valid=all_valid and passed
        print(json.dumps({'trial':name,'mechanical_pass':passed}),flush=True)
    raise SystemExit(0 if all_valid else 2)

if __name__=='__main__':
    main()
