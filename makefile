averager: main.o myfunctions.o
	g++ -o averager main.o myfunctions.o

main.o: main.cpp myfunctions.h
	g++ -c main.cpp

myfunctions.o: myfunctions.cpp myfunctions.h
	g++ -c myfunctions.cpp

clean:
	rm -f *.o averager