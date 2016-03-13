#!/usr/bin/env python
"""Launch a container-based virtual HPC cluster."""

import sys
from subprocess import call

if __name__ == '__main__':
	image_dir = './'
	image_name = 'karlton'
	node_name_prefix = '%s-node' % image_name
	head_name = '%s-head' % image_name
	net_name = '%s-net' % image_name
	num_nodes_per_host = int(sys.argv[1])

	# Setup shared files
	with open('/shared/shared/touch_nodes.sh', 'w') as f:
		for i in range(num_nodes_per_host * 2):
			f.write('ssh karlton-node%d\n' % i)

	# Build image
	#ret = call(['docker', 'build', '-t', image_name, image_dir])
	#if ret != 0:
	    #print 'ERROR: image build error: %d' % ret
	    #sys.exit(1)

	# Start cluster network
	#ret = call(['docker', 'network', 'create', '--driver=overlay',
		    #'--subnet=10.0.0.0/16', net_name])

	# Launch compute nodes.
	for i in range(num_nodes_per_host):
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
