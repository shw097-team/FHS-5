#!/usr/bin/env python3
"""FHS-5 W3 r2 pack consumer (stdlib only). Reader/validator, not a product runner."""
import argparse,hashlib,json,os,re,sys
PACK=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
def sha(p):
 h=hashlib.sha256(); h.update(open(p,'rb').read()); return h.hexdigest()
def lines(p): return len(open(p,'rb').read().decode('utf-8').splitlines())
def load(p):
 def hook(pairs):
  s=set()
  for k,v in pairs:
   if k in s: raise ValueError('duplicate key '+k)
   s.add(k)
  return dict(pairs)
 return json.loads(open(p,'rb').read().decode('utf-8'),object_pairs_hook=hook)
def check(pack,seal=None,adoption=None,current=None,allow_missing=False):
 e=[]; d=load(os.path.join(pack,'05_W3_SOURCE_MANIFEST.json'))
 def w(n,ok,x=''):
  if not ok: e.append({'name':n,'detail':str(x)})
 w('schema',d.get('schema')=='FHS5.PLP.W3.SourceManifest.NF@2',d.get('schema'))
 w('subject',d.get('identity',{}).get('subject_id')=='FHS-5_PLP/W3/CONTROL_PACK')
 w('scope',d.get('identity',{}).get('scope')=='W3-NF-01')
 w('artifact',d.get('identity',{}).get('artifact_id')=='FHS5-PLP/W3/PACK-NF-20261126-r2-CODEX-PRIMARY')
 w('selection',d.get('selection_state')=='PACK_PRIMARY_SELECTED')
 f=d.get('files',[]); w('file_count',len(f)==5,len(f))
 for x in f:
  p=os.path.join(pack,x['path'].replace('/',os.sep)); w('file:'+x['path'],os.path.isfile(p) and sha(p)==x['sha256'] and os.path.getsize(p)==x['bytes'] and lines(p)==x['lines'])
 a=d.get('assets',[]); w('asset_count',len(a)>=36,len(a)); ap=set()
 for x in a:
  ap.add(x['path']); p=os.path.join(pack,x['path'].replace('/',os.sep)); w('asset:'+x['path'],os.path.isfile(p) and sha(p)==x['sha256'] and os.path.getsize(p)==x['bytes'] and lines(p)==x['lines'])
 c=d.get('case_refs',[]); w('case_count',len(c)==16,len(c)); w('case_unique',len({x['case_id'] for x in c})==16)
 cm={x['case_id']:x for x in c}
 for x in c:
  for k in ('case_id','kind','requirement_refs','fixture','oracle','runner','expected','observed','verdict','not_covered','consumer'): w('case_field:%s:%s'%(x['case_id'],k),k in x)
  w('case_not_run:'+x['case_id'],x.get('observed') is None and x.get('verdict')=='NOT_RUN')
  for k in ('fixture','oracle'): w('case_asset:%s:%s'%(x['case_id'],k),x[k]['path'] in ap)
 for x in d.get('requirement_crosswalk',[]):
  fr=x['fr']; pc=x.get('primary_case')
  if x.get('reasoned_nc'): continue
  w('crosswalk_case:'+fr,pc in cm,pc)
  if pc in cm: w('crosswalk_ref:'+fr,fr in cm[pc]['requirement_refs'],cm[pc]['requirement_refs'])
 s=d.get('sources',[]); w('source_count',len(s)==28,len(s))
 for x in s:
  w('source_logical:'+x['id'],x.get('locator','').startswith(('S:','R:')))
  w('source_disposition:'+x['id'],bool(x.get('disposition')))
  for sp in x.get('spans',[]):
   lo,hi=sp['lines']; w('source_span:%s:%s'%(x['id'],sp.get('section')),1<=lo<=hi<=x['lines'],sp)
 pre=''.join(sorted(x['id']+'\t'+x['sha256']+'\t'+str(x['bytes'])+'\t'+x['locator']+'\n' for x in s))
 w('source_set',hashlib.sha256(pre.encode()).hexdigest()==d['digest_contract']['source_set_sha256'])
 tl=[x['path']+'\t'+str(x['bytes'])+'\t'+x['sha256']+'\n' for x in f+a]
 w('package_tree',hashlib.sha256(''.join(sorted(tl)).encode()).hexdigest()==d['digest_contract']['package_tree_sha256'])
 h={x['id']:x for x in d.get('holds',[])}; w('hold_count',len(h)==24,len(h)); w('pack_absent_closed',h.get('W3_PACK_ABSENT',{}).get('state')=='CLOSED_BY_ADOPTION'); w('w2_writer_open',h.get('W2_WRITER_BLOCKED',{}).get('state')=='OPEN')
 t=open(os.path.join(pack,'05_W3_SOURCE_MANIFEST.json'),'rb').read().decode(); w('no_abs_path',not re.search(r'[A-Za-z]:\\\\',t)); w('no_self_hash',sha(os.path.join(pack,'05_W3_SOURCE_MANIFEST.json')) not in t)
 ext={}
 for k,p in (('seal',seal),('adoption',adoption),('current',current)):
  if p:
   w(k+'_exists',os.path.isfile(p),p)
   if os.path.isfile(p): ext[k]=load(p)
  elif not allow_missing: w(k+'_provided',False,'missing')
 if 'seal' in ext:
  w('seal_manifest',ext['seal'].get('manifest_sha256')==sha(os.path.join(pack,'05_W3_SOURCE_MANIFEST.json')))
  w('seal_tree',ext['seal'].get('package_tree_sha256')==d['digest_contract']['package_tree_sha256'])
 if 'adoption' in ext:
  w('adoption_decision',ext['adoption'].get('decision_id')==d['adoption']['decision_id'])
  w('adoption_manifest',ext['adoption'].get('manifest_sha256')==sha(os.path.join(pack,'05_W3_SOURCE_MANIFEST.json')))
 return {'ok':not e,'errors':e,'identity':d.get('identity'),'selection_state':d.get('selection_state'),'counts':{'files':len(f),'assets':len(a),'cases':len(c),'sources':len(s),'holds':len(h)}}
def nxt(pack):
 root=os.path.dirname(os.path.dirname(pack)); seal=os.path.join(root,'EXTERNAL_SEAL.json'); ad=os.path.join(root,'W3_OWNER_ADOPTION.json'); cur=os.path.join(root,'W3_CURRENT.json')
 if not all(os.path.isfile(x) for x in (seal,ad,cur)): return {'action':'STOP_SCOPED','reason':'external seal/adoption/current missing','candidates':[]}
 r=check(pack,seal,ad,cur)
 if not r['ok']: return {'action':'STOP_SCOPED','reason':'pack check failed','errors':r['errors'][:5]}
 return {'action':'P01_READ','reason':'primary/executable; W2 PARTIAL/writer blocked','candidates':['P01_READ','R0_REOPEN','R1_README','ISOLATED_SMOKE'],'product_ready':False}
def case(pack,cid):
 d=load(os.path.join(pack,'05_W3_SOURCE_MANIFEST.json')); c=next((x for x in d['case_refs'] if x['case_id']==cid),None)
 if not c: return {'error':'CASE_UNKNOWN'}
 return {'case_id':cid,'kind':c['kind'],'input':load(os.path.join(pack,c['fixture']['path'])).get('input'),'expected':load(os.path.join(pack,c['oracle']['path'])).get('expected'),'runner':c.get('runner'),'observed':c.get('observed'),'verdict':c.get('verdict')}
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--pack',default=PACK); ap.add_argument('--check',action='store_true'); ap.add_argument('--next',action='store_true'); ap.add_argument('--case'); ap.add_argument('--seal'); ap.add_argument('--adoption'); ap.add_argument('--current'); ap.add_argument('--allow-missing-external',action='store_true'); a=ap.parse_args(); p=os.path.abspath(a.pack)
 if a.case: o=case(p,a.case); code=0 if 'error' not in o else 1
 elif a.next: o=nxt(p); code=0 if o['action']!='STOP_SCOPED' else 1
 else: o=check(p,a.seal,a.adoption,a.current,a.allow_missing_external); code=0 if o['ok'] else 1
 print(json.dumps(o,ensure_ascii=False,indent=2)); return code
if __name__=='__main__': sys.exit(main())
