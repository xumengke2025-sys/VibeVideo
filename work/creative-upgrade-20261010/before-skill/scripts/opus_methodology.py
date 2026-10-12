"""Bounded methodology/source retrieval. No network, third-party execution or render."""
import argparse
import hashlib
import json
import re
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]

def read(relative):
    return json.loads((SKILL / relative).read_text(encoding='utf-8'))

def source_info(source, ref=None):
    root = source.get('local_root')
    out = {k: source[k] for k in ('id','repository','commit','relation','runtime','scope')}
    for key in ('commit_date','repository_created','reference_role','quality_evidence','model_attribution','license_note','inspected'):
        if key in source: out[key] = source[key]
    if root:
        out['local'] = str((SKILL / root / (ref['path'] if ref else '')).resolve())
    if ref:
        out['line'] = ref['line']
        if source['repository']:
            out['url'] = source['repository'] + '/blob/' + source['commit'] + '/' + ref['path'] + '#L' + str(ref['line'])
    return out

def validate(lib, index, gallery):
    errors=[]
    cards={x['id']:x for x in lib['cards']}
    entries={x['slug']:x for x in gallery['entries']}
    if len(cards) != len(lib['cards']): errors.append('duplicate card IDs')
    if len(index['entries']) != len(entries): errors.append('catalogue/index coverage mismatch')
    if len({x['slug'] for x in index['entries']}) != len(index['entries']): errors.append('duplicate index slugs')
    hashes=0
    for sid,s in lib['sources'].items():
        if s['commit'] and not re.fullmatch('[a-f0-9]{40}',s['commit']): errors.append('bad commit '+sid)
        if not s['local_root'] or sid=='codex-tools': continue
        root=SKILL/s['local_root']
        manifest=read(str(root.relative_to(SKILL)/'SOURCE.json'))
        if manifest['commit']!=s['commit']: errors.append('manifest commit mismatch '+sid)
        if (manifest.get('repository') or manifest.get('repo'))!=s['repository']: errors.append('manifest repository mismatch '+sid)
        for row in manifest['files']:
            # Earlier manifests use `path`; new archives use explicit local_path.
            rel=row.get('local_path') or row.get('path') or row.get('source_path')
            p=root/rel
            if not p.is_file(): errors.append('missing source '+str(p)); continue
            if hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']: errors.append('changed source '+str(p))
            hashes+=1
    for c in cards.values():
        for slug in c['gallery_slugs']:
            if slug not in entries: errors.append('missing card case '+slug)
        for ref in c['source_refs']:
            s=lib['sources'].get(ref['source'])
            if not s: errors.append('unknown source '+ref['source']); continue
            if s['local_root']:
                p=SKILL/s['local_root']/ref['path']
                if not p.is_file(): errors.append('missing card anchor '+str(p))
                elif len(p.read_text(encoding='utf-8').splitlines())<ref['line']: errors.append('line outside source '+str(p))
    for row in index['entries']:
        x=entries.get(row['slug'])
        if not x: errors.append('unknown index slug '+row['slug']); continue
        if row['prompt_sha256']!=hashlib.sha256(x['prompt'].encode()).hexdigest(): errors.append('prompt changed '+row['slug'])
        for c in row['candidate_cards']:
            if c['card'] not in cards: errors.append('unknown candidate card '+c['card'])
            if c['text'] not in x['prompt']: errors.append('candidate excerpt not verbatim '+row['slug'])
        if row['source_id'] and row['source_id'] not in lib['sources']: errors.append('unknown indexed source '+row['slug'])
        if row['tech_tags_used_for_original_provenance']: errors.append('remake tags misused '+row['slug'])
        if row['pixel_match_verified']: errors.append('unsupported pixel verification '+row['slug'])
    if index['catalogue_commit']!=gallery['provenance']['commit']: errors.append('snapshot mismatch')
    return {'ok':not errors,'cards':len(cards),'indexed_rows':len(entries),'source_hashes_checked':hashes,'errors':errors}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('stats'); sub.add_parser('validate')
    rec=sub.add_parser('recommend'); rec.add_argument('--query',required=True)
    rec.add_argument('--limit',type=int,default=4); rec.add_argument('--code-only',action='store_true')
    rec.add_argument('--film-only',action='store_true',help='Only methods anchored in film/film-engine sources; not a quality certification')
    c=sub.add_parser('card'); c.add_argument('id')
    s=sub.add_parser('source'); s.add_argument('id')
    t=sub.add_parser('trace'); t.add_argument('slug')
    args=parser.parse_args()
    lib=read('references/opus-methods.json')
    index=read('references/opus-source-index.json')
    gallery=read('assets/opus-gallery.json')
    card_map={c['id']:c for c in lib['cards']}
    rows={r['slug']:r for r in index['entries']}
    entries={x['slug']:x for x in gallery['entries']}
    if args.command=='stats':
        out={'coverage':lib['reading_scope'],'cards':len(card_map),
             'local_archives':[s['id'] for s in lib['sources'].values() if s['local_root'] and s['id']!='codex-tools'],
             'source_read_only':[s['id'] for s in lib['sources'].values() if s['runtime']=='source_read_only'],
             'reference_roles':{s['id']:s.get('reference_role','unclassified') for s in lib['sources'].values()},
             'quality_evidence':{s['id']:s.get('quality_evidence','unclassified') for s in lib['sources'].values()},
             'scope':index['scope']}
    elif args.command=='validate':
        out=validate(lib,index,gallery)
    elif args.command=='source':
        if args.id not in lib['sources']: parser.error('Unknown source ID: '+args.id)
        out=source_info(lib['sources'][args.id])
    elif args.command=='trace':
        if args.slug not in rows: parser.error('Unknown slug: '+args.slug)
        out={**rows[args.slug], 'post_url':entries[args.slug]['post_url'],
             'source':source_info(lib['sources'][rows[args.slug]['source_id']]) if rows[args.slug]['source_id'] else None}
    elif args.command=='card':
        if args.id not in card_map: parser.error('Unknown card ID: '+args.id)
        c=card_map[args.id]
        out={**c,'source_details':[source_info(lib['sources'][r['source']],r) for r in c['source_refs']]}
    else:
        q=args.query.casefold()
        ranking=[]
        for c in lib['cards']:
            if args.code_only and not c['source_refs']: continue
            if args.film_only and not any(lib['sources'][r['source']].get('reference_role') in ('film','film_engine') for r in c['source_refs']): continue
            matched=[t for t in c['terms'] if (t.casefold() in q if re.search('[\u4e00-\u9fff]',t) else re.search(r'(?<![a-z0-9])'+re.escape(t.casefold())+r'(?![a-z0-9])',q))]
            if matched: ranking.append((sum(min(len(t),5) for t in matched),c,matched))
        ranking.sort(key=lambda r:(-r[0],r[1]['id']))
        selected=ranking[:max(1,min(args.limit,8))]
        out={'query':args.query,'scope':'需求→方法候选；文本匹配分值不是画质评价。请按目的/失败条件选核心机制。',
             'cards':[],'unresolved':'没有匹配时自行建立brief，不以随机热门案例填充。' if not selected else None}
        for _,c,matched in selected:
            refs=[source_info(lib['sources'][r['source']],r) for r in c['source_refs']]
            cases=[]
            for slug in c['gallery_slugs']:
                row=rows[slug]
                # Unknown origins are discovery leads, not evidence for code-only work.
                if args.code_only and (not row['source_id'] or row['original_visual_provenance'] in ('generated_video_required_in_prompt','generated_image_required_in_prompt','video_asset_origin_unknown')):
                    continue
                cases.append({'slug':slug,'url':entries[slug]['skillry_url'],
                              'evidence':'public_brief_only_unless_source_shown','visual_provenance':row['original_visual_provenance']})
            out['cards'].append({'id':c['id'],'title':c['title'],'matched_terms':matched,
                                 'purpose':c['purpose'],'status':c['status'],'sources':refs,'reference_leads':cases[:3]})
    print(json.dumps(out,ensure_ascii=False,indent=2))
    if args.command=='validate' and not out['ok']: raise SystemExit(1)

if __name__=='__main__': main()
