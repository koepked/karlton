#!/usr/bin/env python

import argparse, sys

# Possible scenarios:
#
#   1) key/val store already runnning, docker daemon already set with proper
#      engine-opts on all nodes
#   2) key/val store already running, docker daemon needs to be configed with
#      proper engine-opts vals on all nodes
#   3) Nothing is setup yet.
#
# Setting engine-opts is OS-specific, so for now, this script runs under the
# assumption that that's already been taken care of. If it has, then the key/val
# store must already be running, so this script (currently) just sets up the
# virtual cluster network and head/node containers.

if __name__ == '__main__':
    descrip = 'Launch a multihost container-based elastic virtual cluster.'
    hosts_file_help = ('File contiaining list of hosts on which to launch '
                       'compute nodes, one per line.')
    num_nodes_per_host_help = 'Number of compute nodes to launch on each host.'
    net_name_help = 'Name of the overlay network that will be created.'

    parser = argparse.ArgumentParser(prog='start_cluster.py',
                                     description=descrip)
    parser.add_argument('hosts_file', help=hosts_file_help)
    parser.add_argument('num_nodes_per_host', help=num_nodes_per_host_help,
                        type=int)
    parser.add_argument('net_name', help=net_name_help)
    args = parser.parse_args(args=sys.argv[1:])

    hosts_file = args.hosts_file
    num_nodes_per_host = args.num_nodes_per_host
    net_name = args.net_name

    with open(hosts_file) as f:
        host_list = f.readlines()

    print 'Creating overlay network named %s' % net_name

    for host in host_list:
        print ('Launching %d compute node containers on host %s' 
               % (num_nodes_per_host, host))

    print 'Launching head node on localhost'
