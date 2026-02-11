/**
 * @file game.h
 * @brief Core game state and gameplay function declarations.
 *
 * This header defines the GameState structure and the public functions
 * used to initialize ncurses, set up levels, draw the game, and run
 * the main gameplay loop.
 */

// game.h
#ifndef GAME_H
#define GAME_H

#include <ncurses.h>

#define MAP_ROWS 30
#define MAP_COLS 80

/** 
 * @struct GameState
 * @brief Holds all the state for a single game session.
 * This struct keeps track of the player, NPC, key/door/exit status, and various flags used by the game loop and HUD.
 */
typedef struct {
    int player_y, player_x; /** < Player current row and column position on the map . */
    int npc_y, npc_x; /** < NPC current row and column position on the map */
    int npc_dir;        // horizontal patrol: +1 or -1 /**< NPC patrol direction: +1 for right, -1 for left. */

    int has_key;        // 0 = no, 1 = yes  /**< 1 if the player has obtained the key from the NPC. */
    int door_open;      // 0 = closed, 1 = open  /**< 1 if the locked door has been opened. */
    int level_done;     // 1 when exit reached /**< 1 when the player has reached the exit tile. */

    int paused; /**< 1 when the game is paused. */
    int running; /**< 1 while the level loop should keep running. */

    int level;          // 1 or 2  /**< Current level number*/

    char info[128];     // message line /**< Status / dialogue message shown in the HUD. */
} GameState;

/* ncurses setup */
/**
 * @brief Initialize ncurses and configure the terminal.
 *
 * Sets up cbreak mode, disables echo, enables keypad input,
 * and hides the cursor. Must be called before any ncurses calls.
 */

void init_ncurses(void);

/**
 * @brief Restore the terminal and shut down ncurses.
 */

void shutdown_ncurses(void);
/**
 * @brief Initialize the map and GameState for a given level.
 *
 * @param level Level number to load (1 or 2).
 * @param map   2D character buffer that will hold the level layout.
 * @param state Pointer to a GameState struct to initialize.
 */

/* level + game */
void init_level(int level, char map[MAP_ROWS][MAP_COLS], GameState *state);
/**
 * @brief Draw the current map, player, NPC, and HUD to the screen.
 *
 * @param map   The current map contents.
 * @param state The current game state to visualize. */
void draw_game(const char map[MAP_ROWS][MAP_COLS], const GameState *state);
/**
 * @brief Ask the user to confirm quitting the game.
 *
 * @return 1 if the user chooses 'y' or 'Y', 0 otherwise.
 */

int  handle_quit_prompt(void);
/**
 * @brief Update the NPC's patrol position on the map.
 *
 * The NPC moves horizontally between walls or map boundaries.
 *
 * @param state The current game state (NPC position/direction updated).
 * @param map   The map used to check for walls and bounds.
 */
void update_npc(GameState *state, char map[MAP_ROWS][MAP_COLS]);
/**
 * @brief Check if the player is standing next to the NPC.
 *
 * @param state The current game state.
 * @return 1 if the player is adjacent, 0 otherwise.
 */
int  is_adjacent_to_npc(const GameState *state);
/**
 * @brief Attempt to move the player by the given offset.
 *
 * Handles collision with walls, locked doors, opening the door
 * when the key is held, and detecting the exit.
 *
 * @param dy   Change in row (Y).
 * @param dx   Change in column (X).
 * @param state The current game state (updated if movement occurs).
 * @param map   The current map (door tile may be modified).
 */

void attempt_move_player(int dy, int dx, GameState *state,
                         char map[MAP_ROWS][MAP_COLS]);

/**
 * @brief Run the main gameplay loop for the given level.
 *
 * Handles input, updates the NPC, moves the player, and redraws the
 * screen until the level is completed or the player chooses to quit.
 *
 * @param level Level number to play (1 or 2).
 */
void play_level(int level);

#endif

