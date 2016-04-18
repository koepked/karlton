#!/usr/bin/env python

import sys, os

DIR = sys.argv[1]
OUT_FILE = 'condensed_results'

if __name__ == '__main__':
    data = []
    files = [f for f in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, f))]
    for f in files:
	with open(os.path.join(DIR, f), 'r') as content:
                data.append("%s: %s" % (f,
		content.read().split('Time in seconds =')[1].strip().split()[0]))
    data.sort()
    with open(OUT_FILE, 'a') as out:
        out.write('\n'.join(data))
