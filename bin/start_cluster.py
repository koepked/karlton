#!/usr/bin/env python
"""Launch a container-based virtual HPC cluster.

Usage: bin/start_cluster.py NUM_NODES

Uses Docker to build images and launch containers. Launched cluster will be
composed of a data volume, head node, and NUM_NODES compute nodes.
"""
import argparse
import os
import sys
from subprocess import call

TMP_MPI_HOSTFILE = 'temp-mpi-hosts'

if __name__ == '__main__':
	descrip = 'Launch a container-based virtual HPC cluster.'
	parser = argparse.ArgumentParser(prog='bin/start_cluster.py',
									 description=descrip)
	parser.add_argument('num_nodes', help='Number of compute nodes to launch',
						type=int)
	args = parser.parse_args(args=sys.argv[1:])
	compute_nodes = ['karlton-node%d' % i for i in range(args.num_nodes)]
	data_mount = '/karlton'
	data_name = 'karlton-data'
	net_name = 'karlton_net'
	node_image_dir = 'src/docker'
	data_image_dir = 'src/data'
	hosts_file = 'src/data/hosts'

	# Build hosts file.
	with open(hosts_file, 'w') as f:
	    for node in compute_nodes:
	        f.write('%s\n' % node)

	# Build node image.
	ret = call(['docker', 'build', '-t', 'karlton', node_image_dir])
	if ret != 0:
	    print 'ERROR: node image build error: %d' % ret
	    sys.exit(1)

	# Build data volume image.
	ret = call(['docker', 'build', '-t', data_name, data_image_dir])
	if ret != 0:
	    print 'ERROR: data volume image build error: %d' % ret
	    sys.exit(1)
	
	# Create network.
	ret = call(['docker', 'network', 'create', '--driver', 'bridge', net_name])
	if ret != 0:
	    print 'ERROR: network creation error: %d' % ret
	    sys.exit(1)

	# Launch data volume for shared files.
	call(['docker', 'create', '-v', data_mount, '--name', data_name,
		  'karlton-data', '/bin/true'])

	# Launch compute nodes.
	for node in compute_nodes:
		namearg = '--name=%s' % node
		hostnamearg = '--hostname=%s' % node
		ret = call(['docker', 'run', namearg, hostnamearg, '-d',
		            '--volumes-from', data_name, '--net=%s' % net_name, 'karlton',
		            '/usr/sbin/sshd', '-D'])
        if ret != 0:
            print ('ERROR: launch of compute node %s failed with error: %d'
                   % (node, ret))
            sys.exit(1)
	
	# Launch head node.
	args = ['docker', 'run', '--name=karlton-head', '--hostname=karlton-head',
	        '-i', '-t', '--rm=true', '--net=%s' % net_name]
	args += ['--volumes-from', data_name]
	args += ['karlton', '/bin/bash', '-l']
	ret = call(args)
	if ret != 0:
	    print 'ERROR: launch of head node failed: %d' % ret
	    sys.exit(1)

	# Cleanup.
	print 'Stopping containers:'
	call(['docker', 'stop'] + compute_nodes)
	call(['docker', 'stop', 'karlton-data'])
	print 'Removing containers:'
	call(['docker', 'rm'] + compute_nodes)
	call(['docker', 'rm', '-v', data_name])
	print 'Shutting down created docker network %s' % net_name
	call(['docker', 'network', 'rm', net_name])
