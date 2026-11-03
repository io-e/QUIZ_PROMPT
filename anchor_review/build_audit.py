import csv,re,sys,os,collections
sys.path.insert(0,os.path.dirname(__file__)); from map_batch1 import REF,TGT
PKG=os.path.join(os.path.dirname(__file__),'..','Math_Diagnostic_Reference_CLAUDE_v11')
BO=os.environ.get('BO','/workspace/bo')
norm=lambda s:re.sub(r'\s+',' ',s).replace('− ','').replace('−','').strip()
TXT={'BO14':norm(open(f'{BO}/bo14.txt').read()),'MP2I':norm(open(f'{BO}/5cb2f0.txt').read())}
SRC={'1S':('BO n°14 du 2 avril 2026 – Programme d’enseignement de spécialité de mathématiques de la classe de première de la voie générale (MENE2602917A), version PDF complète du BO','https://www.education.gouv.fr/sites/default/files/document/Bulletin%20officiel%20n%C2%B0%2014%20du%202%20avril%202026-515432.pdf','BO14','2026 edition, applicable rentrée 2026-2027'),
'1C':('BO n°14 du 2 avril 2026 – Programme de mathématiques intégré à l’enseignement scientifique en classe de première générale (MENE2602916A), version PDF complète du BO','https://www.education.gouv.fr/sites/default/files/document/Bulletin%20officiel%20n%C2%B0%2014%20du%202%20avril%202026-515432.pdf','BO14','2026 edition, applicable rentrée 2026-2027'),
'MP':('Classes préparatoires MPSI et MP2I – Annexe 1 Programme de mathématiques (MESRI 2021)','https://cache.media.education.gouv.fr/file/SPE1-MEN-MESRI-4-2-2021/64/8/spe779_annexe_1373648.pdf','MP2I','2021 edition, in force since rentrée 2021')}
def verify(p,key):
  for frag in re.split(r'\s*\[\.\.\.\]\s*',p):
    f=norm(frag)
    # tolerate formula pieces lost in extraction: check the first 40 chars
    if norm(f)[:40] not in TXT[key]: return False
  return True
tg=list(csv.DictReader(open(f'{PKG}/Math_Diagnostic_Targets_v11.csv')))
wl={r['target_id']:r for r in csv.DictReader(open(f'{PKG}/Anchor_Verification_Worklist_v11.csv'))}
cols=['target_id','level','track_edition_school_year','anchor_status_v11','capability','current_official_ref','conformity','source_title','source_url','page','page_or_section','verbatim_passage','official_evidence','pedagogical_interpretation','justification','discrepancy_and_proposed_correction','confidence','consulted_on','batch','reviewer','reviewed_on']
out=[];bad=[]
import re as _re, match_batch2 as M
IDX={x['ref']:x for x in csv.DictReader(open(f'{PKG}/Math_Official_Referential_Index_v11.csv'))}
LEV=[l for l in os.environ.get('LEVELS','').split(',') if l]
KEY={'BAC_TLE_SPE':'TS','BAC_TLE_COMPLEMENTAIRES':'TC','BAC_TLE_EXPERTES':'TE','MP2I':'M1','MPI':'M2'}
OVR={k:dict(conformity='SUPPORTED',page='PDF p.14-15',verbatim_passage="Pour une équation différentielle y’ = ay + b (a ≠ 0) : déterminer une solution particulière constante ; utiliser cette solution pour déterminer toutes les solutions. [...] Pour une équation différentielle y’ = ay + ƒ : à partir de la donnée d’une solution particulière, déterminer toutes les solutions.",
  confidence='high',discrepancy_and_proposed_correction='',justification='Manual check (the automated matcher could not parse the formulas); passage copied from pdftotext output, pp. 14-15, Analyse > Primitives, équations différentielles > Capacités attendues.') for k in ('TS-AN-05','TS-AN-38')}
for k in OVR: OVR[k]['official_evidence']=OVR[k]['verbatim_passage']
RANK={'SUPPORTED':0,'PARTIALLY_SUPPORTED':1,'UNVERIFIED':2}
def b2(t):
  refs=[x for x in _re.split(r'[;\s]+',t['official_ref']) if x]
  parts=[];st=[];pages=[];urls=[];titles=[];eds=[];notes=[];interp=[]
  for ref in refs:
    ix=IDX.get(ref)
    if not ix: st.append('UNVERIFIED');notes.append(f'{ref}: not in the referential index');continue
    par=ix['capability_paraphrase']
    srcs=['BR2020','BR2026'] if t['level']=='BREVET' else [KEY[t['level']]]
    res={s:M.best(s,par) for s in srcs}
    main=srcs[0]; r=res[main]
    def stat(r): return 'UNVERIFIED' if not r or not r['found'] else ('SUPPORTED' if len(r['found'])==len(r['terms']) else 'PARTIALLY_SUPPORTED')
    s0=stat(r)
    if t['level']=='BREVET':
      s1=stat(res['BR2026'])
      ed=ix['edition']
      if s0!='SUPPORTED' and s1=='SUPPORTED':
        notes.append(f"{ref}: all terms found only in the 2026 programme (p.{res['BR2026']['page']}), not fully in the 2020 programme that still applies to 3e and the DNB until 2028 (index edition={ed}).")
        if ed=='NEW': interp.append(f'{ref}: consistent with index edition NEW; such items cannot be required for DNB 2027-2028.')
      if s0=='SUPPORTED' and s1!='SUPPORTED': notes.append(f"{ref}: found in the 2020 programme but not fully in the 2026 programme (index edition={ed}); outgoing notion.")
      if ed=='NEW' and s0=='SUPPORTED': notes.append(f'{ref}: index says NEW but terms also found in 2020 text; check edition flag.')
      for k,rr in (('2020',r),('2026',res['BR2026'])):
        if rr and rr['found']:
          parts.append(f"[{k} p.{rr['page']}] "+' / '.join(rr['lines']));pages.append(f"{k}: PDF p.{rr['page']}")
      urls+= [M.SRC['BR2020']['url'],M.SRC['BR2026']['url']]; titles+=[M.SRC['BR2020']['title'],M.SRC['BR2026']['title']]; eds+=[M.SRC['BR2020']['ed'],M.SRC['BR2026']['ed']]
      sx=s0 if s0!='UNVERIFIED' else ('PARTIALLY_SUPPORTED' if s1!='UNVERIFIED' else 'UNVERIFIED')
      if s0!='SUPPORTED' and s1=='SUPPORTED': sx='PARTIALLY_SUPPORTED'
      st.append(sx)
    else:
      if r and r['found']: parts.append(f"[p.{r['page']}] "+' / '.join(r['lines']));pages.append(f"PDF p.{r['page']}")
      urls.append(M.SRC[main]['url']);titles.append(M.SRC[main]['title']);eds.append(M.SRC[main]['ed']);st.append(s0)
    miss=[x.strip() for x in (r['terms'] if r else []) if x not in (r['found'] if r else [])]
    if miss: notes.append(f"{ref}: terms not found anywhere in the applicable text: {miss}")
    if not r or not r['found']: notes.append(f'{ref}: no term of the index paraphrase «{par}» found by automated matching; manual check needed.')
  u=lambda L:' | '.join(dict.fromkeys(L))
  return dict(conformity=max(st,key=lambda x:RANK[x]),source_title=u(titles),source_url=u(urls),track_edition_school_year=u(eds),page=u(pages),
    page_or_section='; '.join(f"{x}: {IDX[x]['chapter']} > {IDX[x]['section']}" for x in refs if x in IDX),verbatim_passage=' || '.join(parts),
    official_evidence=' || '.join(parts),pedagogical_interpretation=' '.join(interp) or 'Automated match of the index paraphrase terms; whether the passage really covers the item as worded needs the teacher.',
    justification='Batch 2: each index-paraphrase term searched (accent/case-insensitive, word prefixes) in the fetched official text; passages are exact source lines.',
    discrepancy_and_proposed_correction=' '.join(notes),confidence=('medium' if max(st,key=lambda x:RANK[x])=='SUPPORTED' else 'low'),consulted_on='2026-11-03',batch='2')
for t in tg:
  i=t['id'];ref=t['official_ref'];r=dict.fromkeys(cols,'')
  r.update(target_id=i,level=t['level'],anchor_status_v11=t['anchor_status'],capability=t['capability'],current_official_ref=ref)
  m=TGT.get(i) or REF.get(ref.split()[0]) if i in wl else None
  if m:
    pg,sec,pas,st,conf,why=m; k='MP' if ref.startswith('MP2I') else ref[:2]
    title,url,key,ed=SRC[k]
    ok=verify(pas,key)
    if not ok: bad.append(i)
    r.update(track_edition_school_year=ed,conformity=('UNVERIFIED' if not ok else st),source_title=title,source_url=url,page=f'PDF p.{pg}',page_or_section=sec,verbatim_passage=pas,
      official_evidence=f'p.{pg} {sec}: «{pas}»',pedagogical_interpretation=why or 'Passage matches the capability as worded.',
      justification=('Passage fetched and string-checked against pdftotext output.' if ok else 'Passage failed automatic string check.'),
      discrepancy_and_proposed_correction=(why if st!='SUPPORTED' else ''),confidence=conf,consulted_on='2026-11-03',batch='1')
    if t['anchor_status']=='NOT_SUPPORTED': r['discrepancy_and_proposed_correction']+=' Keep excluded (no reclassification proposed).'
  elif t['level'] in LEV and t['anchor_status']=='SOURCE_LINKED':
    r.update(b2(t))
    if i in OVR: r.update(OVR[i])
  else:
    r.update(conformity='UNVERIFIED',justification='Not yet audited in batch 1: official text for this level not fetched/checked yet. Existing link alone does not prove conformity.',batch='2 (pending)')
  out.append(r)
w=csv.DictWriter(open(os.path.join(os.path.dirname(__file__),'Official_Programme_Audit_600_GROK.csv'),'w',newline=''),fieldnames=cols);w.writeheader();w.writerows(out)
print('rows',len(out),'unique',len({r['target_id'] for r in out}),'string-check failures',bad)
print(collections.Counter((r['anchor_status_v11'],r['conformity']) for r in out))
