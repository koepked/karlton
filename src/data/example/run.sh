#!/bin/bash

#SBATCH -N 2
#SBATCH -t 0-00:05
#SBATCH -o karlton.out

date

#echo
#echo "-------------------------"
#echo "All SLURM Environment Variables"
#echo "-------------------------"
#printenv | grep SLURM

mpirun --allow-run-as-root karlton

# Wait for any background jobs
wait

exit 0
