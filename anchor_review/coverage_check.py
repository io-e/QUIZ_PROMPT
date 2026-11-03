import csv,collections,os
d=os.path.dirname(os.path.abspath(__file__))
T=[r['id'] for r in csv.DictReader(open(f'{d}/../Math_Diagnostic_Reference_CLAUDE_v11/Math_Diagnostic_Targets_v11.csv'))]
A=[r['target_id'] for r in csv.DictReader(open(f'{d}/Official_Programme_Audit_600_GROK.csv'))]
dup=[k for k,v in collections.Counter(A).items() if v>1]
print('targets',len(T),'unique',len(set(T)),'| audit rows',len(A),'unique',len(set(A)))
print('missing',sorted(set(T)-set(A)),'extra',sorted(set(A)-set(T)),'duplicates',dup)
assert len(A)==600==len(set(A)) and set(A)==set(T); print('COVERAGE_OK: exactly 600 unique IDs, identical to Math_Diagnostic_Targets_v11.csv')

R=list(csv.DictReader(open(f'{d}/Official_Programme_Audit_600_GROK.csv')))
EC=['conformity_2020','source_url_2020','page_2020','passage_2020','conformity_2026','source_url_2026','page_2026','passage_2026','edition_flag']
br=[x for x in R if x['level']=='BREVET']; nb=[x for x in R if x['level']!='BREVET']
assert len(br)==95 and all(x['edition_flag'] in('BOTH','2020_ONLY','2026_ONLY','NEITHER') and x['source_url_2020'] and x['source_url_2026'] for x in br)
assert all(all(x[k]=='N/A' for k in EC) for x in nb)
assert not any(x['conformity']=='PASS' for x in R)
print('EDITION_COLUMNS_OK: 95 BREVET rows flagged', dict(collections.Counter(x['edition_flag'] for x in br)), '| 505 non-Brevet rows N/A | no PASS')
