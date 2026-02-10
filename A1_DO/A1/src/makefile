CC = gcc
CFLAGS = -Wall -g
LDLIBS =

# add -lcunit 
TEST_LIBS = -lcunit

OBJS_HT = ht.o
OBJS_PCODE = pcode.o
OBJS_TEST = Testing/test_ht.o

all: pcode test_ht

pcode: $(OBJS_HT) $(OBJS_PCODE)
	$(CC) $(CFLAGS) -o pcode $(OBJS_HT) $(OBJS_PCODE) $(LDLIBS)

test_ht: $(OBJS_HT) $(OBJS_TEST)
	$(CC) $(CFLAGS) -o test_ht $(OBJS_HT) $(OBJS_TEST) $(TEST_LIBS)

ht.o: ht.c ht.h ht_impl.h
	$(CC) $(CFLAGS) -c ht.c

pcode.o: pcode.c ht.h
	$(CC) $(CFLAGS) -c pcode.c

Testing/test_ht.o: Testing/test_ht.c ht.h
	$(CC) $(CFLAGS) -c Testing/test_ht.c -o Testing/test_ht.o

clean:
	rm -f *.o pcode test_ht Testing/*.o

