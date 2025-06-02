SRC = .
CFLAGS = -Ofast -march=native
LDFLAGS = 
CC = gcc

OBJ1 = o/tsir.o o/misc.o o/heap.o o/pcg_rnd.o

all : tsir

tsir: $(OBJ1)
	$(CC) $(LDFLAGS) -o $@ $^ -lm

o/tsir.o : $(SRC)/tsir.c $(SRC)/tsir.h $(SRC)/Makefile
	$(CC) $(CFLAGS) -c $(SRC)/tsir.c -o $@

o/misc.o : $(SRC)/misc.c $(SRC)/tsir.h $(SRC)/Makefile
	$(CC) $(CFLAGS) -c $(SRC)/misc.c -o $@

o/heap.o : $(SRC)/heap.c $(SRC)/tsir.h $(SRC)/Makefile
	$(CC) $(CFLAGS) -c $(SRC)/heap.c -o $@

o/pcg_rnd.o : $(SRC)/pcg_rnd.c $(SRC)/tsir.h $(SRC)/Makefile
	$(CC) $(CFLAGS) -c $(SRC)/pcg_rnd.c -o $@
