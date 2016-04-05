#!/usr/bin/env python
"""Launch a container-based virtual HPC cluster."""

import os
import sys
from subprocess import call

if __name__ == '__main__':
	image_dir = './'
	image_name = 'karlton'
	node_name_prefix = '%s-node' % image_name
	head_name = '%s-head' % image_name
	net_name = '%s-net' % image_name
	num_nodes_host1 = int(sys.argv[1])
	num_nodes_host2 = int(sys.argv[2])
	known_hosts = '/shared/root/.ssh/known_hosts'

	# Setup shared files
	#with open('/shared/shared/touch_nodes.sh', 'w') as f:
		#for i in range(num_nodes_host1 + num_nodes_host2):
			#f.write('ssh karlton-node%d\n' % i)

	# Setup mpi hosts file
	with open('/shared/shared/NAS/mpihosts', 'w') as f:
		for i in range(num_nodes_host1 + num_nodes_host2):
			f.write('karlton-node%d\n' % i)

	# Setup mpi rank file
	with open('/shared/shared/NAS/rankfile', 'w') as f:
		for i in range(num_nodes_host1 + num_nodes_host2):
			f.write('rank %d=karlton-node%d slot=0,1:0-7\n' % (i, i))

	# Clear known_hosts
	if os.path.isfile(known_hosts):
		os.remove(known_hosts)

	# Build image
	#ret = call(['docker', 'build', '-t', image_name, image_dir])
	#if ret != 0:
	    #print 'ERROR: image build error: %d' % ret
	    #sys.exit(1)

	# Start cluster network
	#ret = call(['docker', 'network', 'create', '--driver=overlay',
		    #'--subnet=10.0.0.0/16', net_name])

	# Launch compute nodes.
	for i in range(num_nodes_host1):
		node_name = '%s%d' % (node_name_prefix, i)
		args = ['docker', 'run', '--name=%s' % node_name,
			'--hostname=%s' % node_name, '-d',
			'--net=%s' % net_name,
			'-v', '/shared/shared:/shared',
			'-v', '/shared/root:/root',
			image_name, '/usr/sbin/sshd', '-D']
		ret = call(args)
		if ret != 0:
		    print 'ERROR: launch of %s failed: %d' % (node_name, ret)
		    sys.exit(1)

	# Launch head node.
	args = ['docker', 'run', '--name=%s' % head_name,
	        '--hostname=%s' % head_name, '-i', '-t', '--rm=true',
	        '--net=%s' % net_name,
		'-v', '/shared/shared:/shared',
		'-v', '/shared/root:/root',
	        image_name, '/bin/bash', '-l']
	ret = call(args)
