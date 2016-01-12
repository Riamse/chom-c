import subprocess as sp
import multiprocessing as mp
import os

from c import new_c

TPL = "/tmp/test.{}.c"
OTPL = "/tmp/{}.out"
total = 1000

def zillion_tests(retplace, pid, count):
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
    except:
        retplace.put((pid, 0))
        return
    os.unlink(fn)
    os.unlink(outfile)
    retplace.put((pid, 1))

cpus = mp.cpu_count()
total //= cpus
q = mp.Queue(cpus)

print("%d cores, %d processes for each core" % (cpus, total))

for i in range(cpus):
    mp.Process(target=zillion_tests, args=[q, i, total]).start()

for i in range(cpus):
    k, v = q.get()
    if v == 0:
        print("Process #{} failed".format(k))
    elif v == 1:
        print("Process #{} succeeded".format(k))

