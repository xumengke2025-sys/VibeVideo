from pathlib import Path
import urllib.request,zipfile,io,json
R=Path(__file__).resolve().parent
URL='https://github.com/nihui/rife-ncnn-vulkan/releases/download/20221029/rife-ncnn-vulkan-20221029-windows.zip'
SIZE=431540241
class RangeFile(io.RawIOBase):
    def __init__(self):self.pos=0;self.url=URL;self.transferred=0
    def seekable(self):return True
    def tell(self):return self.pos
    def seek(self,n,whence=0):
        self.pos=n if whence==0 else self.pos+n if whence==1 else SIZE+n
        return self.pos
    def read(self,n=-1):
        n=SIZE-self.pos if n<0 else min(n,SIZE-self.pos)
        if not n:return b''
        req=urllib.request.Request(self.url,headers={'Range':f'bytes={self.pos}-{self.pos+n-1}','User-Agent':'Codex-video-build'})
        with urllib.request.urlopen(req,timeout=90) as response:
            if response.status!=206:raise RuntimeError(f'Range unsupported: {response.status}')
            self.url=response.url
            data=response.read(n)
        self.pos+=len(data);self.transferred+=len(data)
        return data
p=R/'.tools/rife/release.zip'
remote=None
if p.exists() and zipfile.is_zipfile(p):z=zipfile.ZipFile(p)
else:remote=RangeFile();z=zipfile.ZipFile(remote)
with z:
    names=[n for n in z.namelist() if n.endswith('.exe') or '/rife-v4.6/' in n or n.lower().endswith(('license','license.txt','readme.md'))]
    if not any('/rife-v4.6/' in n for n in names):
        print(json.dumps({'model_directories':sorted({n.split('/')[-2] for n in z.namelist() if n.endswith('.param')})}))
        names=[n for n in z.namelist() if n.endswith('.exe') or '/rife-v4/' in n or n.lower().endswith(('license','license.txt','readme.md'))]
    target=R/'.tools/rife/runtime';target.mkdir(parents=True,exist_ok=True)
    for name in names:
        if name.endswith('/'):continue
        path=Path(name);dest=target/Path(*path.parts[1:]);dest.parent.mkdir(parents=True,exist_ok=True)
        with z.open(name) as source:dest.write_bytes(source.read())
    print(json.dumps({'files':names,'transferred':remote.transferred if remote else 'local archive'}))
