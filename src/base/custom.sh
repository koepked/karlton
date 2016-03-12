. /etc/profile.d/modules.sh
module load /etc/modulefiles/mpi/openmpi-x86_64
/usr/sbin/munged
if [ $(hostname) = karlton-head ]
then
    /usr/sbin/slurmctld
    /root/touch_nodes.py
else
    /usr/sbin/slurmd
fi
