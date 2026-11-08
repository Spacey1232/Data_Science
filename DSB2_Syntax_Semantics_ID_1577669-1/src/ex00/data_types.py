def data_types():
    a=10
    b=""
    c=1.1
    d=True
    e=[]
    f=dict()
    g=tuple()
    j=set()
    list_str = [type(a).__name__, type(b).__name__, type(c).__name__, type(d).__name__, type(e).__name__, type(f).__name__, type(g).__name__, type(j).__name__]
    print("[" + ", ".join(list_str) + "]")


if __name__ == '__main__':
     data_types()