#!/bin/bash

CLASS=A
NPROCS=128
DIR=../NPB3.3.1/NPB3.3-MPI/bin
RESULTSDIR=results3

## 2^n NPROCS ##################################################################

echo is
date
mpirun -hostfile mpihosts -np $NPROCS --mca btl_tcp_if_include p10p1 --mca rmaps_rank_file_path rankfile $DIR/is.$CLASS.$NPROCS > $RESULTSDIR/is.$CLASS.$NPROCS.results
#mpirun -hostfile mpihosts -np $NPROCS --mca btl_tcp_if_include p10p1 $DIR/is.$CLASS.$NPROCS > $RESULTSDIR/is.$CLASS.$NPROCS.results

echo mg
date
mpirun -hostfile mpihosts -np $NPROCS --mca btl_tcp_if_include p10p1 --mca rmaps_rank_file_path rankfile $DIR/mg.$CLASS.$NPROCS > $RESULTSDIR/mg.$CLASS.$NPROCS.results
#mpirun -hostfile mpihosts -np $NPROCS --mca btl_tcp_if_include p10p1 $DIR/mg.$CLASS.$NPROCS > $RESULTSDIR/mg.$CLASS.$NPROCS.results

echo cg
date
mpirun -hostfile mpihosts -np $NPROCS --mca btl_tcp_if_include p10p1 --mca rmaps_rank_file_path rankfile $DIR/cg.$CLASS.$NPROCS > $RESULTSDIR/cg.$CLASS.$NPROCS.results
#mpirun -hostfile mpihosts -np $NPROCS --mca btl_tcp_if_include p10p1 $DIR/cg.$CLASS.$NPROCS > $RESULTSDIR/cg.$CLASS.$NPROCS.results

echo ft
date
mpirun -hostfile mpihosts -np $NPROCS --mca btl_tcp_if_include p10p1 --mca rmaps_rank_file_path rankfile $DIR/ft.$CLASS.$NPROCS > $RESULTSDIR/ft.$CLASS.$NPROCS.results
#mpirun -hostfile mpihosts -np $NPROCS --mca btl_tcp_if_include p10p1 $DIR/ft.$CLASS.$NPROCS > $RESULTSDIR/ft.$CLASS.$NPROCS.results


## n^2 NPROCS ##################################################################

#echo bt
#date
#mpirun -hostfile mpihosts -np $NPROCS --mca btl_tcp_if_include p10p1 --mca rmaps_rank_file_path rankfile $DIR/bt.$CLASS.$NPROCS > $RESULTSDIR/bt.$CLASS.$NPROCS.results
#mpirun -hostfile mpihosts -np $NPROCS --mca btl_tcp_if_include p10p1 $DIR/bt.$CLASS.$NPROCS > $RESULTSDIR/bt.$CLASS.$NPROCS.results

#echo sp
#date
#mpirun -hostfile mpihosts -np $NPROCS --mca btl_tcp_if_include p10p1 --mca rmaps_rank_file_path rankfile $DIR/sp.$CLASS.$NPROCS > $RESULTSDIR/sp.$CLASS.$NPROCS.results
#mpirun -hostfile mpihosts -np $NPROCS --mca btl_tcp_if_include p10p1 $DIR/sp.$CLASS.$NPROCS > $RESULTSDIR/sp.$CLASS.$NPROCS.results

#echo lu
#date
#mpirun -hostfile mpihosts -np $NPROCS --mca btl_tcp_if_include p10p1 --mca rmaps_rank_file_path rankfile $DIR/lu.$CLASS.$NPROCS > $RESULTSDIR/lu.$CLASS.$NPROCS.results
#mpirun -hostfile mpihosts -np $NPROCS --mca btl_tcp_if_include p10p1 $DIR/lu.$CLASS.$NPROCS > $RESULTSDIR/lu.$CLASS.$NPROCS.results
