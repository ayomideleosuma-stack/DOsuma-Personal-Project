/**
 * @file menu.c
 * @brief Implementation of the splash screen and main menu.
 *
 * Uses ncurses to draw the title screen and menu options, and reads
 * the user's choice for which level to play or whether to exit.
 */


// menu.c
#include <ncurses.h>
#include "game.h"
#include "menu.h"

void splash_screen(void) {
    clear();
    mvprintw(5, 10, "=== Maze of the Lost Key ===");
    mvprintw(7, 10, "Ncurses game by Dele and Tenzin:");
    mvprintw(8, 12, "- Talk to the NPC to get a key");
    mvprintw(9, 12, "- Use the key to unlock the door");
    mvprintw(10, 12, "- Reach the exit to finish the level");
    mvprintw(12, 10, "Press any key to continue...");
    refresh();
    getch();
}

int main_menu(void) {
    while (1) {
        clear();
        mvprintw(5, 10, "=== Main Menu ===");
        mvprintw(7, 12, "1) Level 1 (easier)");
        mvprintw(8, 12, "2) Level 2 (harder)");
        mvprintw(9, 12, "3) Exit");
        mvprintw(11, 10, "Choose an option (1-3):");
        refresh();

        int ch = getch();
        if (ch == '1') return 1;
        if (ch == '2') return 2;
        if (ch == '3' || ch == 'q' || ch == 'Q') return 0;
    }
}

