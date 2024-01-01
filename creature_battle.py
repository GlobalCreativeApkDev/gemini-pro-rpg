"""
This file contains code for generating a complex creature battle turn-based strategy RPG using Gemini Pro.
Author: GlobalCreativeApkDev
"""


# Importing necessary libraries


import sys
import uuid
import pickle
import copy
import google.generativeai as gemini
from datetime import datetime
import os
from functools import reduce
from dotenv import load_dotenv
from tabulate import tabulate
from mpmath import mp, mpf

mp.pretty = True


# Creating static functions to be used in this game.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def triangular(n: int) -> int:
    return int(n * (n - 1) / 2)


def mpf_sum_of_list(a_list: list) -> mpf:
    return mpf(str(sum(mpf(str(elem)) for elem in a_list if is_number(str(elem)))))


def mpf_product_of_list(a_list: list) -> mpf:
    return mpf(reduce(lambda x, y: mpf(x) * mpf(y) if is_number(x) and
                                                      is_number(y) else mpf(x) if is_number(x) and not is_number(
        y) else mpf(y) if is_number(y) and not is_number(x) else 1, a_list, 1))


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


class Action:
    """
    This class contains attributes of an action that can occur during battles.
    """

    POSSIBLE_NAMES: list = ["NORMAL ATTACK", "NORMAL HEAL", "USE SKILL"]

    def __init__(self, name):
        # type: (str) -> None
        self.name: str = name if name in Action.POSSIBLE_NAMES else Action.POSSIBLE_NAMES[0]

    # TODO: execute action based on name

    def clone(self):
        # type: () -> Action
        return copy.deepcopy(self)


class AwakenBonus:
    """
    This class contains attributes of the bonus gained for awakening a legendary creature.
    """


class Battle:
    """
    This class contains attributes of a battle in a creature battle RPG.
    """

    def __init__(self, battle_team1, battle_team2):
        # type: (BattleTeam, BattleTeam) -> None
        self.battle_team1: BattleTeam = battle_team1
        self.battle_team2: BattleTeam = battle_team2

    # TODO: implement battle

    def clone(self):
        # type: () -> Battle
        return copy.deepcopy(self)


class BattleArea:
    """
    This class contains attributes of a battle area.
    """

    def __init__(self, name, levels, clear_reward):
        # type: (str, list, Reward) -> None
        self.name: str = name
        self.__levels: list = levels
        self.clear_reward: Reward = clear_reward
        self.is_cleared: bool = False

    def get_levels(self):
        # type: () -> list
        return self.__levels

    def clone(self):
        # type: () -> BattleArea
        return copy.deepcopy(self)


class MapArea(BattleArea):
    """
    This class contains attributes of a map area.
    """

    POSSIBLE_MODES: list = ["EASY", "NORMAL", "HARD", "HELL"]

    def __init__(self, name, levels, clear_reward, mode):
        # type: (str, list, Reward, str) -> None
        BattleArea.__init__(self, name, levels, clear_reward)
        self.mode: str = mode if mode in self.POSSIBLE_MODES else self.POSSIBLE_MODES[0]


class Dungeon(BattleArea):
    """
    This class contains attributes of a dungeon.
    """

    POSSIBLE_TYPES: list = ["RESOURCE", "ITEM"]

    def __init__(self, name, levels, clear_reward, dungeon_type):
        # type: (str, list, Reward, str) -> None
        BattleArea.__init__(self, name, levels, clear_reward)
        self.dungeon_type: str = dungeon_type if dungeon_type in self.POSSIBLE_TYPES else self.POSSIBLE_TYPES[0]


class Level:
    """
    This class contains attributes of a level in a battle area.
    """

    def __init__(self, name, stages, clear_reward):
        # type: (str, list, Reward) -> None
        self.name: str = name
        self.__stages: list = stages
        self.clear_reward: Reward = clear_reward
        self.is_cleared: bool = False

    def get_stages(self):
        # type: () -> list
        return self.__stages

    def clone(self):
        # type: () -> Level
        return copy.deepcopy(self)


class Stage:
    """
    This class contains attributes of a stage inside a level.
    """

    def __init__(self, enemies_list):
        # type: (list) -> None
        self.__enemies_list: list = enemies_list
        self.is_cleared: bool = False

    def clone(self):
        # type: () -> Stage
        return copy.deepcopy(self)


class BattleTeam:
    """
    This class contains attributes of a team brought to battles.
    """

    def __init__(self, max_legendary_creatures, legendary_creatures=None):
        # type: (int, list) -> None
        if legendary_creatures is None:
            legendary_creatures = []
        self.max_legendary_creatures: int = max_legendary_creatures
        self.__legendary_creatures: list = legendary_creatures if len(legendary_creatures) <= \
                                                                  self.max_legendary_creatures else []
        self.leader: LegendaryCreature or None = None if len(self.__legendary_creatures) == 0 else \
            self.__legendary_creatures[0]

    def set_leader(self, leader):
        # type: (LegendaryCreature) -> None
        self.leader = None if len(self.__legendary_creatures) == 0 or leader not in self.__legendary_creatures else \
            leader

    def add_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if len(self.__legendary_creatures) < self.max_legendary_creatures:
            self.__legendary_creatures.append(legendary_creature)
            return True
        return False

    def remove_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.__legendary_creatures:
            self.__legendary_creatures.remove(legendary_creature)
            return True
        return False

    def get_legendary_creatures(self):
        # type: () -> list
        return self.__legendary_creatures

    def clone(self):
        # type: () -> BattleTeam
        return copy.deepcopy(self)


class LegendaryCreature:
    """
    This class contains attributes of a legendary creature in a creature battle RPG.
    """


class FusionLegendaryCreature(LegendaryCreature):
    """
    This class contains attributes of a fusion legendary creature.
    """


class Element:
    """
    This class contains attributes of an element a legendary creature can have.
    """

    def __init__(self, name, strengths, weaknesses):
        # type: (str, list, list) -> None
        self.name: str = name
        self.__strengths: list = strengths
        self.__weaknesses: list = weaknesses

    def get_strengths(self):
        # type: () -> list
        return self.__strengths

    def get_weaknesses(self):
        # type: () -> list
        return self.__weaknesses

    def clone(self):
        # type: () -> Element
        return copy.deepcopy(self)


class Skill:
    """
    This class contains attributes of a skill legendary creatures have.
    """


class ActiveSkill(Skill):
    """
    This class contains attributes of an active skill which is manually used.
    """


class PassiveSkill(Skill):
    """
    This class contains attributes of a passive skill which is automatically used.
    """


class PassiveSkillEffect:
    """
    This class contains attributes of the effect of a passive skill.
    """


class LeaderSkill(Skill):
    """
    This class contains attributes of a leader skill.
    """


class LeaderSkillEffect:
    """
    This class contains attributes of the effect of a leader skill.
    """


class DamageMultiplier:
    """
    This class contains attributes of the damage multiplier of a skill.
    """


class BeneficialEffect:
    """
    This class contains attributes of a beneficial effect a legendary creature has.
    """


class HarmfulEffect:
    """
    This class contains attributes of a harmful effect a legendary creature has.
    """


class Item:
    """
    This class contains attributes of an item in a creature battle RPG.
    """


class Rune(Item):
    """
    This class contains attributes of a rune used to strengthen legendary creatures.
    """


class StatIncrease:
    """
    This class contains attributes of the increase in stats when equipping a rune.
    """


class AwakenShard(Item):
    """
    This class contains attributes of an awaken shard used to instantly awaken a legendary creature.
    """


class EXPShard(Item):
    """
    This class contains attributes of a shard used to increase the EXP of legendary creatures.
    """


class LevelUpShard(Item):
    """
    This class contains attributes of a level up shard used to immediately level up a legendary creature.
    """


class SkillLevelUpShard(Item):
    """
    This class contains attributes of a skill level up shard to level up skills owned by legendary creatures.
    """


class Scroll(Item):
    """
    This class contains attributes of a scroll used to summon legendary creatures.
    """


class ItemShop:
    """
    This class contains attributes of an item shop selling items.
    """

    def __init__(self, name, items_sold):
        # type: (str, list) -> None
        self.name: str = name
        self.__items_sold: list = items_sold

    def get_items_sold(self):
        # type: () -> list
        return self.__items_sold

    def clone(self):
        # type: () -> ItemShop
        return copy.deepcopy(self)


class Player:
    """
    This class contains attributes of a player of a creature battle RPG.
    """

    def __init__(self, name, required_exp, max_legendary_creatures):
        # type: (str, mpf, int) -> None
        self.player_id: str = str(uuid.uuid1())
        self.name: str = name
        self.level: int = 1
        self.exp: mpf = mpf("0")
        self.required_exp: mpf = required_exp
        self.gold: mpf = mpf("0")
        self.gems: mpf = mpf("0")
        self.battle_team: BattleTeam = BattleTeam(max_legendary_creatures)
        self.item_inventory: ItemInventory = ItemInventory()
        self.legendary_creature_inventory: LegendaryCreatureInventory = LegendaryCreatureInventory()
        self.player_base: PlayerBase = PlayerBase()

    def clone(self):
        # type: () -> Player
        return copy.deepcopy(self)


class ItemInventory:
    """
    This class contains attributes of an inventory containing items.
    """

    def __init__(self, items=None):
        # type: (list) -> None
        if items is None:
            items = []
        self.__items: list = items

    def get_items(self):
        # type: () -> list
        return self.__items

    def add_item(self, item):
        # type: (Item) -> None
        self.__items.append(item)

    def remove_item(self, item):
        # type: (Item) -> bool
        if item in self.__items:
            self.__items.remove(item)
            return True
        return False

    def clone(self):
        # type: () -> ItemInventory
        return copy.deepcopy(self)


class LegendaryCreatureInventory:
    """
    This class contains attributes of an inventory containing legendary creatures.
    """

    def __init__(self, legendary_creatures=None):
        # type: (list) -> None
        if legendary_creatures is None:
            legendary_creatures = []
        self.__legendary_creatures: list = legendary_creatures

    def get_legendary_creatures(self):
        # type: () -> list
        return self.__legendary_creatures

    def add_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> None
        self.__legendary_creatures.append(legendary_creature)

    def remove_legendary_creature(self, legendary_creature):
        # type: (LegendaryCreature) -> bool
        if legendary_creature in self.__legendary_creatures:
            self.__legendary_creatures.remove(legendary_creature)
            return True
        return False

    def clone(self):
        # type: () -> LegendaryCreatureInventory
        return copy.deepcopy(self)


class PlayerBase:
    """
    This class contains attributes of player's base.
    """

    def __init__(self, island_build_gold_cost):
        # type: (mpf) -> None
        self.__islands: list = [Island()]  # initial value
        self.island_build_gold_cost: mpf = island_build_gold_cost

    def add_island(self):
        # type: () -> None
        self.island_build_gold_cost *= mpf("10") ** (triangular(len(self.__islands)))
        self.__islands.append(Island())

    def get_islands(self):
        # type: () -> list
        return self.__islands

    def clone(self):
        # type: () -> PlayerBase
        return copy.deepcopy(self)


class Island:
    """
    This class contains attributes of an island in a player's base.
    """


class IslandTile:
    """
    This class contains attributes of a tile on an island.
    """


class Building:
    """
    This class contains attributes of a building to be built on an island tile.
    """


class BuildingShop:
    """
    This class contains attributes of a shop selling buildings.
    """


class Reward:
    """
    This class contains attributes of the reward gained for doing something in this game.
    """


class SavedGameData:
    """
    This class contains attributes of saved game data.
    """

    def __init__(self, game_name, temperature, top_p, top_k, max_output_tokens):
        # type: (str, float, float, float, int) -> None
        self.game_name: str = game_name
        self.temperature: float = temperature
        self.top_p: float = top_p
        self.top_k: float = top_k
        self.max_output_tokens: int = max_output_tokens

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
        saved_game_files: list = [f for f in os.listdir("saved_creature_battle")]
        while game_name in saved_game_files:
            print("Below is a list of existing games:\n")
            for i in range(len(saved_game_files)):
                print(str(i + 1) + ". " + str(saved_game_files[i]))

            game_name = input("Sorry, the game " + str(game_name) + " already exists! "
                "Enter another name of the game you are playing: ")

        player_name: str = input("Please enter your name: ")
        convo = model.start_chat(history=[
        ])
        # TODO: create SavedGameData object
        saved_game_data = SavedGameData(game_name, float_temperature, float_top_p, float_top_k,
                                        int_max_output_tokens)
    else:
        clear()

        saved_game_files: list = [f for f in os.listdir("saved_creature_battle")]
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

        saved_game_data = load_game_data(os.path.join("saved_creature_battle", game_name))

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
            save_game_data(saved_game_data, os.path.join("saved_creature_battle", game_name))
            return 0  # successfully saved the game

        clear()
        convo = model.start_chat(history=[
        ])


if __name__ == '__main__':
    main()
