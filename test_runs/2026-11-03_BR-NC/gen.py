import csv,json,html,re
from sympy import Rational as R, symbols, expand, solve, factor, Eq, sympify
x=symbols('x')
K='/workspace/quiz2/Math_Diagnostic_Reference_CLAUDE_v11/'
rows={r['id']:r for r in csv.DictReader(open(K+'Math_Diagnostic_Targets_v11.csv',encoding='utf-8'))}
elig={r['target_id']:r for r in csv.DictReader(open(K+'Item_Release_Eligibility_v11.csv',encoding='utf-8'))}
# MCQ items: (row, stem FR, key text, key sympy, [(code, text, sympy model of the error)], order)
M=[
('BR-NC-01','Calculer : −3/4 + 1/2. Donner le résultat sous forme de fraction irréductible.','−1/4',R(-3,4)+R(1,2),
 [('BR-NC-01-E1','−1/3',R(-3+1,4+2),"A additionné numérateurs et dénominateurs : (−3+1)/(4+2)."),
  ('BR-NC-01-E2','5/4',R(3,4)+R(1,2),"A ignoré le signe moins de −3/4."),
  ('BR-NC-01-E3','−5/4',-(R(3,4)+R(1,2)),"A additionné les valeurs absolues en gardant le signe moins.")],'B'),
('BR-NC-06','Calculer : −7 + 3 − (−5)','1',-7+3-(-5),
 [('BR-NC-06-E1','−5',-(7+3)+5,"A additionné les valeurs absolues de −7 et 3 en gardant le signe moins."),
  ('BR-NC-06-E2','−9',-7+3-5,"A traité « − (−5) » comme « − 5 »."),
  ('BR-NC-06-E3','9',7-3+5,"A perdu le signe de −7 + 3.")],'D'),
('BR-NC-10','Calculer : 2/3 − 1/4. Donner le résultat sous forme de fraction irréductible.','5/12',R(2,3)-R(1,4),
 [('BR-NC-10-E1','−1',R(2-1,3-4),"A soustrait numérateurs et dénominateurs."),
  ('BR-NC-10-E2','1/12',R(2-1,12),"A pris 12 comme dénominateur commun sans convertir les numérateurs."),
  ('BR-NC-10-E3','1/6',R(2*1,3*4),"A appliqué la règle du produit à la différence.")],'A'),
('BR-NC-22','Développer et réduire : 5 − 3(2x − 4)','17 − 6x',expand(5-3*(2*x-4)),
 [('BR-NC-22-E1','−7 − 6x',5-6*x-12,"N’a pas appliqué le signe moins au second terme de la parenthèse."),
  ('BR-NC-22-E2','1 − 6x',5-3*2*x-4,"A multiplié seulement le premier terme par 3."),
  ('BR-NC-22-E3','4x − 8',expand(2*(2*x-4)),"A calculé 5 − 3 d’abord.")],'C'),
('BR-NC-26','Résoudre l’équation : 5x − 7 = 2x + 8','x = 5',solve(Eq(5*x-7,2*x+8),x)[0],
 [('BR-NC-26-E1','x = 1/3',solve(Eq(3*x,8-7),x)[0],"A déplacé −7 sans changer son signe."),
  ('BR-NC-26-E2','x = 12',R(15-3),"A confondu opposé et inverse (3x = 15 ⇒ x = 12)."),
  ('BR-NC-26-E3','x = 15/7',solve(Eq(7*x,15),x)[0],"A déplacé 2x sans changer son signe.")],'B'),
]
def sig2sym(s):
    s=s.replace('−','-').replace(' ','').replace('x=','')
    return sympify(re.sub(r'(\d)x',r'\1*x',s))
L='ABCD'; check=[]; items=[]
for rid,stem,ktxt,kval,ds,kpos in M:
    r=rows[rid]; errs={e['id']:e for e in json.loads(r['errors_json'])}
    assert r['allowed_items']=='MCQ+OPEN'
    ok_key=sympy_eq=(sig2sym(r['mcq_key'])-kval).equals(0) if 'x' not in r['mcq_key'] or '=' in r['mcq_key'] else expand(sig2sym(r['mcq_key'])-kval)==0
    ok_key=expand(sig2sym(ktxt)-kval)==0 and ok_key
    opts=[None]*4; others=[i for i in range(4) if L[i]!=kpos]
    opts[L.index(kpos)]=dict(text=ktxt,correct=True)
    dl=[]
    for (c,t,v,why),p in zip(ds,others):
        sig=errs[c].get('sig_mcq','')
        m1=expand(sig2sym(sig)-v)==0; m2=expand(sig2sym(t)-v)==0; distinct=expand(v-kval)!=0
        dl.append((c,t,sig,str(v),m1 and m2 and distinct))
        opts[p]=dict(text=t,correct=False,error_code=c,why=why)
    items.append(dict(id=rid,type='mcq',stem=stem,options=opts,key=kpos,anchor=r['anchor_status'],elig=elig[rid]['eligibility_paper']+'/'+elig[rid]['eligibility_digital']))
    check.append((rid,r['mcq_seed'],r['mcq_key'],ktxt,str(kval),ok_key,dl))
# open seed check BR-NC-04
sol04=sorted(solve(9*x**2-25,x)); f04=factor(9*x**2-25)
check_open=[('BR-NC-04','9x²−25=0',str(f04),str(sol04),f04==factor((3*x-5)*(3*x+5)) and sol04==[R(-5,3),R(5,3)])]
s05=solve(2*x+3-11,x)[0]; check_open.append(('BR-NC-05','2x+3≤11','x ≤ 4',str(s05),s05==4))
json.dump(dict(items=items,check=[list(map(str,c[:6]))+[c[6]] for c in check],open=check_open),open('BR-NC_items.json','w'),ensure_ascii=False,indent=1,default=str)
print(json.dumps(check,ensure_ascii=False,default=str,indent=0)); print(check_open)
