# karlton

This project aims to launch container-based virtual HPC clusters in a
simple yet configurable manner, for some definition of simple, and, for some
definition of configurable.

## Quick Start Guide

 1. Checkout the repository
```
$ git checkout https://github.com/koepked/karlton.git
```

 1. Launch a cluster with NUM_NODES compute nodes.
  ```
$ cd karlton
$ sudo bin/start_cluster.py NUM_NODES
  ```

 1. Launch one of the example mpi jobs.
  ```
$ cd /karlton/example
$ make
$ mpirun --hostfile ../mpi-hosts ./karlton
$ exit
  ```

 1. Cleanup the generated images.
  ```
$ sudo bin/cleanup_images
  ```
