from .reduction import register as register
from _typeshed import Incomplete

HAVE_SEND_HANDLE: Incomplete

def DupFd(fd): ...
def rebuild_connection(df, readable, writable): ...
def reduce_connection(conn): ...
