import subprocess as sp
import multiprocessing as mp
import os

from c import new_c

TPL = "/tmp/test.{}.c"
OTPL = "/tmp/{}.out"
total = 1000

def zillion_tests(pid, count):
    fn = TPL.format(pid)
    outfile = OTPL.format('abcdefghijklmnopqrstuvwxyz'[pid])
    g = new_c()
    def do_crap():
        for i in range(count):
            with open(fn, 'w') as fp:
                print(''.join(g.expand("$FILE")), file=fp)
            sp.check_call(['gcc', fn, '-o', outfile])
    try:
        do_crap()
    finally:
        os.unlink(fn)
        os.unlink(outfile)

cpus = mp.cpu_count()
total //= cpus

for i in range(cpus):
    mp.Process(target=zillion_tests, args=[i, total]).start()

