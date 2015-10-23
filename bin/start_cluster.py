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
	links = ['karlton-node%d' % i for i in range(args.num_nodes)]
	data_mount = '/karlton'
	data_name = 'karlton-data'

	if not os.path.isdir('build'):
	    os.mkdir('build')

	# Generate mpi-hosts file.
	with open(os.path.join('build', TMP_MPI_HOSTFILE), 'w') as f:
		f.write('\n'.join(links))
	
	# Generate dockerfile for karlton data volume.
	with open(os.path.join('build', 'Dockerfile'), 'w') as f:
	    f.write('FROM karlton\nMAINTAINER karlton\n\n')
	    f.write('ADD %s /karlton/mpi-hosts' % TMP_MPI_HOSTFILE)
	
	# Build base image.
	call(['docker', 'build', '-t', 'karlton', 'src/docker'])

	# Build data volume image with generated mpi-hosts file.
	call(['docker', 'build', '-t', 'karlton-data', 'build'])

	# Launch data volume for shared files.
	call(['docker', 'create', '-v', data_mount, '--name', data_name,
		  'karlton-data', '/bin/true'])

	# Launch compute nodes.
	for link in links:
		namearg = '--name=%s' % link
		hostnamearg = '--hostname=%s' % link
		call(['docker', 'run', namearg, hostnamearg, '-d', '--volumes-from',
			  data_name, 'karlton', '/usr/sbin/sshd', '-D'])
	
	# Launch head node.
	args = ['docker', 'run', '--name=karlton-head', '-i', '-t', '--rm=true']
	args += ['--link=%s:%s' % (link, link) for link in links]
	args += ['--volumes-from', data_name]
	args += ['karlton', '/bin/bash', '-l']
	call(args)

	# Cleanup.
	print 'Stopping containers:'
	call(['docker', 'stop'] + links)
	call(['docker', 'stop', 'karlton-data'])
	print 'Removing containers:'
	call(['docker', 'rm'] + links)
	call(['docker', 'rm', '-v', data_name])
