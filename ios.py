import io, struct, fcntl, tempfile
from packer import DevCtl, formatting
import socket, os

def down_to_child(r,w): # TODO implement formatting and struct packing of messages between threads
    os.close(r)
    os.write(w, b"tetw") 

class IO(io.BytesIO):
    def __init__(self, buf):
        buf = io.BytesIO(buf)
        self._io = io.TextIOWrapper(buf)
        self.dev = DevCtl(buf)
        self.size = self._io.read().__len__()
        self._io.seek(0)
        self.tmp_file = tempfile.SpooledTemporaryFile()
        self.tmp_file.write(self._io.read().encode())
        self.fileno = self.tmp_file.fileno()

    def pipe(self):
        fn = fcntl.fcntl(self.tmp_file,1,1)
        pid = os.fork() 
        r,w = os.pipe()
        if pid > 0: 
            os.write(w, b"test")
        else:
            c = 1
            os.close(w)
            while 1:
                val = os.read(r,c)
                print(val)
                c+=1 

    def child_parent(self):
        r,w = os.pipe()
        pid = os.fork()
        if pid > 0:
            down_to_child(r,w)
        else:
            os.close(w)
            r = os.fdopen(r)
            print(r.read())
    def bdir_pipe(self):
        return
    

def main():
    buf =struct.pack("l", 1)
    _io = io.BytesIO(buf)
    fmt=formatting(_io)
    Io = IO(buf)
    Io.pipe()

