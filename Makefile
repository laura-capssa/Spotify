CC=mpicc
CFLAGS=-O2 -Wall
TARGET=spotify_mpi
SRC=src/main.c src/map_utils.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $(TARGET) $(SRC)

clean:
	rm -f $(TARGET) *.o partial_*.txt