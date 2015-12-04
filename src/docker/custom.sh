. /etc/profile.d/modules.sh
module load /etc/modulefiles/mpi/openmpi-x86_64
/usr/sbin/munged
if [ $(hostname) = karlton-head ]
then
    #su -c /usr/sbin/slurmctld slurm
    /usr/sbin/slurmctld
    /root/touch_nodes.py
else
    #su -c /usr/sbin/slurmd slurm
    /usr/sbin/slurmd
fi
