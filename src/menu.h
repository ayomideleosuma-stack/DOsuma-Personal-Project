/**
 * @file menu.h
 * @brief Splash screen and main menu interface.
 *
 * Declares functions used to show the game title screen and the
 * main menu that lets the player choose a level or exit.
 */


// menu.h
#ifndef MENU_H
#define MENU_H

/**
 * @brief Show the splash screen with the game title and basic instructions.
 *
 * Waits for a key press before returning.
 */
void splash_screen(void);

/**
 * @brief Display the main menu and return the user's choice.
 *
 * @return 0 to exit the game, 1 for level 1, 2 for level 2.
 */
int  main_menu(void);

#endif

