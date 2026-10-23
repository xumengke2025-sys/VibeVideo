import sys,json,zipfile,pathlib,hashlib
archive,tree_path,dest,repo,commit=sys.argv[1:]
target=pathlib.Path(dest).resolve();target.mkdir(parents=True,exist_ok=True)
tree=json.loads(pathlib.Path(tree_path).read_text(encoding='utf-8'));expected={x['path']:x for x in tree['tree'] if x['type']=='blob'};files=[]
with zipfile.ZipFile(archive) as z:
    for item in z.infolist():
        if item.is_dir():continue
        rel=item.filename.split('/',1)[1] if '/' in item.filename else ''
        if rel not in expected:continue
        p=(target/rel).resolve()
        if not p.is_relative_to(target):raise ValueError('Unsafe archive path')
        data=z.read(item);sha1=hashlib.sha1(('blob '+str(len(data))+'\0').encode()+data).hexdigest()
        if sha1!=expected[rel]['sha']:raise ValueError('Git blob mismatch: '+rel)
        p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        files.append({'path':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'gitBlob':sha1,'lfsPointer':data.startswith(b'version https://git-lfs.github.com/spec/v1')})
if len(files)!=len(expected):raise ValueError('Archive incomplete')
(target/'SOURCE.json').write_text(json.dumps({'repo':repo,'repository':'https://github.com/'+repo,'commit':commit,'scope':'固定commit完整仓库文件快照；LFS指针按Git原样保存，实际视频另行取证','executed':False,'files':files},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'repo':repo,'files':len(files),'gitBlobsVerified':True,'bytes':sum(x['bytes'] for x in files)}))
