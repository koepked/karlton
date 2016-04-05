#!/usr/bin/env python

import argparse
import sys

NAS_BIN_DIR = '/shared/NAS/bin'
NET_INTF = 'p10p1'
MPIHOSTS = 'mpihosts'
ALL_CLASSES = ['S', 'W', 'A', 'B', 'C', 'D', 'E', 'F']

def check_pow_of_two(n):
    return ((n & (n-1)) == 0) and n != 0

def check_any(n):
    return True

def check_n_squared(n):
    l = [4, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225]
    if n > l[-1:][0]:
        return False
    return n in l

ALL_BENCHMARKS = {
    'is': {'nprocs_constraint': check_pow_of_two},
    'ep': {'nprocs_constraint': check_any},
    'cg': {'nprocs_constraint': check_pow_of_two},
    'mg': {'nprocs_constraint': check_pow_of_two},
    'ft': {'nprocs_constraint': check_pow_of_two},
    'bt': {'nprocs_constraint': check_n_squared},
    'sp': {'nprocs_constraint': check_n_squared},
    'lu': {'nprocs_constraint': check_n_squared}
}
NPROC_LIST = [16, 25, 32, 36, 49, 64, 81, 100, 121, 128, 144]

def arg_list(s):
    if s[0] == ',':
        s = s[1:]
    if s[-1:] == ',':
        s = s[:-1]

    return s.split(',')

def num_range(s):
    result = s.split('-')
    if len(result) != 2:
        return None
    if int(result[0]) < int(result[1]):
        return (int(result[0]), int(result[1])+1)
    else:
        return (int(result[1]), int(result[0])+1)

def nprocs_valid(nprocs, benchmark):
    return ALL_BENCHMARKS[benchmark]['nprocs_constraint'](nprocs)

def launch_benchmark(benchmark, benchmark_class, host_file, nprocs, bin_dir,
                     output_file, rank_file=None, net_intf=None):

    launch_args = ['mpirun', '-hostfile', host_file, '-np', str(nprocs)]
    if net_intf:
        launch_args += ['--mca', 'btl_tcp_if_include', net_intf]
    if rank_file:
        launch_args += ['--mca', 'rmaps_rank_file_path', rank_file]
    launch_args.append('%s/%s.%s.%s'
                       % (bin_dir, benchmark, benchmark_class, nprocs))
    print launch_args
                           

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--classes', type=arg_list)
    arg_parser.add_argument('--nprocs', type=int)
    arg_parser.add_argument('--nprocs_range', type=num_range)
    arg_parser.add_argument('--benchmarks', type=arg_list)
    args = arg_parser.parse_args(sys.argv[1:])

    nprocs = args.nprocs

    if args.classes:
        classes = args.classes
    else:
        classes = ALL_CLASSES

    if args.benchmarks:
        benchmarks = args.benchmarks
    else:
        benchmarks = ALL_BENCHMARKS.keys()

    if args.nprocs_range:
        nprocs_range = args.nprocs_range
    elif args.nprocs:
        nprocs_range = (args.nprocs, args.nprocs + 1)
    else:
        nprocs_range = (NPROC_LIST[0], NPROC_LIST[-1:][0]+1)

    for cls in classes:
        for benchmark in benchmarks:
            nprocs_list = [n for n in NPROC_LIST if (n in range(*nprocs_range)
                           and nprocs_valid(n, benchmark))]
            for nprocs in nprocs_list:
                launch_benchmark(benchmark, cls, 'test_hosts', nprocs,
                                 NAS_BIN_DIR,
                                 '%s.%s.%d.results' % (benchmark, cls, nprocs),
                                 'test_rank', NET_INTF)
