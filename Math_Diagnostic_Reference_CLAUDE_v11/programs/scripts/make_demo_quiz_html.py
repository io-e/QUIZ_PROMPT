#!/usr/bin/env python3
"""Generate a safe static HTML demonstration quiz from a small, hand-reviewed JSON specification.
Usage: python -I make_demo_quiz_html.py
This is NOT a converter from Claude v11 targets to a validated student quiz.
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from pathlib import Path
import json
import shutil

import ea_paths  # noqa: E402
ea_paths.bootstrap_sys_path()
HERE = ea_paths.data_root()
OUTPUT = ea_paths.ensure_output_dirs()

def encode(data):
    return json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')

def validate(doc):
    assert isinstance(doc.get('items'),list) and doc['items'], 'Expected a nonempty items list'
    seen=set()
    for item in doc['items']:
        assert item.get('id') not in seen, f"Duplicate item ID {item.get('id')}"
        seen.add(item['id'])
        assert item.get('question'), f"Missing question: {item['id']}"
        assert item.get('type') in ('mcq','open'), f"Invalid type: {item['id']}"
        if item['type']=='mcq':
            opts=item.get('options') or []
            assert len(opts)==4, f"{item['id']}: exactly 4 options required"
            assert len([x for x in opts if x.get('correct')])==1, f"{item['id']}: exactly one key required"
            assert len({x['text'] for x in opts})==4, f"{item['id']}: duplicate options"
            assert all(x.get('error_code') and x.get('why') for x in opts if not x.get('correct')),f"{item['id']}: distractor lacks code or explanation"
        assert item.get('solution'), f"Missing solution: {item['id']}"

def main():
    src=HERE/'quiz_demo_v11.json'
    doc=json.loads(src.read_text(encoding='utf-8'))
    validate(doc)
    html=r'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Prototype diagnostic mathématique v11</title>
<style>
*{box-sizing:border-box}body{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;background:#f2f5fa;color:#162338;margin:0}header{background:#172e4b;color:white;padding:24px max(20px,calc((100% - 840px)/2))}h1{font-size:clamp(1.5rem,4vw,2rem);margin:8px 0}main{max-width:840px;margin:auto;padding:20px}section.item{border:1px solid #d8e1e8;border-radius:12px;background:white;padding:20px;margin:18px 0}fieldset{border:0;padding:0;margin:0}legend{font-weight:700;margin-bottom:12px}.choice{display:block;border:1px solid #dee5ec;border-radius:8px;padding:10px;margin:8px 0;cursor:pointer}.choice:has(input:checked){border-color:#194f89;background:#edf4fc}.label{font-weight:650}input[type=radio]{margin-right:9px}textarea{font:inherit;width:100%;min-height:130px;border:1px solid #9cacc0;padding:12px;border-radius:7px}.confidence{margin-top:18px;border-top:1px solid #e6edf3;padding-top:14px}.confidence label{margin-right:15px}button{font:inherit;background:#194f89;color:white;border:0;border-radius:8px;padding:11px 18px;cursor:pointer}.box{padding:14px;border:1px solid #ccd8e4;background:#fff;border-radius:10px;margin:15px 0}.caution{background:#fff5df;border-left:4px solid #a46b17;padding:12px 16px}.muted{color:#536980;font-size:.88rem}.answer{border-left:3px solid #406b97;padding-left:11px;margin-top:12px}code{background:#edf2f7;padding:2px 4px}.result{font-weight:700;font-size:1.15rem}.hidden{display:none}footer{margin:28px 0;color:#5c7185;font-size:.83rem}
</style></head><body><header><div>MODE DÉMONSTRATION · HORS VALIDATION OFFICIELLE</div><h1 id="quiztitle"></h1><div>Questions de calcul et démonstration géométrique</div></header>
<main><div class="caution"><strong>Prototype technique uniquement.</strong> Les 600 lignes de la référence v11 sont sur HOLD. Ne pas utiliser ce modèle pour évaluer des élèves ni produire un diagnostic officiel. Les réponses sont traitées uniquement dans votre navigateur.</div>
<div id="items"></div><button id="submit" type="button">Afficher les corrections</button><button id="reset" type="button" style="background:#6b7787">Effacer les réponses</button><div class="box hidden" id="results" aria-live="polite"></div><footer>HTML local sans serveur, sans bibliothèque et sans transfert de données. Les codes d’erreur sont des hypothèses pédagogiques, pas des diagnostics confirmés. Les questions ouvertes nécessitent une correction humaine.</footer></main>
<script>
const quiz=__QUIZ__; const root=document.getElementById('items'); document.getElementById('quiztitle').textContent=quiz.title;
const ce=(type,text,css)=>{const e=document.createElement(type); if(text!==undefined)e.textContent=text;if(css)e.className=css;return e};
const letters=['A','B','C','D'];
for(let i=0;i<quiz.items.length;i++){
 const q=quiz.items[i], sec=ce('section',undefined,'item'); sec.id='item-'+i;
 const h=ce('div','Question '+(i+1)+' · '+q.skill_id,'muted');sec.append(h);
 if(q.type==='mcq'){
  const fs=ce('fieldset');fs.append(ce('legend',q.question));
  q.options.forEach((op,j)=>{const label=ce('label',undefined,'choice'),inp=ce('input');inp.type='radio';inp.name='q'+i;inp.value=String(j);label.append(inp,ce('span',letters[j]+'. '+op.text));fs.append(label)});
  const nsplabel=ce('label',undefined,'choice'),nsp=ce('input');nsp.type='radio';nsp.name='q'+i;nsp.value='NSP';nsplabel.append(nsp,ce('span','E. Je ne sais pas'));fs.append(nsplabel);sec.append(fs);
  const conf=ce('div',undefined,'confidence');conf.append(ce('span','Confiance : ','label'));
  for(const [v,label] of [['sure','Sûr'],['unsure','Pas sûr']]){const wrap=ce('label'),input=ce('input');input.type='radio';input.name='confidence'+i;input.value=v;wrap.append(input,ce('span',label));conf.append(wrap);}sec.append(conf);
 }else{sec.append(ce('p',q.question,'label'));const ta=ce('textarea');ta.name='open'+i;ta.setAttribute('aria-label','Votre démonstration');sec.append(ta);}
 const correction=ce('div',undefined,'answer hidden');correction.id='correction'+i;sec.append(correction);root.append(sec);
}
function selected(name){return document.querySelector('input[name="'+name+'"]:checked')?.value??'';}
function grade(){let attempted=0,correct=0,total=0,unsureCorrect=0;const outcomes=[];
 quiz.items.forEach((q,i)=>{const panel=document.getElementById('correction'+i);panel.replaceChildren(); panel.classList.remove('hidden');
  if(q.type==='mcq'){total++;const selectedIndex=selected('q'+i),conf=selected('confidence'+i);const idx=Number(selectedIndex);const valid=selectedIndex!==''&&selectedIndex!=='NSP'&&Number.isInteger(idx)&&idx>=0&&idx<4;const opt=valid?q.options[idx]:null;
   if(opt){attempted++;if(opt.correct){correct++;if(conf==='unsure')unsureCorrect++;panel.append(ce('strong','Bonne réponse.'));}else{panel.append(ce('strong','Réponse incorrecte.'));panel.append(ce('p','Hypothèse à vérifier : '+(opt.error_code||'LOCAL')+' — '+(opt.why||'')));}}
   else panel.append(ce('strong',selectedIndex==='NSP'?'Je ne sais pas sélectionné.':'Aucune réponse sélectionnée.'));
   panel.append(ce('p','Correction : '+q.solution));outcomes.push({id:q.id,reply:valid?letters[idx]:(selectedIndex||'BLANK'),confidence:conf||'',correct:!!(opt&&opt.correct)});
  }else{panel.append(ce('strong','Question ouverte : correction humaine obligatoire.'));panel.append(ce('p','Solution indicative : '+q.solution));}
 });
 const result=document.getElementById('results');result.classList.remove('hidden');result.replaceChildren();result.append(ce('div','QCM : '+correct+' / '+total+' réponses correctes','result'));result.append(ce('p','Tentatives : '+attempted+' / '+total+' · Réponses correctes avec hésitation : '+unsureCorrect+'.'));result.append(ce('p','La démonstration ouverte n’est pas notée automatiquement. Un QCM isolé ne permet pas de confirmer une difficulté.'));result.scrollIntoView({behavior:'smooth',block:'nearest'});
}
document.getElementById('submit').addEventListener('click',grade);document.getElementById('reset').addEventListener('click',()=>{document.querySelectorAll('input').forEach(x=>x.checked=false);document.querySelectorAll('textarea').forEach(x=>x.value='');document.querySelectorAll('.answer').forEach(x=>x.classList.add('hidden'));document.getElementById('results').classList.add('hidden')});
</script></body></html>'''
    html=html.replace('__QUIZ__',encode(doc))
    out = HERE / 'diagnostic_prototype_v11.html'
    out.write_text(html, encoding='utf-8', newline='\n')
    mirror = OUTPUT['demos'] / 'diagnostic_prototype_v11.html'
    shutil.copyfile(out, mirror)
    print('Generated', out, '(+ mirror', mirror, ') with', len(doc['items']), 'demo questions (UNVALIDATED)')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
