CC = g++
CFLAGS = -lm -pthread -Ofast -march=native -Wall -funroll-loops -Wno-unused-result 

all: ransampl.o line

ransampl.o : ransampl.c
	$(CC) $(CFLAGS) $(OPT_DEF) -c ransampl.c

line : line.cpp
	$(CC) $(CFLAGS) $(OPT_DEF) -I/usr/local/opt/gsl/include -L/usr/local/opt/gsl/lib line.cpp ransampl.o -o line -lgsl -lm -lgslcblas

clean:
	rm -rf *.o line
