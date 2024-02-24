"""
This file contains code for the game "Gemini Pro RPG".
Author: GlobalCreativeApkDev
"""

# Importing necessary libraries


import sys
import uuid
import pickle
import copy
import google.generativeai as gemini
import os
from dotenv import load_dotenv
from mpmath import mp, mpf

mp.pretty = True


# Creating static functions to be used in this game.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def load_game_data(file_name):
    # type: (str) -> SavedGameData
    return pickle.load(open(file_name, "rb"))


def save_game_data(game_data, file_name):
    # type: (SavedGameData, str) -> None
    pickle.dump(game_data, open(file_name, "wb"))


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating necessary classes


class Player:
    """
    This class contains attributes of the player in this game.
    """

    def __init__(self, name, max_hp, attack_power, defense):
        # type: (str, mpf, mpf, mpf) -> None
        self.player_id: str = str(uuid.uuid1())
        self.name: str = name
        self.level: int = 1
        self.max_hp: mpf = max_hp
        self.curr_hp: mpf = self.max_hp
        self.attack_power: mpf = attack_power
        self.defense: mpf = defense

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += "Player ID: " + str(self.player_id) + "\n"
        res += "Name: " + str(self.name) + "\n"
        res += "Level: " + str(self.level) + "\n"
        res += "HP: " + str(self.curr_hp) + "/" + str(self.max_hp) + "\n"
        res += "Attack Power: " + str(self.attack_power) + "\n"
        res += "Defense: " + str(self.defense) + "\n"
        return res

    def restore(self):
        # type: () -> None
        self.curr_hp = self.max_hp

    def get_is_alive(self):
        # type: () -> bool
        return self.curr_hp > 0

    def level_up(self):
        # type: () -> None
        self.max_hp *= self.level * 2
        self.restore()
        self.attack_power *= self.level * 2
        self.defense *= self.level * 2
        self.level += 1

    def attack(self, other, is_crit):
        # type: (Enemy, bool) -> None
        raw_damage: mpf = self.attack_power * 2 - other.defense if is_crit else self.attack_power - other.defense
        damage: mpf = raw_damage if raw_damage > 0 else mpf("0")
        other.curr_hp -= damage
        print(str(self.name) + " dealt " + str(damage) + " damage on " + str(other.name) + "!")

    def clone(self):
        # type: () -> Player
        return copy.deepcopy(self)


class Enemy(Player):
    """
    This class contains attributes of an enemy in this game.
    """

    def __init__(self, name, max_hp, attack_power, defense):
        # type: (str, mpf, mpf, mpf) -> None
        Player.__init__(self, name, max_hp, attack_power, defense)


class SavedGameData:
    """
    This class contains attributes of a saved game data.
    """

    def __init__(self, game_name, temperature, top_p, top_k, max_output_tokens, player_data):
        # type: (str, float, float, float, int, Player) -> None
        self.game_name: str = game_name
        self.temperature: float = temperature
        self.top_p: float = top_p
        self.top_k: float = top_k
        self.max_output_tokens: int = max_output_tokens
        self.player_data: Player = player_data

    def __str__(self):
        # type: () -> str
        res: str = ""  # initial value
        res += str(self.game_name).upper() + "\n"
        res += "Temperature: " + str(self.temperature) + "\n"
        res += "Top P: " + str(self.top_p) + "\n"
        res += "Top K: " + str(self.top_k) + "\n"
        res += "Max output tokens: " + str(self.max_output_tokens) + "\n"
        return res

    def clone(self):
        # type: () -> SavedGameData
        return copy.deepcopy(self)


# Creating main function used to run the application.


def main() -> int:
    """
    This main function is used to run the application.
    :return: an integer
    """

    load_dotenv()
    gemini.configure(api_key=os.environ['GEMINI_API_KEY'])

    # Gemini safety settings
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    # Saved game data
    saved_game_data: SavedGameData

    # Game name
    game_name: str = ""  # initial value

    # Gemini Generative Model
    model = gemini.GenerativeModel(model_name="gemini-pro",
                                       generation_config={"temperature": 0.9,
                                                          "top_p": 1,
                                                          "top_k": 1,
                                                          "max_output_tokens": 2048,},
                                       safety_settings=safety_settings)  # initial value

    print("Enter 'NEW GAME' to play new game.")
    print("Enter 'PLAY EXISTING GAME' to play existing game.")
    action: str = input("What do you want to do? ")
    while action not in ["NEW GAME", "PLAY EXISTING GAME"]:
        clear()
        print("Enter 'NEW GAME' to play new game.")
        print("Enter 'PLAY EXISTING GAME' to play existing game.")
        action = input("Sorry, invalid input! What do you want to do? ")

    if action == "NEW GAME":
        clear()

        # Asking user input values for generation config
        temperature: str = input("Please enter temperature (0 - 1): ")
        while not is_number(temperature) or float(temperature) < 0 or float(temperature) > 1:
            temperature = input("Sorry, invalid input! Please re-enter temperature (0 - 1): ")

        float_temperature: float = float(temperature)

        top_p: str = input("Please enter Top P (0 - 1): ")
        while not is_number(top_p) or float(top_p) < 0 or float(top_p) > 1:
            top_p = input("Sorry, invalid input! Please re-enter Top P (0 - 1): ")

        float_top_p: float = float(top_p)

        top_k: str = input("Please enter Top K (at least 1): ")
        while not is_number(top_k) or int(top_k) < 1:
            top_k = input("Sorry, invalid input! Please re-enter Top K (at least 1): ")

        float_top_k: int = int(top_k)

        max_output_tokens: str = input("Please enter maximum input tokens (at least 1): ")
        while not is_number(max_output_tokens) or int(max_output_tokens) < 1:
            max_output_tokens = input("Sorry, invalid input! Please re-enter maximum input tokens (at least 1): ")

        int_max_output_tokens: int = int(max_output_tokens)

        # Set up the model
        generation_config = {
            "temperature": float_temperature,
            "top_p": float_top_p,
            "top_k": float_top_k,
            "max_output_tokens": int_max_output_tokens,
        }

        model = gemini.GenerativeModel(model_name="gemini-pro",
                                       generation_config=generation_config,
                                       safety_settings=safety_settings)

        game_name = input("Enter the name of the game you are playing: ")
        saved_game_files: list = [f for f in os.listdir("saved")]
        while game_name in saved_game_files:
            print("Below is a list of existing games:\n")
            for i in range(len(saved_game_files)):
                print(str(i + 1) + ". " + str(saved_game_files[i]))

            game_name = input("Sorry, the game " + str(game_name) + " already exists! "
                "Enter another name of the game you are playing: ")

        player_name: str = input("Please enter your name: ")
        convo = model.start_chat(history=[
        ])
        convo.send_message("Please enter any float between 100 and 150 inclusive!")
        player_max_hp: str = str(convo.last.text.split("\n")[0])
        convo.send_message("Please enter any float between 20 and 50 inclusive!")
        player_attack_power: str = str(convo.last.text.split("\n")[0])
        convo.send_message("Please enter any float between 10 and 20 inclusive!")
        player_defense: str = str(convo.last.text.split("\n")[0])
        saved_game_data = SavedGameData(game_name, float_temperature, float_top_p, float_top_k,
                                        int_max_output_tokens, Player(player_name, mpf(player_max_hp),
                                                                      mpf(player_attack_power), mpf(player_defense)))
    else:
        clear()

        saved_game_files: list = [f for f in os.listdir("saved")]
        if len(saved_game_files) == 0:
            return 1  # cannot play any game!

        print("Below is a list of existing games:\n")
        for i in range(len(saved_game_files)):
            print(str(i + 1) + ". " + str(saved_game_files[i]))

        game_name = input("What game do you want to play? ")
        while game_name not in saved_game_files:
            clear()
            print("Below is a list of existing games:\n")
            for i in range(len(saved_game_files)):
                print(str(i + 1) + ". " + str(saved_game_files[i]))

            game_name = input("Sorry, invalid input! What game do you want to play? ")

        saved_game_data = load_game_data(os.path.join("saved", game_name))

        # Set up the model
        generation_config = {
            "temperature": saved_game_data.temperature,
            "top_p": saved_game_data.top_p,
            "top_k": saved_game_data.top_k,
            "max_output_tokens": saved_game_data.max_output_tokens,
        }

        model = gemini.GenerativeModel(model_name="gemini-pro",
                                       generation_config=generation_config,
                                       safety_settings=safety_settings)

    # Start playing the game
    while True:
        clear()
        print("Enter 'Y' for yes.")
        print("Enter anything else for no.")
        continue_playing: str = input("Do you want to continue playing? ")
        if continue_playing != "Y":
            save_game_data(saved_game_data, os.path.join("saved", game_name))
            return 0  # successfully saved the game

        clear()
        # Define the enemy
        convo = model.start_chat(history=[
        ])
        convo.send_message("Please enter any float between " +
                           str(mpf("0.85") * saved_game_data.player_data.max_hp) + " and " +
                           str(mpf("1.15") * saved_game_data.player_data.max_hp) + " (one word response only)!")
        enemy_max_hp: str = str(convo.last.text)
        convo.send_message("Please enter any float between " +
                           str(mpf("0.85") * saved_game_data.player_data.attack_power) + " and " +
                           str(mpf("1.15") * saved_game_data.player_data.attack_power) + " (one word response only)!")
        enemy_attack_power: str = str(convo.last.text)
        convo.send_message("Please enter any float between " +
                           str(mpf("0.85") * saved_game_data.player_data.defense) + " and " +
                           str(mpf("1.15") * saved_game_data.player_data.defense) + " (one word response only)!")
        enemy_defense: str = str(convo.last.text)
        convo.send_message("Generate a random monster name!")
        enemy_name: str = str(convo.last.text)
        enemy: Enemy = Enemy(enemy_name, mpf(enemy_max_hp), mpf(enemy_attack_power), mpf(enemy_defense))

        turn: int = 0
        player_flee: bool = False
        enemy_flee: bool = False
        while saved_game_data.player_data.get_is_alive() and enemy.get_is_alive() \
            and not player_flee and not enemy_flee:
            print(str(saved_game_data.player_data.name) + "'s stats:\n\n" + str(saved_game_data.player_data))
            print(str(enemy.name) + "'s stats:\n\n" + str(enemy))

            turn += 1
            if turn % 2 == 1:
                print("It is " + str(saved_game_data.player_data.name) + "'s turn to move!")
                print("Enter 'ATTACK' to attack.")
                print("Enter 'FLEE' to flee.")
                battle_action: str = input("What do you want to do? ")
                while battle_action not in ["ATTACK", "FLEE"]:
                    clear()
                    print("Enter 'ATTACK' to attack.")
                    print("Enter 'FLEE' to flee.")
                    battle_action = input("Sorry, invalid input! What do you want to do? ")

                if battle_action == "ATTACK":
                    convo.send_message("Enter \"CRITICAL\" or \"NORMAL\"!")
                    is_crit: bool = str(convo.last.text) == "CRITICAL"
                    saved_game_data.player_data.attack(enemy, is_crit)
                else:
                    player_flee = True
            else:
                print("It is " + str(enemy.name) + "'s turn to move!")
                convo.send_message("Enter \"ATTACK\" or \"FLEE\"!")
                flee: bool = str(convo.last.text) == "FLEE"
                if flee:
                    enemy_flee = True
                else:
                    convo.send_message("Enter \"CRITICAL\" or \"NORMAL\"!")
                    is_crit: bool = str(convo.last.text) == "CRITICAL"
                    enemy.attack(saved_game_data.player_data, is_crit)

        if not saved_game_data.player_data.get_is_alive():
            print(str(saved_game_data.player_data.name) + " was defeated!")
            saved_game_data.player_data.restore()
        elif player_flee:
            print(str(saved_game_data.player_data.name) + " fled!")
            saved_game_data.player_data.restore()
        elif enemy_flee or not enemy.get_is_alive():
            print(str(saved_game_data.player_data.name) + " won the battle!")
            convo.send_message("Please enter an integer between 1 and 100 inclusive!")
            level_ups: str = str(convo.last.text.split("\n")[0])
            for i in range(int(level_ups)):
                saved_game_data.player_data.level_up()


if __name__ == '__main__':
    main()
