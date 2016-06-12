# Pygame Tactic RPG Prototype

A "game" similar to tactic games like Fire Emblem and Advance Wars, made priarily as learning experience.
Currently this is not "really" a game, just a very barebone base structure. You can move around (pathfinding for the player) and attack enemies, 
including attack animations but that is more or less it. 



Requires python 2.7 and pygame 1.9.2a0 win32 bit: http://www.pygame.org/download.shtml

Uses pytmx version 3.20 to allow loading of .tmx map files. pytmx is licensed under LGPL v3:  https://github.com/bitcraft/PyTMX

To update the pytmx library, download the newest build from https://github.com/bitcraft/PyTMX and replace the pytmx folder
with the pytmx folder from bitcraft's repository.
 
Updating pytmx possibly requires you to modifiy the tilerenderer.py file.

pytmx additionally uses the "six"-module by "gutworth". "six" is licensed under MIT: https://bitbucket.org/gutworth/six


Controls:

Start the game by launching main.py.

Left Click on the hero character, then select a tile to move to. If you are next to an enemy, you can attack that enemy. 
Press Space to end your turn after you moved.