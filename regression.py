# Regression test

import os, sys
from subprocess import *

files = filter(lambda x: '_test' in x, os.listdir('scripts/'))
cmd = 'python interpreter.py'
count = 0
server = Popen(['python', 'server.py', '14215'], stdout=None, stderr=None)

for fname in files:
    sys.stderr.write('Running test case %s...' % fname)
    fin = open('scripts/' + fname, 'r')
    p = Popen(['python', 'interpreter.py'], stdout=PIPE, stderr=PIPE, stdin=fin)
    p.stderr.read()
    status = os.waitpid(p.pid, 0)[1]
    if status == 0:
        sys.stderr.write('passed.\n')
        count += 1
    else:
        sys.stderr.write('failed, error code=%d\n' % status)

sys.stderr.write('\n')
sys.stderr.write('-' * 40 + '\n')
sys.stderr.write('%d/%d cases passed.\n' % (count, len(files)))
