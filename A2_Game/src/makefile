CC      = gcc
CFLAGS  = -Wall -Wextra -std=c11
LDFLAGS = -lncurses

SRC     = main.c game.c menu.c
OBJ     = $(SRC:.c=.o)

BIN_DIR = ../bin
APP     = $(BIN_DIR)/appGame

DOXYFILE = Doxyfile 

.PHONY: all appGame clean mem_valgrind debug doc

# Default target: build the appGame executable
all: appGame

# appGame target
appGame: CFLAGS += -O2
appGame: $(OBJ)
	mkdir -p $(BIN_DIR)
	$(CC) $(CFLAGS) -o $(APP) $(OBJ) $(LDFLAGS)

# 4. debug target
debug: CFLAGS += -g -DDEBUG
debug: clean appGame

# 2. clean target
clean:
	rm -f $(OBJ) $(APP)

# mem_valgrind
mem_valgrind: appGame
	valgrind --leak-check=full --track-origins=yes $(APP)

doc:
	mkdir -p ../doc
	doxygen $(DOXYFILE)


