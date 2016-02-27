#
# Generic Makefile for the sample MPI programs
#
# J. Hursey
# D. Koepke
#

# Use the MPI wrapper compiler
CC=mpicc
CFLAGS=-Wall -g -O0
LDFLAGS=-lm

#
# List all of the binary programs you want to build here
# Separate each program with a single space
#
PROGS=karlton

all: $(PROGS)

karlton: karlton.c
	$(CC) -o karlton $(CFLAGS) karlton.c

clean:
	$(RM) $(PROGS) *.o
