import subprocess as sp

from c import g


for i in range(100000):
    with open("/tmp/test.c", "w") as fp:
        print(''.join(g.expand("$FILE")), file=fp)
    sp.check_call(["gcc", "/tmp/test.c", '-o', '/tmp/a.out'])
