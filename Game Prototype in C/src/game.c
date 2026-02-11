/**
 * @file game.c
 * @brief Implementation of the core game logic.
 *
 * Contains the functions that initialize levels, update NPCs,
 * move the player, handle interactions (key, door, exit), and
 * draw the game state using ncurses.
 */

// game.c
#include "game.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* NCURSES SETUP */

void init_ncurses(void) {
    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);
    curs_set(0);   // hide cursor
}

void shutdown_ncurses(void) {
    endwin();
}

/* LEVEL SETUP */

static void clear_map(char map[MAP_ROWS][MAP_COLS]) {
    for (int y = 0; y < MAP_ROWS; y++) {
        for (int x = 0; x < MAP_COLS; x++) {
            map[y][x] = ' ';
        }
    }
}

static void add_borders(char map[MAP_ROWS][MAP_COLS]) {
    for (int y = 0; y < MAP_ROWS; y++) {
        for (int x = 0; x < MAP_COLS; x++) {
            if (y == 0 || y == MAP_ROWS - 1 || x == 0 || x == MAP_COLS - 1) {
                map[y][x] = '#';
            }
        }
    }
}


/* Copies a text-based maze layout into the map array.*/
static void load_maze(char map[MAP_ROWS][MAP_COLS],
                             const char *layout[],
                             int num_rows)
{
    int y, x;

    for (y = 0; y < num_rows && y < MAP_ROWS; y++) {
        const char *row = layout[y];

        for (x = 0; x < MAP_COLS; x++) {
            /* If the row is shorter than MAP_COLS, fill with spaces. */
            if (row[x] == '\0')
                map[y][x] = ' ';
            else
                map[y][x] = row[x];
        }
    }

    /* If the maze is fewer rows than MAP_ROWS, fill the rest with spaces as well */
    for (; y < MAP_ROWS; y++) {
        for (x = 0; x < MAP_COLS; x++) {
            map[y][x] = ' ';
        }
    }
}


static void add_simple_maze_level1(char map[MAP_ROWS][MAP_COLS])
{
const char *layout[] = {
        "################################################################################",
        "#              #         #       #                   #                         #",
        "#        #     #   #     #       #       #           #     ###############     #",
        "#        #         #             #       #           #     #             #     #",
        "#    #####################       #       #   #########     #         E   #     #",
        "#           #            #       #       #           #     #             #     #",
        "#           #            #       #       #           #     #   ###########     #",
        "#######     #            #       #       #                 #             #     #",
        "#           #######      #               #           #     #             #     #",
        "#           #            ###########################################    ##     #",
        "#           #            #                           #     #             #     #",
        "#    ########            #                           #           #       #     #",
        "#                        #                           #           #       #     #",
        "#                        #                           #     #     #       #     #",
        "######D###################         ################  #     #     #########     #",
        "#           #            #         #                 #     #     #             #",
        "#           #            #         #                 #     #     #             #",
        "#           #            #         #                 #     #######      ########",
        "#           #            #         #                 #       #          #      #",
        "#           #            #         #                 #       #          #      #",
        "#           #            #         #                 #       #   ########      #",
        "#           ####      ####         ###################       #          #      #",
        "#                        #               #           #       #          #      #",
        "#                        #               #           #       #          #      #",
        "#                        #               #           #       #          #      #",
        "#                                        #           #       #                 #",
        "#                        #               #           #                         #",
        "#                        #                           #                         #",
        "################################################################################"
};

    load_maze(map, layout, sizeof(layout)/sizeof(layout[0]));
}


static void add_simple_maze_level2(char map[MAP_ROWS][MAP_COLS])
{
const char *layout[] = {
        "################################################################################",
        "#              #         #       #                   #     #                   #",
        "#        #     #   #     #   #           #           #     ###############     #",
        "#        #         #         #           #           #     #             #     #",
        "#    #########################   #       #   #########     #             #     #",
        "#           #            #       #### ####           ####  #      E      D     #",
        "#                        #       #       #   #   #   #     #             #     #",
        "#######     #            ###   ###           #   #         #             #     #",
        "#           #######      #               #   #   #   #     ###############  ####",
        "#    ########            ############  #######   ######  ###         #   #     #",
        "#           #     #      #    #    #    #            #     #         #         #",
        "####   ######     ########    #    #    #   ##########     #     #   #         #",
        "#      #       #              #    #                 #           #   #   ####  #",
        "#      #       #         #    #    #    #      #     #     #     #       #     #",
        "#   ######################         ################  #     #     #####   #     #",
        "#   #       #            #######   #              #  #     #     #      ###  ###",
        "#   #  #    ##########   #         #              #  ###   #     #      #      #",
        "#   #  #    #            #         #                 #     ##########   ####  ##",
        "#      #    #    #########   #######    ###########  #    #  #     #           #",
        "########    #      #     #         #    #       #    #       #     #           #",
        "#           #      #     #         #       #    #    #   #   #   ########      #",
        "#  #############   #  ####     #   #########   #######   #####          #  #####",
        "#       #      #   #     #     #         #      #    #       #     #    #      #",
        "####   #   #   #   #  #  #     #         #      #    ####    #######    #      #",
        "#     #    #   #   #  #  #######    ######           #       #     #    #####  #",
        "#    #     #   #      #        #    #    #   ###     #   #####     #    #      #",
        "#      #####   ########  #     #    #    #     #     #    #     #       #      #",
        "#          #             #          #          #     #          #              #",
        "################################################################################"
};

    load_maze(map, layout, sizeof(layout)/sizeof(layout[0]));
}

void init_level(int level, char map[MAP_ROWS][MAP_COLS], GameState *state) {
    clear_map(map);
    add_borders(map);

    memset(state, 0, sizeof(*state));
    state->running    = 1;
    state->paused     = 0;
    state->has_key    = 0;
    state->door_open  = 0;
    state->level_done = 0;
    state->level      = level;
    state->info[0]    = '\0';

    // Player start
    state->player_y = MAP_ROWS / 2;
    state->player_x = MAP_COLS / 4;

    // NPC start
    state->npc_y   = MAP_ROWS / 2;
    state->npc_x   = MAP_COLS / 2;
    state->npc_dir = -1;

    if (level == 1) {
        add_simple_maze_level1(map);
    } else {
        add_simple_maze_level2(map);
    }
}

/* DRAWING */

void draw_game(const char map[MAP_ROWS][MAP_COLS], const GameState *state) {
    clear();

    // Draw map
    for (int y = 0; y < MAP_ROWS; y++) {
        for (int x = 0; x < MAP_COLS; x++) {
            mvaddch(y, x, map[y][x]);
        }
    }

    // Draw NPC
    mvaddch(state->npc_y, state->npc_x, 'N');

    // Draw player
    mvaddch(state->player_y, state->player_x, '@');

    // HUD
    mvprintw(MAP_ROWS, 0,
             "Level %d | Arrows: move | t: talk | p: pause | q: quit",
             state->level);
    mvprintw(MAP_ROWS + 1, 0,
             "Key: %s | Door: %s",
             state->has_key ? "YES" : "NO",
             state->door_open ? "OPEN" : "CLOSED");

    if (state->paused) {
        mvprintw(MAP_ROWS + 2, 0,
                 "GAME PAUSED - press 'p' to resume");
    }

    if (state->info[0] != '\0') {
        mvprintw(MAP_ROWS + 3, 0, "%s", state->info);
    }

    refresh();
}

/* QUIT CONFIRM */

int handle_quit_prompt(void) {
    mvprintw(MAP_ROWS + 3, 0, "Quit game? (y/n): ");
    clrtoeol();
    refresh();
    int ch = getch();
    return (ch == 'y' || ch == 'Y');
}

/*  NPC & INTERACTION */

void update_npc(GameState *state, char map[MAP_ROWS][MAP_COLS]) {
    int next_x = state->npc_x + state->npc_dir;

    // Stay within inner area and avoid walls
    if (next_x <= 1 || next_x >= MAP_COLS - 2 ||
        map[state->npc_y][next_x] == '#') {
        state->npc_dir = -state->npc_dir;
        next_x = state->npc_x + state->npc_dir;
        if (next_x <= 1 || next_x >= MAP_COLS - 2 ||
            map[state->npc_y][next_x] == '#') {
            return; // stuck
        }
    }

    state->npc_x = next_x;
}

int is_adjacent_to_npc(const GameState *state) {
    int dy = state->player_y - state->npc_y;
    int dx = state->player_x - state->npc_x;
    if (dy < 0) dy = -dy;
    if (dx < 0) dx = -dx;
    return (dy + dx == 1); // distance 1
}

/* MOVEMENT & DOOR/EXIT LOGIC */

void attempt_move_player(int dy, int dx, GameState *state,
                         char map[MAP_ROWS][MAP_COLS]) {
    int new_y = state->player_y + dy;
    int new_x = state->player_x + dx;

    if (new_y < 0 || new_y >= MAP_ROWS || new_x < 0 || new_x >= MAP_COLS) {
        return;
    }

    char cell = map[new_y][new_x];

    // Walls
    if (cell == '#') {
        snprintf(state->info, sizeof(state->info),
                 "You bump into a wall.");
        return;
    }

    // Door
    if (cell == 'D') {
        if (!state->has_key) {
            snprintf(state->info, sizeof(state->info),
                     "The door is locked. You need a key.");
            return;
        } else {
            // Open door
            map[new_y][new_x] = '.';
            state->door_open = 1;
            snprintf(state->info, sizeof(state->info),
                     "You unlock and open the door.");
            state->player_y = new_y;
            state->player_x = new_x;
            return;
        }
    }

    // Exit
    if (cell == 'E') {
        if (!state->door_open) {
            snprintf(state->info, sizeof(state->info),
                     "You must open the door first!");
            return;
        } else {
            state->player_y = new_y;
            state->player_x = new_x;
            state->level_done = 1;
            snprintf(state->info, sizeof(state->info),
                     "You found the exit!");
            return;
        }
    }

    // Normal floor/space
    state->player_y = new_y;
    state->player_x = new_x;
    state->info[0] = '\0';
}

/*  PLAY ONE LEVEL */

void play_level(int level) {
    char map[MAP_ROWS][MAP_COLS];
    GameState state;

    init_level(level, map, &state);

    while (state.running && !state.level_done) {
        draw_game(map, &state);

        int ch = getch();

        if (state.paused) {
            if (ch == 'p' || ch == 'P') {
                state.paused = 0;
                snprintf(state.info, sizeof(state.info),
                         "Game resumed.");
            }
            continue;
        }

        // state.info[0] = '\0';

        if (ch == 'q' || ch == 'Q') {
            if (handle_quit_prompt()) {
                state.running = 0;
            }
        } else if (ch == 'p' || ch == 'P') {
            state.paused = 1;
            snprintf(state.info, sizeof(state.info),
                     "Game paused.");
        } else if (ch == KEY_UP) {
            attempt_move_player(-1, 0, &state, map);
        } else if (ch == KEY_DOWN) {
            attempt_move_player(1, 0, &state, map);
        } else if (ch == KEY_LEFT) {
            attempt_move_player(0, -1, &state, map);
        } else if (ch == KEY_RIGHT) {
            attempt_move_player(0, 1, &state, map);
        } else if (ch == 't' || ch == 'T') {
		if (is_adjacent_to_npc(&state)) {
			if (!state.has_key) {
				state.has_key = 1;
				snprintf(state.info, sizeof(state.info),
						"NPC: Here, take this key!");
			} else {
				snprintf(state.info, sizeof(state.info),
						"NPC: You already have the key.");
			}
		} else {
			snprintf(state.info, sizeof(state.info),
					"No one nearby to talk to.");
    }
}


        if (state.running && !state.paused) {
            update_npc(&state, map);
        }
    }

    if (state.level_done && state.running) {
        draw_game(map, &state);
        mvprintw(MAP_ROWS + 4, 0,
                 "Level %d complete! Press any key to continue...", level);
        refresh();
        getch();
    }
}

