#!/usr/bin/env python3
"""Build a stand-alone, read-only HTML dashboard from v11 validation outputs.

Usage: python -I v11_html_dashboard.py
Place alongside validation_report_v11.json and Item_Release_Eligibility_v11.csv.
This script DOES NOT run validation, approve content, or change release statuses.
"""
import csv
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def read_csv(name):
    with (HERE / name).open('r', encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))

def js_json(v):
    return json.dumps(v, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')

def main():
    report = json.loads((HERE / 'validation_report_v11.json').read_text(encoding='utf-8'))
    rows = read_csv('Item_Release_Eligibility_v11.csv')
    gaps = read_csv('Coverage_Gaps_v11.csv')
    info = {'status':report.get('status'), 'blocking':report.get('blocking_findings'),
            'gates':report.get('gates',{}), 'release':report.get('release_status',{}),
            'elig':report.get('item_eligibility',{}), 'coverage':report.get('coverage',{}),
            'environment':report.get('environment',{}),'count':len(rows),'gaps_count':len(gaps),
            'summary':report.get('summary','')}
    document = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Math Diagnostic v11 — Local Validation Dashboard</title>
<style>
:root{color-scheme:light;font-family:system-ui,-apple-system,"Segoe UI",sans-serif;line-height:1.4;color:#12253c;background:#f3f6fa}
*{box-sizing:border-box} body{margin:0} header{background:#10253f;color:#fff;padding:2rem max(24px,calc((100% - 1160px)/2))} h1{margin:.2rem 0;font-size:clamp(1.6rem,4vw,2.4rem)}h2{font-size:1.15rem;margin:0 0 .8rem}p{margin:.45rem 0}.sub{color:#c8d5e1}
main{max-width:1160px;margin:auto;padding:24px}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}.card{border:1px solid #dce3ea;border-radius:12px;background:#fff;padding:16px}.big{font-size:1.85rem;font-weight:760;font-variant-numeric:tabular-nums}.label{font-size:.83rem;color:#4e647c}.warn{border-left:4px solid #aa692c;padding:14px 18px;background:#fff8eb;border-radius:6px;margin:20px 0}.panel{background:white;border:1px solid #dce3ea;border-radius:12px;margin:18px 0;padding:20px}.gates{display:grid;grid-template-columns:repeat(auto-fit,minmax(245px,1fr));gap:8px}.gate{border:1px solid #dbe3eb;padding:11px 12px;border-radius:8px;display:flex;justify-content:space-between;gap:16px}.status{font-size:.76rem;font-weight:750;letter-spacing:.02em;border-radius:4px;padding:3px 7px;background:#e7edf2}.pass{color:#176044;background:#d9f2e3}.hold{color:#965313;background:#fff1d5}.fail{color:#a12b36;background:#ffe4e4}.unverified,.partial{color:#705599;background:#f0e9fc}
.toolbar{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-bottom:12px}.toolbar input,.toolbar select{font:inherit;padding:10px;border-radius:6px;border:1px solid #aab7c7;max-width:100%;background:white}.toolbar input{flex:2;min-width:200px}.toolbar select{flex:1;min-width:140px} button{font:inherit;border:1px solid #7790ad;background:#fff;border-radius:6px;padding:9px 12px;cursor:pointer}button:hover{background:#eff5fa}.wraptable{overflow-x:auto;max-height:535px;border:1px solid #e0e5ea;border-radius:8px}table{border-collapse:collapse;width:100%;font-size:.86rem}thead{position:sticky;top:0;background:#eff3f7;z-index:1}th,td{padding:9px 11px;text-align:left;border-bottom:1px solid #e5eaf0;vertical-align:top}td.reason{min-width:420px;max-width:690px}code{font-size:.87em;background:#eff3f6;border-radius:4px;padding:2px 4px}footer{font-size:.83rem;color:#526478;margin:25px 0 40px}a{color:#175ba0}
</style></head><body>
<header><p class="sub">LOCAL REPORT · STATIC HTML · NO NETWORK</p><h1>Math Diagnostic v11</h1><p class="sub">Validation results and row-by-row release eligibility</p></header>
<main>
<div class="warn"><strong>Not approved for student release.</strong> Structural checks do not verify teaching quality, official programme extracts, student responses or player compatibility. HTML displays the last run; it does not execute Python tests.</div>
<section class="cards" id="summary" aria-label="Validation summary"></section>
<section class="panel"><h2>Release gates</h2><div id="gates" class="gates"></div><p class="label" style="margin-top:14px" id="release"></p></section>
<section class="panel"><h2>Item eligibility</h2><div class="toolbar"><input id="rowsearch" type="search" placeholder="Filter by target ID or reason" aria-label="Search items"><select id="statusfilter" aria-label="Filter by paper status"><option value="">All paper statuses</option><option>PASS</option><option>HOLD</option><option>FAIL</option></select><button id="rowexport" type="button">Export filtered CSV</button></div><p class="label" id="rowcount"></p><div class="wraptable"><table><thead><tr><th>Target</th><th>Paper</th><th>Digital</th><th>Calculation</th><th>Curriculum</th><th>Teacher</th><th>Diagnostic</th><th>Reason</th></tr></thead><tbody id="rows"></tbody></table></div></section>
<section class="panel"><h2>Open validation gaps</h2><div class="toolbar"><input id="gapsearch" type="search" placeholder="Filter by ID, value or gap" aria-label="Search gaps"><select id="gapfilter" aria-label="Filter by gap type"><option value="">All gap types</option></select><button id="gapexport" type="button">Export filtered gaps</button></div><p class="label" id="gapcount"></p><div class="wraptable"><table><thead><tr><th>ID</th><th>Field</th><th>Seed</th><th>Value</th><th>Gap type</th></tr></thead><tbody id="gaps"></tbody></table></div></section>
<footer>Generated from the files in the extracted Claude v11 package. No data is transmitted. A new validation run requires the Python scripts, then regenerating this page. Source environment: <span id="env"></span>.</footer>
</main>
<script>
const INFO=__INFO__; const ROWS=__ROWS__; const GAPS=__GAPS__;
const $=id=>document.getElementById(id);
const el=(tag,txt,cls)=>{const n=document.createElement(tag); if(txt!==undefined)n.textContent=String(txt); if(cls)n.className=cls;return n;};
const state=s=>{const v=String(s||'UNKNOWN');const span=el('span',v,'status '+v.toLowerCase().replace(/[^a-z]/g,''));return span;};
const cell=(tr,text,tag='td')=>{const td=el(tag,text);tr.appendChild(td);return td;};
function card(label, value){const c=el('div',undefined,'card'); c.append(el('div',value,'big'),el('div',label,'label'));$('summary').appendChild(c);}
card('Structural findings',INFO.blocking);card('Targets',INFO.count);card('Paper on HOLD',INFO.elig?.paper?.HOLD??'—');card('Digital on HOLD',INFO.elig?.digital?.HOLD??'—');card('Unchecked keys',INFO.coverage.rows_total-INFO.coverage.rows_with_key_check);card('Open gaps',INFO.gaps_count);
for(const [name,value] of Object.entries(INFO.gates)){const g=el('div',undefined,'gate');g.append(el('span',name),state(value));$('gates').append(g);}
$('release').textContent='Overall paper: '+INFO.release.paper+' · Digital: '+INFO.release.digital+' · Scope: '+INFO.release.scope;
$('env').textContent=(INFO.environment.python||'?')+' / SymPy '+(INFO.environment.sympy||'?');
let filteredRows=[],filteredGaps=[];
function renderRows(){const q=$('rowsearch').value.toLowerCase();const filter=$('statusfilter').value;filteredRows=ROWS.filter(x=>(!filter||x.eligibility_paper===filter)&&(!q||(x.target_id+' '+x.reasons).toLowerCase().includes(q)));const root=$('rows');root.replaceChildren();for(const x of filteredRows){const tr=el('tr');cell(tr,x.target_id);for(const k of ['eligibility_paper','eligibility_digital','calculation','curriculum','teacher_review','diagnostic_validity']){const t=el('td');t.append(state(x[k]));tr.append(t);}cell(tr,x.reasons,'td').className='reason';root.append(tr);}$('rowcount').textContent=filteredRows.length+' of '+ROWS.length+' targets displayed';}
function renderGaps(){const q=$('gapsearch').value.toLowerCase();const filter=$('gapfilter').value;filteredGaps=GAPS.filter(x=>(!filter||x.gap===filter)&&(!q||(x.id+' '+x.seed+' '+x.value+' '+x.gap).toLowerCase().includes(q)));const root=$('gaps');root.replaceChildren();for(const x of filteredGaps){const tr=el('tr');for(const k of ['id','field','seed','value','gap'])cell(tr,x[k]);root.append(tr);}$('gapcount').textContent=filteredGaps.length+' of '+GAPS.length+' gaps displayed';}
const types=[...new Set(GAPS.map(x=>x.gap))].sort();for(const t of types){const opt=el('option',t);opt.value=t;$('gapfilter').append(opt);}
$('rowsearch').addEventListener('input',renderRows);$('statusfilter').addEventListener('change',renderRows);$('gapsearch').addEventListener('input',renderGaps);$('gapfilter').addEventListener('change',renderGaps);
function downloadCSV(filename,records,keys){const quote=s=>'"'+String(s??'').replace(/"/g,'""')+'"';const content=[keys.join(','),...records.map(r=>keys.map(k=>quote(r[k])).join(','))].join('\r\n');const blob=new Blob(['\ufeff',content],{type:'text/csv;charset=utf-8;'});const link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download=filename;link.click();setTimeout(()=>URL.revokeObjectURL(link.href),1000);}
$('rowexport').addEventListener('click',()=>downloadCSV('eligibility_filtered_v11.csv',filteredRows,['target_id','eligibility_paper','eligibility_digital','calculation','curriculum','teacher_review','diagnostic_validity','reasons']));
$('gapexport').addEventListener('click',()=>downloadCSV('coverage_gaps_filtered_v11.csv',filteredGaps,['id','field','seed','value','gap']));
renderRows();renderGaps();
</script></body></html>'''
    document=document.replace('__INFO__',js_json(info)).replace('__ROWS__',js_json(rows)).replace('__GAPS__',js_json(gaps))
    out=HERE/'validation_dashboard_v11.html'
    out.write_text(document,encoding='utf-8',newline='\n')
    print(f'HTML generated: {out.name} ({len(rows)} target rows, {len(gaps)} gaps)')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
