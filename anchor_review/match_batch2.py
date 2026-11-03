"""Batch 2: automated, verbatim term matching of each SOURCE_LINKED ref against the official text.
Every passage returned is an exact line of the pdftotext output; nothing is paraphrased."""
import re,unicodedata,os
BO=os.environ.get('BO','/workspace/bo')
def pages(f,a=1,b=10**6):
  t=open(f'{BO}/{f}').read().split('\f'); return [(i+1,p) for i,p in enumerate(t) if a<=i+1<=b]
a,b=127,139  # volet 3 Mathématiques, PDF pages 127-139 (checked by hand)
SRC={
 'BR2020':dict(title='Programme du cycle 4 en vigueur à la rentrée 2020 (BO n°31 du 30 juillet 2020), volet 3 Mathématiques, version Éduscol',url='https://eduscol.education.gouv.fr/sites/default/files/document/programme-d-enseignement-du-cycle-4-67722.pdf',ed='2020 cycle 4 programme; applies to 3e in 2026-27 and 2027-28 (DNB 2027 and 2028)',pg=pages('C4_2020.txt',a,b)),
 'BR2026':dict(title='Annexe 2 – Programme de mathématiques pour le cycle 4 (BO n°10 du 5 mars 2026, MENE2602912A)',url='https://www.education.gouv.fr/sites/default/files/document/Annexe%202%20%E2%80%93%20Programme%20de%20math%C3%A9matiques%20pour%20le%20cycle%204-480716.pdf',ed='2026 cycle 4 programme; 5e 2026-27, 4e 2027-28, 3e 2028-29 (first DNB under it: 2029)',pg=pages('R15.txt')),
 'TS':dict(title='Programme de spécialité de mathématiques de terminale générale (BO spécial n°8 du 25 juillet 2019, MENE1921246A), annexe Éduscol',url='https://eduscol.education.gouv.fr/sites/default/files/document/spe246annexe1158907pdf-84159.pdf',ed='2019 text, in force in Terminale 2026-27 (new 2026 text from 2027-28)',pg=pages('R12.txt')),
 'TC':dict(title='Programme d’enseignement optionnel de mathématiques complémentaires de terminale générale (BO spécial n°8 du 25 juillet 2019, MENE1921265A), annexe Éduscol',url='https://eduscol.education.gouv.fr/sites/default/files/document/spe265annexe1159134pdf-84162.pdf',ed='2019 text, in force in Terminale 2026-27',pg=pages('R28.txt')),
 'TE':dict(title='Programme d’enseignement optionnel de mathématiques expertes de terminale générale (BO spécial n°8 du 25 juillet 2019), annexe Éduscol',url='https://eduscol.education.gouv.fr/sites/default/files/document/spe264annexe1158825pdf-84165.pdf',ed='2019 text, in force in Terminale 2026-27',pg=pages('R10.txt')),
 'M1':dict(title='Classes préparatoires MPSI et MP2I – Annexe 1 Programme de mathématiques (MESRI 2021)',url='https://cache.media.education.gouv.fr/file/SPE1-MEN-MESRI-4-2-2021/64/8/spe779_annexe_1373648.pdf',ed='2021 programme, in force since rentrée 2021',pg=pages('5cb2f0.txt')),
 'M2':dict(title='Classes préparatoires MP et MPI – Annexe 1 Programme de mathématiques (MESRI 2021)',url='https://cache.media.education.gouv.fr/file/31/21/2/ensecsup756_annexes_1417212.pdf',ed='2021 programme, in force since rentrée 2022 (2nd year)',pg=pages('R25.txt')),
}
def n(s): s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if unicodedata.category(c)!='Mn'); return re.sub(r'[^a-z0-9²³ⁿ∞]+',' ',s)
STOP=set('les des une avec pour dans sans entre sous sur aux par est son ses leur cas lien nouveau sortant explicite seulement'.split())
def words(term): return [w[:6] for w in n(term).split() if len(w)>3 and w not in STOP]
def terms(par):
  par=re.sub(r'\((?:sortant|nouveau|[^)]*: ?(?:nouveau|sortant))\)','',par)
  return [t for t in re.split(r'[,;]| et (?=[a-zéè])',par) if words(t)]
def hit(ws,txt): return all(re.search(r'\b'+re.escape(w),txt) for w in ws)
def best(src,par):
  """Each term is searched independently over all pages; for a term, the hit is the source line with the best
  word coverage on a page that contains all its words. Returns pages and exact lines."""
  ts=terms(par); found=[];lines=[];pgs=[]; allw=words(par)
  for t in ts:
    ws=words(t); bestl=None
    for p,txt in SRC[src]['pg']:
      if not hit(ws,n(txt)): continue
      for l in txt.split('\n'):
        nl=n(l); sc=sum(bool(re.search(r'\b'+re.escape(w),nl)) for w in ws)
        if sc: sc=sc*10+sum(bool(re.search(r'\b'+re.escape(w),nl)) for w in allw)
        if sc and (not bestl or sc>bestl[0]): bestl=(sc,p,l.strip())
    if bestl:
      found.append(t); pgs.append(bestl[1])
      if bestl[2] not in lines: lines.append(bestl[2])
  if not ts: return None
  return dict(page=','.join(str(x) for x in dict.fromkeys(pgs)) or '-',terms=ts,found=found,lines=lines)
