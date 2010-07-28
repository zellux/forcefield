# Regression test

import os, sys
from subprocess import *

files = filter(lambda x: '_test' in x, os.listdir('scripts/'))
cmd = 'cat scripts/%s | python interpreter.py'
count = 0

for fname in files:
    status = call(cmd % fname, shell=True, stdout=PIPE, stderr=PIPE)
    if status == 0:
        print('Test case %s passed.' % fname)
        count += 1
    else:
        print('Test case %s failed, error code=%d' % (fname, status))

print
print('-' * 40)
print('%d/%d cases passed.' % (count, len(files)))
