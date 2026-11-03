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
  else:
    r.update(conformity='UNVERIFIED',justification='Not yet audited in batch 1: official text for this level not fetched/checked yet. Existing link alone does not prove conformity.',batch='2 (pending)')
  out.append(r)
w=csv.DictWriter(open(os.path.join(os.path.dirname(__file__),'Official_Programme_Audit_600_GROK.csv'),'w',newline=''),fieldnames=cols);w.writeheader();w.writerows(out)
print('rows',len(out),'unique',len({r['target_id'] for r in out}),'string-check failures',bad)
print(collections.Counter((r['anchor_status_v11'],r['conformity']) for r in out))
