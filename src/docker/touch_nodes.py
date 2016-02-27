#!/usr/bin/env python

import sys
from subprocess import call

HOST_FILE = '/karlton/hosts'
KNOWN_HOSTS_FILE = '~/.ssh/known_hosts'

with open(HOST_FILE, 'r') as f:
    for line in f:
        call(['ssh-keyscan', line, '>>', KNOWN_HOSTS_FILE])

