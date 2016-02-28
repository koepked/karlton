#!/usr/bin/env python

from subprocess import check_output, STDOUT

HOST_FILE = '/karlton/hosts'

with open(HOST_FILE, 'r') as f:
    for line in f:
        hostname = line.strip()
        check_output(['ssh', hostname, '"exit"'], stderr=STDOUT)

