# gemini-pro-rpg

Interested in playing a dynamic role-playing game (RPG)? **Gemini Pro RPG** allows such feature with Gemini Pro integrated
into the game! Experience dynamic game structure and storyline like never before!

# Source Code

The source code of the game **Gemini Pro RPG** is available in 
[Source Code](https://github.com/GlobalCreativeApkDev/gemini-pro-rpg/blob/master/main.py).

# Installation

```
pip install gemini-pro-rpg
```

# How to Play the Game?

Pre-requisites:
1. [Python](https://www.python.org/downloads/) installed in your device.
2. .env file in the same directory as <GEMINI_PRO_RPG_DIRECTORY> and has the value of GEMINI_API_KEY.
3. The directory "saved" exists inside the directory <GEMINI_PRO_RPG_DIRECTORY>. Please create the "saved" directory
if it has not existed in <GEMINI_PRO_RPG_DIRECTORY> directory yet.

First, open a Terminal or Command Prompt window and run the following commands.

```
cd <GEMINI_PRO_RPG_DIRECTORY>
python3 main.py
```

**Note:** Replace <GEMINI_PRO_RPG_DIRECTORY> with the path to the directory of the game **Gemini Pro RPG**.

Then, the game will start with something looking like in the screenshot below.

![Application](images/Application.png)

You have two choices.

1. Enter "NEW GAME" to play a new game.
2. Enter "PLAY EXISTING GAME" to play an existing game.

# New Game Creation

The following happens when you choose to create a new game.

![New Game Input](images/New%20Game%20Input.png)

You will then be asked to input the following values.

1. Temperature - between 0 and 1 inclusive
2. Top P - between 0 and 1 inclusive
3. Top K - at least 1
4. Max output tokens - at least 1
5. Name of the new game
6. Your name to be used as player name

You will then be directed to the main menu.

# Playing Existing Game

You will only be able to play existing game if at least one or more saved game files are stored inside the "saved" directory.

The following happens when you choose to play an existing game.

![Play Existing Game](images/Play%20Existing%20Game.png)

You will then be asked to enter the name of the game you want to play (from the ones listed like 
in the screenshot above). After that, your saved game data will be loaded and you will be
directed to the main menu.

# Main Menu

Once you reach the main menu, you will be asked whether you want to continue playing the game or not. If you enter 'Y', 
you will be directed to a battle. Else, your game data will be saved and you will exit the game.

![Main Menu](images/Main%20Menu.png)

# Battle

During a battle, you will have two choices during your turn to make a move:

1. Enter 'ATTACK' to attack the enemy.
2. Enter 'FLEE' to exit the battle and return to the main menu.

![Battle](images/Battle.png)

If you either defeated the enemy or the enemy fled, you will level up between 1 and 100 times inclusive. If the enemy
defeated you or you fled, you will not level up at all but your HP will be restored.

**Note:** Levelling up automatically restores your HP.

# Progress

1. Supports dynamic simple turn-based RPG on command-line interface (done)
2. Supports dynamic complex turn-based RPG with items, levels, shops, resources, etc on command-line interface (pending)
3. Supports dynamic player exploration RPG on command-line interface (pending)
4. Supports custom RPG on command-line interface (pending)
5. Supports dynamic graphical user interface RPG (pending)
6. Supports Python for Unity (pending)

# Version History

1. Version 0.5 (Release Date: 28 December 2023):
* Allows the player to play a dynamic simple turn-based RPG on command-line interface

2. Version 1 (Release Date: TBA, 2024):
* Allows the player to play a dynamic complex turn-based strategy RPG with items, levels, shops, resources, etc on command-line interface
* Allows the player to play a dynamic player exploration RPG on command-line interface
* Allows the player to play a customised and dynamic RPG based on the specifications he/she wants on command-line interface.

3. Version 1.5 (Release Date: TBA, 2024):
* Allows the player to play a dynamic graphical user interface RPG

4. Version 2 (Release Date: TBA, 2024):
* Supports Python for Unity
