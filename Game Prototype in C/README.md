# A2 Ncurses Game

A terminal-based adventure game.


## GAME PLAN

**Overall Goal**

- The player must:
  1. Find and approach the NPC.
  2. Talk to the NPC to obtain a key.
  3. Use the key to unlock a door.
  4. Reach the exit tile to complete the level.

**Level 1 – Intro Level**

- Layout:
  - Simple maze with a few internal walls.
  - Locked door (`D`) blocking the path to the exit (`E`).
- Objectives:
  - Introduce movement and interaction.
  - NPC is relatively close to the starting position.
- Flow:
  - Move around using arrow keys.
  - Find the NPC (`N`), press `t` when adjacent to receive the key.
  - Walk to the door (`D`); it opens once you have the key.
  - Continue to the exit (`E`) to finish the level.

**Level 2 – Harder Maze**

- Layout:
  - More complex walls and obstacles.
  - Door and exit are farther from the starting point and NPC.
- Objectives:
  - Make navigation and planning more important.
  - Forces the player to explore more of the level.
- Flow:
  - Same mechanics as Level 1, but with a longer route and more chances to get blocked by walls.

**NPC + Key Mechanic**

- The NPC (`N`) patrols horizontally across part of the map.
- When the player stands adjacent to the NPC and presses `t`:
  - If the player does not have the key:
    - NPC gives the key (`has_key = 1`) and displays a message.
  - If the player already has the key:
    - NPC shows dialogue (“You already have the key.”).
- If the player presses `t` with no one nearby:
  - A message indicates that there is “No one nearby to talk to.”

**Door + Exit Mechanic**

- The door is represented by `D` on the map.
- If the player tries to walk into `D` without the key:
  - Movement is blocked.
  - A message appears: “The door is locked. You need a key.”
- If the player has the key and walks into `D`:
  - The door tile is replaced with floor (`.`).
  - `door_open` is set to 1 and a message indicates the door opened.
- The exit tile is represented by `E`.
  - The player can only complete the level by reaching `E` after opening the door.
  - When the player steps on `E` with `door_open == 1`, the level is marked complete.


## Controls

Arrow key = Move Player "@"
't' = Talk/Interact with NPC
'P' = Pause/Resume
'Q' = Quit Game 

## Project Structure

src/ 
main.c # Splash screen, menu, and level loop
game.c # Core gameplay logic (movement, NPC, key, door, exit)
game.h # GameState struct and function declarations
menu.c # Splash screen and main menu


