from io import BytesIO
import zipfile
from urllib import request as urlreq, parse as urlparse
from pathlib import PurePath, Path
from typing import List, Tuple, Optional


def extract_single(f: zipfile.ZipFile, name: str, dest: str):
    b = f.read(name)

    p = Path(dest, PurePath(name).name)
    p.parent.mkdir(parents=True, exist_ok=True)

    with p.open('wb') as file:
        file.write(b)


def extract(f: zipfile.ZipFile, name: str, dest: str):
    """Extract a file NODE or files of subtree rooted at NODE to PATH
    """
    if f.getinfo(name).is_dir():
        parentname = name
        for childname in filter(lambda e: e.startswith(parentname), f.namelist()):
            if f.getinfo(childname).is_dir():
                continue

            b = f.read(childname)

            p = Path(dest, PurePath(parentname).name, './' + childname.replace(parentname, ''))
            p.parent.mkdir(parents=True, exist_ok=True)

            with p.open('wb') as file:
                file.write(b)
    else:
        b = f.read(name)

        p = Path(dest, PurePath(name).name)
        p.parent.mkdir(parents=True, exist_ok=True)

        with p.open('wb') as file:
            file.write(b)


def url_to_destdir(url: str, dest: str):
    u = urlparse.urlparse(url)
    name = PurePath(u.path).name
    with urlreq.urlopen(url) as f:
        b = f.read()
    
    Path(dest).mkdir(parents=True, exist_ok=True)
    with Path(dest, name).open('wb') as f:
        f.write(b)
    

def urlzip_to_destdir(url: str, namedestpairs: List[Tuple[str, str]]):
    with urlreq.urlopen(url) as f:
        b = f.read()

    zf = zipfile.ZipFile(BytesIO(b))
    for name, dest in namedestpairs:
        extract(zf, name, dest)


class FromFile:

    def __init__(self, url_debug: str, url_release: str, dest: str):
        self.url_debug = url_debug
        self.url_release = url_release
        self.dest = dest
    
    def drop(self, is_debug: bool):
        url = self.url_debug if is_debug else self.url_release
        url_to_destdir(url, self.dest)


class FromZip:
    
    def __init__(
        self,
        url_debug: str,
        url_release: str,
        name: Optional[str] = None,
        dest: Optional[str] = None,
        *,
        namedestpairs: Optional[List[Tuple[str, str]]] = None,
    ):
        self.url_debug = url_debug
        self.url_release = url_release
        if namedestpairs:
            self.namedestpairs = namedestpairs
        else:
            self.namedestpairs = [(name, dest)]
    
    def drop(self, is_debug: bool):
        url = self.url_debug if is_debug else self.url_release
        urlzip_to_destdir(url, self.namedestpairs)
