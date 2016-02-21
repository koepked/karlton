#!/usr/bin/env python

import sys
from subprocess import call

HOST_FILE = '/etc/hosts'

with open(HOST_FILE, 'r') as f:
    lines = filter(lambda x:
        'karlton' in x and len(x.split()) == 3 and 'bridge' not in x,
        list(f)[1:])

for line in lines:
    call(['ssh', line.strip().split()[1], '"exit"'])
