#include <stdio.h>
#include <mpi.h>

int main(int argc, char **argv) {
    int size;
    int self;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &self);

    printf("Karlton %d says what's up to the other %d nodes!\n", self, size-1);

    MPI_Finalize();
    return 0;
}
