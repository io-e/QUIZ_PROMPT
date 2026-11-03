import csv,collections,os
d=os.path.dirname(os.path.abspath(__file__))
T=[r['id'] for r in csv.DictReader(open(f'{d}/../Math_Diagnostic_Reference_CLAUDE_v11/Math_Diagnostic_Targets_v11.csv'))]
A=[r['target_id'] for r in csv.DictReader(open(f'{d}/Official_Programme_Audit_600_GROK.csv'))]
dup=[k for k,v in collections.Counter(A).items() if v>1]
print('targets',len(T),'unique',len(set(T)),'| audit rows',len(A),'unique',len(set(A)))
print('missing',sorted(set(T)-set(A)),'extra',sorted(set(A)-set(T)),'duplicates',dup)
assert len(A)==600==len(set(A)) and set(A)==set(T); print('COVERAGE_OK: exactly 600 unique IDs, identical to Math_Diagnostic_Targets_v11.csv')
