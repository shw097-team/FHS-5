
#!/usr/bin/env python3
"""FHS-5 PLP r3 author-only integrity/linkage guard. No privileged Reader/Issuer/Checker.
This reference never promotes local results to original/native acceptance.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile

SHA = re.compile(r'^[a-f0-9]{64}$')
WAVE = re.compile(r'^W(?:0|[1-9][0-9]*)$')
IDENT = re.compile(r'<!-- FHS5_IDENTITY: (\{[^\r\n]+\}) -->')
SOURCE_SCHEMA = 'FHS5.PLP.SourceManifest@proposal-2'
CONTROL_SCHEMA = 'FHS5.PLP.WaveControl@proposal-2'
FILE_SCHEMA = 'FHS5.PLP.FileManifest@proposal-2'
TQAEP_SCHEMA = 'FHS5.PLP.TQAEPProjection@proposal-2'
IDENTITY_KEYS = ('project_id','subject_id','scope','wave_id','batch_id','source_manifest_sha256')
EFFECTS = {'READ','DRAFT','DEV','OPS','USER','RELEASE'}
DOC_FIXED = ('00_WAVE_RUN_MANIFEST.md','01_SOURCE_SCOPE_AND_CONSTRUCTION.md',
             '03_DEV_ECP.md','04_OPS_ECP.md','05_PLANNED_TQAEP.md',
             '06_PERMISSION_STOP_RESUME.md','07_EVIDENCE_AND_CHECKER.md',
             '08_AS_BUILT_AND_HANDOFF.md','09_README_RUN_ORDER.md')
JSON_FIXED = ('00_WAVE_RUN_MANIFEST.json','02_ORIGINAL_CONTRACT_REFS.json',
              '05_PLANNED_TQAEP.json')
CASE_KINDS = {'POS','NEG','EDGE','SEC'}

class GuardError(Exception): pass

def require(cond, msg):
    if not cond: raise GuardError(msg)

def digest(b): return hashlib.sha256(b).hexdigest()

def sha(v): return isinstance(v,str) and bool(SHA.fullmatch(v))

def unique_pairs(pairs):
    out={}
    for key,val in pairs:
        if key in out: raise GuardError('JSON_DUPLICATE_KEY:'+key)
        out[key]=val
    return out

def bad_constant(c): raise GuardError('JSON_BAD_CONSTANT:'+c)

def read_json(path):
    try: return json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=unique_pairs,parse_constant=bad_constant)
    except (UnicodeError,json.JSONDecodeError) as e: raise GuardError('JSON_UNREADABLE:'+path.name) from e

def safe_file(root:Path,relative:str):
    require(isinstance(relative,str) and relative and len(relative)<512,'BAD_RELATIVE_PATH')
    require('\\' not in relative and ':' not in relative and '\x00' not in relative,'BAD_PATH_SYNTAX')
    p=PurePosixPath(relative)
    require(not p.is_absolute() and all(x not in ('','..','.') for x in relative.split('/')),'PATH_TRAVERSAL')
    base=root.resolve(strict=True)
    require(base.is_dir(),'ROOT_NOT_DIRECTORY')
    cur=base
    for part in p.parts:
        cur=cur/part
        try: mode=cur.lstat().st_mode
        except OSError as e: raise GuardError('MISSING_FILE:'+relative) from e
        require(not stat.S_ISLNK(mode),'SYMLINK_FORBIDDEN:'+relative)
    actual=cur.resolve(strict=True)
    require(actual.is_relative_to(base) and actual.is_file(),'PATH_OUTSIDE_ROOT:'+relative)
    return actual

def identity(obj):
    require(isinstance(obj,dict),'IDENTITY_NOT_OBJECT')
    for k in IDENTITY_KEYS:
        v=obj.get(k)
        require(isinstance(v,str) and v.strip(),'IDENTITY_MISSING:'+k)
    require(sha(obj['source_manifest_sha256']),'SOURCE_MANIFEST_SHA_BAD')
    require(WAVE.fullmatch(obj['wave_id']) is not None,'WAVE_ID_BAD')
    return {k:obj[k] for k in IDENTITY_KEYS}

def check_inventory(source_root, manifest_path, expected=None):
    mf=read_json(Path(manifest_path))
    require(mf.get('schema')==SOURCE_SCHEMA,'SOURCE_MANIFEST_SCHEMA')
    entries=mf.get('sources'); require(isinstance(entries,list) and entries,'SOURCE_EMPTY')
    ids=set(); paths=set(); verified=[]
    for e in entries:
        require(isinstance(e,dict),'SOURCE_RECORD_NOT_OBJECT')
        sid,rel=e.get('source_id'),e.get('path')
        require(isinstance(sid,str) and sid and sid not in ids,'SOURCE_DUPLICATE_ID')
        require(rel not in paths,'SOURCE_DUPLICATE_PATH')
        require(sha(e.get('sha256')),'SOURCE_SHA_INVALID:'+sid)
        data=safe_file(Path(source_root),rel).read_bytes()
        require(digest(data)==e['sha256'],'SOURCE_SHA_MISMATCH:'+sid)
        require(len(data)==e.get('bytes'),'SOURCE_BYTECOUNT_MISMATCH:'+sid)
        try: lc=len(data.decode('utf-8-sig').splitlines())
        except UnicodeError as err: raise GuardError('SOURCE_UTF8_INVALID:'+sid) from err
        require(lc==e.get('lines'),'SOURCE_LINECOUNT_MISMATCH:'+sid)
        ids.add(sid);paths.add(rel);verified.append(sid)
    declaration=mf.get('required_source_set')
    if declaration=='CORE16':
        require(isinstance(expected,dict) and len(expected)==16,'CORE16_PIN_SET_UNBOUND')
        require(set(verified)==set(expected),'CORE16_ID_SET_INCOMPLETE')
        for e in entries:
            pins=expected[e['source_id']]
            require(e['sha256']==pins['sha256'] and e['path']==pins['path'],'CORE16_PIN_MISMATCH:'+e['source_id'])
        return {'status':'CORE16_LOCAL_BYTE_IDENTITY_ONLY','count':len(verified),'original_reader':'UNBOUND'}
    require(declaration=='SELECTED_ONLY','SOURCE_SET_DECLARATION_REQUIRED')
    require(mf.get('coverage_claim')=='PARTIAL_SOURCE_SET_ONLY','FULL_COVERAGE_FALSE_CLAIM')
    return {'status':'SELECTED_SOURCE_BYTES_CHECK_ONLY','count':len(verified),'original_reader':'UNBOUND'}

def read_doc(pack, rel, want):
    p=safe_file(pack,rel)
    raw=p.read_bytes()
    require(digest(raw)==want,'FILE_DIGEST_MISMATCH:'+rel)
    try: body=raw.decode('utf-8-sig')
    except UnicodeError as e: raise GuardError('DOC_UTF8:'+rel) from e
    m=IDENT.search(body[:900])
    require(m is not None,'DOC_IDENTITY_HEADER_MISSING:'+rel)
    try: ident=json.loads(m.group(1),object_pairs_hook=unique_pairs)
    except json.JSONDecodeError as e: raise GuardError('DOC_IDENTITY_BAD:'+rel) from e
    require(ident==identity(ident),'DOC_IDENTITY_NOT_EXACT:'+rel)
    require(ident==want['identity'] if isinstance(want,dict) else True,'DOC_IDENTITY_MISMATCH')
    return body,ident

def meaningful(body,rel,ident):
    # Strictly rejects placeholders; does not claim to understand arbitrary human prose.
    require(len(body.splitlines())>=9 and len(body)>180,'SUBSTANCE_MISSING:'+rel)
    banned=('TODO','TBD','FILL_ME','<placeholder>','全部待補','此處填入','lorem ipsum')
    require(not any(x.lower() in body.lower() for x in banned),'PLACEHOLDER_BODY:'+rel)
    sections=[x.strip() for x in body.splitlines() if x.startswith('## ')]
    require(len(set(sections))>=2,'BODY_SECTIONS_MISSING:'+rel)
    if rel in ('03_DEV_ECP.md','04_OPS_ECP.md'):
        for name in ('Applicability:','Preconditions:','Postconditions:','Permission:','Readback:','Recovery:'):
            require(name in body,'ECP_SUBSTANCE_FIELD_MISSING:'+rel+':'+name)
    if rel=='05_PLANNED_TQAEP.md':
        for name in ('Requirement:','Case:','Oracle:','POS:','NEG:','ExpectedRaw:','Checker:'):
            require(name in body,'TQAEP_SUBSTANCE_FIELD_MISSING:'+name)
    # Reference marker describes concrete Operation/Output/Consumer/NEG/FirstFail; no semantic PASS.
    for key in ('Input:','Operation:','Output:','Consumer:','NEG:','FirstFail:'):
        require(key in body,'BODY_CONTRACT_FIELD_MISSING:'+rel+':'+key)
    for v in (ident['subject_id'],ident['scope'],ident['batch_id']):
        require(v in body,'BODY_IDENTITY_NOT_VISIBLE:'+rel)

def validate_cases(pack,cases,ident):
    require(isinstance(cases,list) and len(cases)>=2,'CASES_EMPTY')
    ids=set();kinds=set()
    for c in cases:
        require(isinstance(c,dict),'CASE_NOT_OBJECT')
        cid=c.get('case_id')
        require(isinstance(cid,str) and cid and cid not in ids,'CASE_ID_BAD_OR_DUPLICATE')
        ids.add(cid);kinds.add(c.get('kind'))
        require(c.get('kind') in CASE_KINDS,'CASE_KIND_INVALID:'+cid)
        require(c.get('subject_id')==ident['subject_id'] and c.get('scope')==ident['scope'],'CASE_SCOPE_MISMATCH:'+cid)
        require(isinstance(c.get('requirement_ref'),str) and c['requirement_ref'].strip(),'CASE_REQUIREMENT_UNBOUND:'+cid)
        require(isinstance(c.get('expected_raw'),dict) and c['expected_raw'],'CASE_EXPECTED_RAW_EMPTY:'+cid)
        for stem in ('oracle','fixture'):
            ref=c.get(stem+'_path');pin=c.get(stem+'_sha256')
            require(sha(pin),'CASE_'+stem.upper()+'_SHA_BAD:'+cid)
            require(digest(safe_file(pack,ref).read_bytes())==pin,'CASE_'+stem.upper()+'_PIN_MISMATCH:'+cid)
    require({'POS','NEG'}.issubset(kinds),'POS_NEG_PAIR_INCOMPLETE')
    return {c['case_id']:c for c in cases}

def check_pack(pack_root):
    pack=Path(pack_root).resolve(strict=True)
    fm=read_json(safe_file(pack,'PACKAGE_FILE_MANIFEST.json'))
    require(fm.get('schema')==FILE_SCHEMA,'FILE_MANIFEST_SCHEMA')
    wave=read_json(safe_file(pack,'00_WAVE_RUN_MANIFEST.json'))
    require(wave.get('schema')==CONTROL_SCHEMA,'WAVE_CONTROL_ABI_MISMATCH')
    ident=identity(wave)
    require(fm.get('identity')==ident,'FILE_MANIFEST_IDENTITY_MISMATCH')
    required=set(DOC_FIXED)|set(JSON_FIXED)|{ident['wave_id']+'_START_THIN_PROMPT.md'}
    files=fm.get('files')
    require(isinstance(files,list),'FILE_SET_EMPTY')
    declared={}
    for e in files:
        require(isinstance(e,dict) and isinstance(e.get('path'),str) and sha(e.get('sha256')),'FILE_PIN_INVALID')
        require(e['path'] not in declared,'FILE_DUPLICATE')
        declared[e['path']]=e['sha256']
    require(required.issubset(declared),'REQUIRED_FILE_MISSING:'+','.join(sorted(required-set(declared))))
    for rel,pin in declared.items():
        require(digest(safe_file(pack,rel).read_bytes())==pin,'PACK_DIGEST_MISMATCH:'+rel)
    docs={}
    for rel in sorted(x for x in required if x.endswith('.md')):
        raw=safe_file(pack,rel).read_text(encoding='utf-8-sig')
        m=IDENT.search(raw[:900]);require(m is not None,'DOC_IDENTITY_HEADER_MISSING:'+rel)
        try: docident=json.loads(m.group(1),object_pairs_hook=unique_pairs)
        except json.JSONDecodeError as e: raise GuardError('DOC_IDENTITY_BAD:'+rel) from e
        require(docident==ident,'CONTRACT_SCOPE_MISMATCH:'+rel)
        meaningful(raw,rel,ident)
        docs[rel]=raw
    # NO positive original claims even if caller supplies realistic receipt objects.
    claims=wave.get('claims')
    require(isinstance(claims,dict),'CLAIMS_REQUIRED')
    require(set(claims)=={'local_observed','native_observed','independent_accepted','released'},'CLAIMS_DIMENSIONS_INVALID')
    require(all(type(x) is bool for x in claims.values()),'CLAIM_TYPE_BAD')
    require(not any(claims.values()),'ORIGINAL_OR_LOCAL_SUCCESS_CLAIM_UNVERIFIED')
    for key in ('execution_admission_receipt','independent_checker_receipt','publisher_receipt','verified_original_receipt_ref'):
        require(wave.get(key) is None,'ORIGINAL_RECEIPT_UNVERIFIABLE:'+key)
    require(wave.get('claim_ceiling')=='AUTHOR_DESIGN_ONLY','CLAIM_CEILING_EXCEEDED')
    require(wave.get('effect_analysis') in EFFECTS,'EFFECT_UNKNOWN')
    require(wave.get('original_reader_state')=='UNBOUND','READER_STATE_CANNOT_BE_VERIFIED_HERE')
    require(wave.get('source_set_state') in ('CORE16_VERIFIED_LOCAL','SELECTED_ONLY'),'SOURCE_SET_STATE_UNKNOWN')
    # Must match the literal SHA of the pinned selected source manifest file within pack.
    src=safe_file(pack,'SOURCE_MANIFEST.json')
    require(digest(src.read_bytes())==wave['source_manifest_sha256'],'SOURCE_MANIFEST_SHA_MISMATCH')
    srcrec=read_json(src)
    require(srcrec.get('schema')==SOURCE_SCHEMA,'SOURCE_MANIFEST_SCHEMA_MISMATCH')
    if wave['source_set_state']=='CORE16_VERIFIED_LOCAL':
        require(srcrec.get('required_source_set')=='CORE16','SOURCE_SET_FALSE_CLAIM')
        # Core16 is verified by the separately pinned inventory command; never trust wave caller alone.
        raise GuardError('CORE16_CLAIM_REQUIRES_PINNED_INVENTORY_AND_ORIGINAL_READER')
    else:
        require(srcrec.get('required_source_set')=='SELECTED_ONLY','SOURCE_SET_FALSE_CLAIM')
        check_inventory(pack,src)
    source_lookup={e['sha256']:safe_file(pack,e['path']) for e in srcrec['sources']}
    refs=read_json(safe_file(pack,'02_ORIGINAL_CONTRACT_REFS.json'))
    require(refs.get('identity')==ident,'ORIGINAL_REFS_SCOPE_MISMATCH')
    for name in ('original_pi_ref','original_pd_ref','original_ecp_ref','original_tqaep_ref'):
        require(name in refs,'ORIGINAL_REF_FIELD_MISSING:'+name)
        require(refs[name] is None,'ORIGINAL_REF_NOT_VERIFIED_BY_GUARD:'+name)
    tqaep=read_json(safe_file(pack,'05_PLANNED_TQAEP.json'))
    require(tqaep.get('schema')==TQAEP_SCHEMA,'TQAEP_ABI_MISMATCH')
    require(tqaep.get('identity')==ident,'TQAEP_SCOPE_MISMATCH')
    require(tqaep.get('original_tqaep_ref')==refs['original_tqaep_ref'],'TQAEP_ORIGINAL_REF_DRIFT')
    require(tqaep.get('projection_of_sha256')==digest(safe_file(pack,'05_PLANNED_TQAEP.md').read_bytes()),'TQAEP_BODY_MISMATCH')
    require(tqaep.get('cases')==wave.get('cases'),'TQAEP_CASE_MISMATCH')
    cases=validate_cases(pack,wave.get('cases'),ident)
    for cid,c in cases.items():
        pin=c.get('requirement_source_sha256')
        require(pin in source_lookup,'CASE_SOURCE_NOT_IN_SELECTED_MANIFEST:'+cid)
        source_lines=source_lookup[pin].read_text(encoding='utf-8-sig').splitlines()
        start,end=c.get('clause_start_line'),c.get('clause_end_line')
        require(type(start) is int and type(end) is int and 1<=start<=end<=len(source_lines),'CASE_SOURCE_SPAN_INVALID:'+cid)
        clause=c.get('clause_text')
        require(isinstance(clause,str) and clause.strip() and clause == '\n'.join(source_lines[start-1:end]),'CASE_SOURCE_CLAUSE_MISMATCH:'+cid)
        oracle=read_json(safe_file(pack,c['oracle_path']))
        require(oracle.get('first_fail')==c['expected_raw'].get('first_fail'),'CASE_ORACLE_FIRSTFAIL_MISMATCH:'+cid)
    # Only locally linked observations; never interprets a 'command' string as proof it ran.
    obs=wave.get('observations',[]); require(isinstance(obs,list),'OBSERVATIONS_BAD')
    occupied=set()
    for o in obs:
        require(isinstance(o,dict),'OBSERVATION_BAD')
        cid=o.get('case_id'); require(cid in cases,'OBSERVATION_CASE_UNKNOWN')
        case=cases[cid]
        require(o.get('subject_id')==ident['subject_id'] and o.get('scope')==ident['scope'],'OBSERVATION_SCOPE_DRIFT')
        require(o.get('oracle_sha256')==case['oracle_sha256'] and o.get('fixture_sha256')==case['fixture_sha256'],'OBSERVATION_ORACLE_OR_FIXTURE_MISMATCH')
        require(isinstance(o.get('command'),str) and o['command'].strip() and type(o.get('exit')) is int,'OBSERVATION_COMMAND_OR_EXIT_INVALID')
        rp=o.get('raw_path');require(isinstance(rp,str),'OBSERVATION_RAW_PATH_MISSING')
        require(sha(o.get('raw_sha256')) and digest(safe_file(pack,rp).read_bytes())==o['raw_sha256'],'OBSERVATION_RAW_PIN_MISMATCH')
        require(rp not in occupied,'RAW_REUSED_ACROSS_CASES')
        occupied.add(rp)
    # Positive local linkage is not a native invocation or OriginalReader proof.
    return {'status':'AUTHOR_LOCAL_LINKS_ONLY','claim_ceiling':'AUTHOR_DESIGN_ONLY',
            'wave':ident['wave_id'],'case_count':len(cases),'observation_count':len(obs),
            'original_reader':'UNBOUND','native':'NOT_VERIFIED','release':'NOT_GRANTED'}

def run_cli():
    p=argparse.ArgumentParser()
    sub=p.add_subparsers(dest='task',required=True)
    x=sub.add_parser('inventory');x.add_argument('--source-root',required=True);x.add_argument('--manifest',required=True);x.add_argument('--expected-core16',default=None)
    y=sub.add_parser('check-pack');y.add_argument('--pack-root',required=True)
    a=p.parse_args()
    try:
        if a.task=='inventory':
            pins=None
            if a.expected_core16:
                raw=read_json(Path(a.expected_core16)); pins=raw.get('pins')
            v=check_inventory(a.source_root,a.manifest,pins)
        else: v=check_pack(a.pack_root)
        print(json.dumps(v,ensure_ascii=False,sort_keys=True));return 0
    except (GuardError,OSError,KeyError,TypeError,ValueError) as e:
        print(json.dumps({'status':'AUTHOR_GUARD_FAIL_CLOSED','first_fail':str(e),'claim_ceiling':'AUTHOR_DESIGN_ONLY'},ensure_ascii=False));return 2

if __name__=='__main__':sys.exit(run_cli())

