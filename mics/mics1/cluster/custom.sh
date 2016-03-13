cp /shared/munge.key /etc/munge/munge.key
munged

cp /shared/slurm.conf /etc/slurm.conf
chown slurm:slurm /etc/slurm.conf

if [ $(hostname) = karlton-head ]
then
    slurmctld
    sleep 5
    bash /shared/touch_nodes.sh
else
    slurmd
fi
