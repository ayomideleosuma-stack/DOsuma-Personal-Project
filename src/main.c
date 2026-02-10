/**
 * @file main.c
 * @brief Entry point for the A2 Ncurses Game.
 *
 * Sets up ncurses, shows the splash screen and main menu, and
 * starts the selected level. Cleans up ncurses on exit.
 */

/**
 * @mainpage 
 * The player moves `@` around a 2D map,
 * interacts with an NPC to obtain a key, unlocks a door, and reaches
 * the exit tile to complete the level.
 * See the @ref GameState struct and the functions in game.h and menu.h
 * for more implementation details.
 */


// main.c
#include <stdio.h>
#include "game.h"
#include "menu.h"
/**
 * @brief Program entry point.
 *
 * Initializes ncurses, checks terminal size, shows the splash screen
 * and main menu, then runs the requested level until the user exits.
 *
 * @return 0 on normal exit, non-zero on error (e.g., terminal too small).
 */

int main(void) {
    init_ncurses();

    // size check (LINES/COLS from ncurses)
    if (LINES < MAP_ROWS + 6 || COLS < MAP_COLS) {
        shutdown_ncurses();
        fprintf(stderr, "Terminal too small. Need at least %dx%d.\n",
                MAP_ROWS + 6, MAP_COLS);
        return 1;
    }

    splash_screen();

    while (1) {
        int choice = main_menu();
        if (choice == 0) break;
        play_level(choice);
    }

    shutdown_ncurses();
    return 0;
}

