#!/usr/bin/env python

import argparse
import os
import sys
from subprocess import call, check_output
from tempfile import mkstemp

script_name = 'net_setup.sh'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('hosts_file')
    parser.add_argument('bridge_name')
    parser.add_argument('net')
    parser.add_argument('interface')
    args = parser.parse_args(sys.argv[1:])

    with open(args.hosts_file, 'r') as f:
        hosts = map(lambda x: x.strip(), f.readlines())


    for host in hosts:
        node_num = hosts.index(host)

        command = (
            '#!/bin/bash\n'
            'brctl addbr %s\n'
            'brctl addif %s %s\n'
            'ip addr add dev %s %s.%d.0/16\n'
            'ip link set up dev %s\n'
            'service docker stop\n'
            'docker daemon -b %s --fixed-cidr=%s.%d.0/24 &\n'
        ) % (args.bridge_name, args.bridge_name, args.interface,
             args.bridge_name, args.net, node_num, args.bridge_name,
             args.bridge_name, args.net, node_num)

        (fd, fname) = mkstemp()
        os.write(fd, command)
        os.close(fd)
        call(['scp', fname, '%s:%s' % (host, script_name)])
        os.remove(fname)
        call(['ssh', host, 'chmod +x %s' % script_name])

