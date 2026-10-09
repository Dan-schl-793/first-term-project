import time
import random
from itertools import zip_longest

#logic for esc to exit the game at any time
import sys
import msvcrt

def safe_input(prompt):
    """Read input while checking for Escape to quit instantly."""
    print(prompt, end="", flush=True)
    text = ""

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getwch()

            if key == '\x1b':
                print("\nEscape pressed. Exiting...")
                sys.exit(0)

            if key in ('\r', '\n'):
                print()
                return text

            if key == '\b':
                if text:
                    text = text[:-1]
                    print('\b \b', end="", flush=True)
                continue

            if key in ('\x00', '\xe0'):
                msvcrt.getwch()
                continue

            if key.isprintable():
                text += key
                print(key, end="", flush=True)

#opening title card and message
with open("title_card.txt", "r") as file:
    content = file.read().splitlines()
    for line in content:
        print(line)


def prompt_choice(prompt, valid_choices, invalid_message="Invalid choice. Please try again."):
    """Loop until the user enters one of the valid choices."""
    valid_choices = {choice.lower() for choice in valid_choices}
    while True:
        choice = safe_input(prompt).strip()
        if choice.lower() in valid_choices:
            return choice
        print(invalid_message)


def show_player_stats(player):
    """Display the key character and party statistics for the player."""
    print("\n=== Character Status ===")
    print(f"Name: {player.name}")
    print(f"Class: {player.class_name}")
    print(f"Party size: {player.party_members}")
    print(f"HP: {player.hp}/{player.max_hp}")
    print(f"Strength: {player.attack_power}")
    print(f"Defense: {player.defense}")
    print(f"Agility: {player.agility}")
    print(f"Lives remaining: {player.lives}")
    print(f"Experience: {player.experience}")


enter = prompt_choice(
    "press [S]tart. press [E]xit, you can also press [ESC] to exit the game at any time: ",
    ["S", "E"],
    "Invalid choice. Please press [S] to start or [E] to exit."
)

if enter.lower() == "s":
    print("\nplease ensure to have your terminal window enlarged for the best playing experience.")
    time.sleep(3)

    # opening message
    with open("opening_paragraph.txt", "r") as file:
        opening_paragraph = file.read()

    print()
    print(opening_paragraph)

elif enter.lower() == "e":
    print("You chose to exit.")
    sys.exit(0)

#character creation
player_exp = 0
print("\n   -   Before you begin your journey, you must first create your character.")

#character name input
while True:
    character_name = safe_input("\nWhat is your name, brave knight?: ").strip()
    if not character_name:
        print("Your knight name cannot be empty. Please enter a valid name.")
    elif len(character_name) > 20:
        print("Your knight name must be 20 characters or fewer. Please try again.")
    else:
        break

name_reply = ["What an amazing choice, ", "Such a noble name, ", "A name that echoes with courage, "]
print(random.choices(name_reply, weights=[0.333, 0.333, 0.333])[0], "", character_name,"!")

#character health input
while True:
    try:
        character_lives = int(safe_input("\nNow it's time to choose the amount of lives you want. The default is 3, going higher than 3 would make\n"
                                         " the game more forgiving and going below will make it more of a challenge. what will you choose?: "))
        break
    except ValueError:
        print("Invalid input. Please enter a valid number.")

#response to character health input
if character_lives > 3:
    print("\nYou have chosen to have more than the default amount of lives; it would be a bit embarrassing if you fail! Good luck!")
elif character_lives < 3:
    print("\nYou have chosen to have less than the default amount of lives; this is going to be a challenge. Good luck!")
elif character_lives == 3:
    print("\nYou have chosen to have the default amount of lives; this is a balanced choice. Good luck!")
elif character_lives <= 0:
    print("\nYou can't have 0 or less lives, so you will be given the default amount of lives. Good luck!")

#weapon set selection
print("\n\n - next we must determine your starting class.\n - You can choose from a sword and shield, a bow and sword, or a spear and shield.\n"
      " - Each weapon set has its own strengths and weaknesses which will be displayed by typing inspect into the terminal.\n" \
      " - You will then get the choice of whether you would like to pick that option or go back to the list and select another.")
print()
print()
class_arts = []
for art_file in ("warrior_class.txt", "archer_class.txt", "paladin_class.txt"):
    with open(art_file, "r") as file:
        class_arts.append(file.read().splitlines())

column_widths = [max(map(len, art)) for art in class_arts]
for art_row in zip_longest(*class_arts, fillvalue=""):
    print("  ".join(line.ljust(width) for line, width in zip(art_row, column_widths)))


#class choice input
class_details = {
    "warrior": (
        "1",
        "The warrior is balanced, with moderate attack, defense and mobility. It has less range than the paladin and cannot attack from a distance like the archer.",
    ),
    "archer": (
        "2",
        "The archer attacks from distance, close and has high mobility, using a dagger and bow. But cannot parry like the warrior or paladin due to its lack of a shield.",
    ),
    "paladin": (
        "3",
        "The paladin uses a halberd for mid-close range and a large shield for strong parries, but has the least mobility.",
    ),
}

while True:
    class_set = prompt_choice(
        "\nselect a class: [warrior], [archer], or [paladin]: ",
        class_details,
        "Invalid class choice. Please choose warrior, archer, or paladin.",
    ).lower()
    action = prompt_choice(
        f"Would you like to [choose] or [inspect] the {class_set} class?: ",
        ["choose", "inspect"],
        "Please type choose or inspect.",
    ).lower()

    if action == "inspect":
        print(f"\n{class_details[class_set][1]}")
        action = prompt_choice(
            "Type [choose] to select this class or [back] to return to the class list: ",
            ["choose", "back"],
            "Please type choose or back.",
        ).lower()
        if action == "back":
            continue

    weapon_set = class_details[class_set][0]
    break

#location lists
first_location = ["the lowlands", "ronderdale", "the dark forest", "kyrlo castle"]
second_location = ["the midlands", "clonsel", "hebra village", "kyrlo castle"]
third_location = [ "the highlands", "the cursed swamp", "the dragon's lair", "kyrlo castle"]
fourth_location = ["the frosty peaks", "valcano pass", "kyrlo castle"]
final_battle = ["krylo castle"]

#checking if the player or enemy is still alive based on their health points
class Character:
    """Base class for any entity participating in combat."""
    def __init__(self, name: str, max_hp: int, attack_power: int, defense: int):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack_power = attack_power
        self.defense = defense
        self.is_defending = False

    def is_alive(self) -> bool:
        return self.hp > 0
#calculating damage taken by the player and enemy based on their attack power and defense stats
    def take_damage(self, raw_damage: int):
        """Calculates mitigated damage and reduces health points."""
        mitigation = self.defense if not self.is_defending else self.defense * 2
        final_damage = max(1, raw_damage - mitigation)
        self.hp = max(0, self.hp - final_damage)
        print(f"{self.name} takes {final_damage} damage! (HP: {self.hp}/{self.max_hp})")
#deciding how much damage the player and enemy do to each other based on their attack power and defense stats
    def attack(self, target: 'Character'):
        """Deals randomized damage to a target based on base attack power."""
        print(f"{self.name} attacks {target.name}!")
        variance = random.randint(-2, 4)
        raw_damage = self.attack_power + variance

        if random.random() < 0.10:
            raw_damage = int(raw_damage * 1.5)
            print("CRITICAL HIT!")

        target.take_damage(raw_damage)
#resetting defensive states at the start of a turn to ensure that defense only applies for one turn
    def reset_status(self):
        """Resets temporary defensive states at the start of a turn."""
        self.is_defending = False

#additional player attributes and methods for inventory management, experience, and life tracking
class Player(Character):
    """Player subclass with life tracking, experience, and inventory items."""
    def __init__(self, name: str, max_hp: int, attack_power: int, defense: int, class_name: str):
        super().__init__(name, max_hp, attack_power, defense)
        self.class_name = class_name
        self.lives = 1
        self.experience = 0
        self.gold = 0
        self.party_members = 0
        self.agility = 5
        self.inventory = {}
#adding items to the inventory logic
    def add_item(self, item_name, quantity=1):
        """Add a found item to the player's inventory."""
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity
        print(f"{self.name} picked up {quantity} {item_name}.")
#fixed so that the player can view their inventory without spending a turn
    def view_inventory(self):
        """Shows the player's inventory without spending a turn."""
        if not self.inventory:
            print("Your inventory is empty.")
            return

        print("\nInventory:")
        for item, count in self.inventory.items():
            if count > 0:
                print(f"- {item} x{count}")
#inventory use logic
    def use_inventory(self, enemy=None):
        """Lets the player use an item they have collected on the journey."""
        if not self.inventory or not any(count > 0 for count in self.inventory.values()):
            print("Your inventory is empty.")
            return False

        self.view_inventory()

        choice = safe_input("\nType the item name to use it, or [cancel] to leave: ").strip().lower()

        if choice == "cancel":
            return False

        if choice not in self.inventory or self.inventory[choice] <= 0:
            print("You do not have that item.")
            return False

        print("That item is not useful right now.")
        return False
#what happens if player health reaches 0 (lose a life and restore full health + end battle on a loss)
    def lose_life(self):
        """When HP reaches 0, lose one life and restore the full HP bar."""
        if self.lives > 0:
            self.lives -= 1
            self.hp = self.max_hp
            print(f"{self.name} lost a life! Remaining lives: {self.lives}")
            if self.lives <= 0:
                self.hp = 0
                print(f"{self.name} has no lives left. Game over.")

#deciding enemy stats and behaviour
class Enemy(Character):
    """Enemy subclass with basic automated AI."""
    def take_turn(self, target: Character):
        """Simple AI: Defends if low on health, otherwise attacks."""
        if self.hp < (self.max_hp * 0.25) and random.random() < 0.5:
            self.is_defending = True
            print(f"{self.name} takes a defensive stance!")
        else:
            self.attack(target)

#battle loop function that manages the turn-based system
def battle_loop(player: Player, enemy: Enemy):
    """Manages the loop of the turn-based system."""
    print(f"\nA wild {enemy.name} appeared! It engages you in battle!\n")
    turn_counter = 1
#deciding if another turn should be taken based on the health of the player and enemy
    while player.is_alive() and enemy.is_alive():
        print(f"\n=== TURN {turn_counter} ===")
        print(f"{player.name}: {player.hp}/{player.max_hp} HP | {enemy.name}: {enemy.hp}/{enemy.max_hp} HP")
        print("-" * 30)
#player chooses action
        player.reset_status()
        print("Choose your action:")
        print("1. Attack")
        print("2. Defend")
        print("3. Inventory")

        choice = safe_input("Enter choice (1-3): ").strip()
        print()
#check if player used an item in the inventory, if not, continue with the battle loop
        inventory_used = False
#what happens depending on action choice, does the player chooses to attack, defend or use an item from the inventory
        if choice == "1":
            player.attack(enemy)
        elif choice == "2":
            player.is_defending = True
            print(f"{player.name} braces for the next impact!")
        elif choice == "3":
            while True:
                if not player.inventory:
                    print("Inventory empty.")
                    inventory_choice = safe_input("Type [cancel] to return to battle: ").strip().lower()
                    if inventory_choice == "cancel":
                        print("You close your inventory and keep fighting.")
                        inventory_used = False
                        break
                    print("That is not a valid option.")
                    continue

                player.view_inventory()
                print("\nInventory options:")
                print("- Type the name of an item to use it")
                print("- Type [cancel] to return to battle")
                inventory_choice = safe_input("What do you want to do? ").strip().lower()

                if inventory_choice == "cancel":
                    print("You close your inventory and keep fighting.")
                    inventory_used = False
                    break

                if inventory_choice not in player.inventory or player.inventory[inventory_choice] <= 0:
                    print("You do not have that item.")
                    continue

                inventory_used = player.use_inventory(enemy)
                break

            if choice == "3" and not inventory_used:
                print("You take a moment to check your gear, then get back into the fight.")
                continue
        else:
            print("Invalid choice! You stumbled and lost your turn.")

        if not enemy.is_alive():
            player.experience += 10
            player.hp = player.max_hp
            print(f"\n{enemy.name} has been defeated! {player.name} wins!")
            print(f"{player.name} gains 10 experience points! Total XP: {player.experience}")
            return "win"

        if not player.is_alive():
            if player.lives > 0:
                player.lose_life()
                player.hp = player.max_hp
                print(f"{player.name} is back at full HP and the battle is over.")
                print(f"{enemy.name} wins this round.")
                return "loss"
            else:
                print(f"\n{player.name} has fallen in battle. Game Over.")
                player.hp = 0
                return "loss"

        time.sleep(1)

        enemy.reset_status()
        print(f"\n--- {enemy.name}'s Turn ---")
        enemy.take_turn(player)

        if not player.is_alive():
            if player.lives > 0:
                player.lose_life()
                player.hp = player.max_hp
                print(f"{player.name} is back at full HP and the battle ends here.")
                print(f"{enemy.name} wins this round.")
                return "loss"
            else:
                print(f"\n{player.name} has fallen in battle. Game Over.")
                player.hp = 0
                return "loss"

        turn_counter += 1
        time.sleep(1)

    if enemy.hp <= 0 and player.hp > 0:
        return "win"
    if player.hp <= 0:
        return "loss"
    return "loss"


#starting gameplay
print(f"\nNow that you have your character, it's time to begin your journey. Good luck, {character_name}!")

#location selection mechanic explanation
print("\nYou will go through 5 different location tiers in this game. There are locations in tiers 1 through 4, and then a final battle at the fallen throne.\n"
" Each location tier has 4 locations to choose from, and you will need to pick one to travel to. You will be able to travel back and forth between locations in\n"
" the same tier, but you will not be able to go back to a previous tier once you have moved on.")

location_descriptions = {
    "the lowlands": "The lowlands are a broad area of open grassland with many weak enemies and a few scattered survivors.",
    "ronderdale": "Ronderdale is a market town on the edge of the kingdom. It is safer than the wild frontier and offers healing, upgrades, and easier quests.",
    "the dark forest": "The dark forest is a dense woodland packed with beasts and ambushes. It rewards brave adventurers with stronger experience gains.",
    "the wastelands": "The wastelands are a ruined battlefield of broken stone and ash. Few enemies remain, but hidden treasure may still be found here.",
    "the midlands": "The midlands are rolling hills crossed by patrol routes and ruined roads, filled with raiders and scouts.",
    "clonsel": "Clonsel is a fortified trade city known for its stone walls and well-trained guards. It is a steady place to gather information and rest.",
    "hebra village": "Hebra village sits near a river and is populated by survivors who need help defending their homes from roaming attackers.",
    "the ruined bridge": "The ruined bridge stretches over a deep ravine and is haunted by ambushers who use the broken stones as cover.",
    "the highlands": "The highlands rise into harsh cliffs and narrow mountain paths. The land is cold, steep, and full of dangerous patrols.",
    "the cursed swamp": "The cursed swamp is a soggy nightmare of mud, fog, and monstrous creatures. It is a risky but rewarding route through the kingdom.",
    "the dragon's lair": "The dragon's lair is a volcanic cavern where ancient winged beasts guard their nests and treasure hoards.",
    "the obsidian gate": "The obsidian gate is a giant black fortress entrance covered in ash and old sigils, protected by elite guards.",
    "the frosty peaks": "The frosty peaks are icy ridges where the cold is brutal and the enemy patrols are relentless.",
    "volcano pass": "Volcano pass is a narrow path cut through a steaming mountain range, filled with fire-wreathed monsters.",
    "the glass caverns": "The glass caverns are crystal-lined tunnels that reflect light unnaturally and hide deadly ambushes.",
    "the moonlit ruins": "The moonlit ruins are a silent, ancient fortress where old magic still flickers beneath the stone.",
    "krylo castle": "The fallen throne is the final battlefield of the war, where the last resistance will stand against the enemy's dark ruler."
}

first_location = ["the lowlands", "ronderdale", "the dark forest", "krylo castle"]
second_location = ["the midlands", "clonsel", "hebra village", "krylo castle"]
third_location = [ "the highlands", "the cursed swamp", "the dragon's lair", "krylo castle"]
fourth_location = ["the frosty peaks", "volcano pass", "krylo castle"]
final_battle = ["krylo castle"]

#first location selection
print("\nyou will first need to decide the first location you will travel to.")
print("\nthese are your options for the first location:")
print(first_location)
valid_locations = [location.lower() for location in first_location]

while True:
    first_location_choice = prompt_choice(
        "\nby entering the name of a location you will be given details about the location and you will be able to choose whether to go there or not: ",
        valid_locations,
        "Invalid location. Please choose one from the list."
    )

    print(f"\n{location_descriptions[first_location_choice.lower()]}")

    travel_or_back1 = prompt_choice(
        "\ntype [travel] to go to this location or type [back] to go back to the list of locations: ",
        ["travel", "back"],
        "Invalid choice. Please type [travel] or [back]."
    )

    if travel_or_back1.lower() == "travel":
        break

    print()
    print(first_location)

#traveling to the first location
print(f"Traveling to {first_location_choice}...")
time.sleep(1)
print(f"Traveling to {first_location_choice}...")
time.sleep(1)
print(f"Traveling to {first_location_choice}...")
time.sleep(1)
print(f"Traveling to {first_location_choice}...")
time.sleep(1)

#deciding whether to battle or flee from enemies in the new location
if first_location_choice != "the wastelands":
    print("\nwhen entering certain new locations you cannot do any other actions until you have slain the nearby enemies.")

while True:
    welcome_message = prompt_choice(
        f"\nYou have arrived at {first_location_choice}, would you like to either [flee] or [battle] nearby enemies?: ",
        ["flee", "battle"],
        "Invalid choice. Please type [flee] or [battle]."
    )
    battle_message1 = ("your first battle is with a chulu, a chimp looking creature with medium health but low damage output")

    if welcome_message.lower() == "flee":
        print("\nyou have fled Ronderdale, you can now choose where you would like to go from here")
        print(first_location)
        continue

    if welcome_message.lower() == "battle":
        with open("chulu.txt", "r") as file:
            content = file.read().splitlines()
            for line in content:
                print(line)
        print(f"\n\n{battle_message1}")
        break

#defining player stats based on character creation choices
knight = Player(
    name=character_name,
    max_hp=50,
    attack_power=12,
    defense=3,
    class_name=class_set,
)
knight.lives = character_lives
#deciding player dmg and defence based on weapon set choice
if weapon_set == "1":
    knight.attack_power += 4
    knight.defense += 3
    knight.agility += 2
elif weapon_set == "2":
    knight.attack_power += 3
    knight.defense += 4
    knight.agility += 5
elif weapon_set == "3":
    knight.attack_power += 5
    knight.defense -= 1
    knight.agility += 1
#defining enemy stats and starting the battle loop
villain = Enemy(name="Chulu", max_hp=30, attack_power=random.randint(5, 9), defense=1)
battle_result = battle_loop(knight, villain)

if battle_result == "win":
    print("\nThe Chulu has been defeated. The close area is now safe.")
    print(f"\nYou earned 10 experience points for defeating the Chulu! Total XP: {knight.experience}")
    print("\nNow that you have defeated the Chulu, you can continue your journey.")
else:
    print("\nThe Chulu defeats you and the battle ends.")
    print(f"{knight.name}, you have lost a life and returned to full health.")
    print("\nYou can try again from the start of this encounter.")

player_next_action1 = safe_input("\nYou have a few options of what you can do from here.\nYou can [explore] the area, type [talk]"
                                 " to other characters and find out more about them and your enemies, type [travel] to another location, or type [status]\n"
                                 " to check your condition and use experience points: ").strip().lower()

if player_next_action1 == "explore":
    explore_outcomes1 = ["You explore the area and find nothing of interest.", "You explore the area and find a chest."]
    result = random.choice(explore_outcomes1)
    print(result)
    open1 = prompt_choice(
        "\nType [open] to open the chest or [leave] to leave it alone: ",
        ["open", "leave"],
        "Invalid choice. Please type [open] or [leave]."
    )
    if open1.lower() == "open":
        chest_outcomes1 = ["You found a health potion!.", "You found a damage potion!.", "You found 5 gold coins!."]
        result = random.choice(chest_outcomes1)
        print(result)
        if "5 gold coins" in result.lower():
            knight.gold += 5
            print(f"You gained 5 gold coins. Total gold: {knight.gold}")
        knight.experience += 5
        print(f"\nYou also earned 5 experience points for opening the chest! Total XP: {knight.experience}")
        stats1 = safe_input("\nwould you like to see your updated stats? type [yes] or [no]: ")
        if stats1.lower() == "yes":
            show_player_stats(knight)
        else:
            print("You chose not to view your stats.")
    elif open1.lower() == "leave":
        print("You leave the chest alone and continue exploring.")
    else:
        print("Invalid choice. You leave the chest alone and continue exploring.")

if player_next_action1 == "talk":
    print("\nYou talk to the villager, patrick. He tells you about the recent attacks by the Zoli civilisation and their leader Yohl.")
    print("He also mentions that there are other survivors in the area who might be able to help you on your journey.")
    
    character_accept1 = safe_input("\nwould you like to [recruit] patrick or [leave] him alone?: ")
    if character_accept1.lower() == "recruit":
        knight.party_members += 1
        print("\nYou have recruited a survivor to join your party. They will help you in battles and provide support.")
        knight.add_item("Survivor Ally", 1)
        print(f"Your party now has {knight.party_members} member(s).")
    elif character_accept1.lower() == "leave":
        print("\nYou decide not to recruit the survivor and continue on your journey.")

if player_next_action1 == "travel":
    second_location_choice = prompt_choice(
        "\nYou can either travel to another location in the same tier or move on to the next tier of locations. You cannot go back to a previous tier once you have moved on so be careful to not move on too quickly.\n"
        "Type [same] to travel to another location in the same tier or type [next] to move on to the next tier of locations: ",
        ["same", "next"],
        "Invalid choice. Please type [same] or [next]."
    )

    if second_location_choice.lower() == "same":
        print("\nYou have chosen to travel to another location in the same tier. Here are your options:")
        print(second_location)
    elif second_location_choice.lower() == "next":
        print("\nYou have chosen to move on to the next tier of locations. Here are your options:")
        print(second_location)

if player_next_action1 == "status":
    show_player_stats(knight)

choice2 = safe_input("\nwhat would you like to do next? Do you need a reminder of your options? type [yes] or [no]: ")
if choice2.lower() == "yes":
    player_next_action2 = safe_input("\nYou can [explore] the area, type [talk] to other characters and find out more about them and your enemies,\n"
                                     "type [travel] to another location, or type [status]to check your condition and use experience points: ").strip().lower()
elif choice2.lower() == "no":
    player_next_action2 = safe_input("\nOkay what would you like to do next?: ").strip().lower()
else:
    safe_input("\nInvalid choice. Please type [yes] or [no]: ")


if player_next_action2 == "explore":
    explore_outcomes2 = ["You explore the area and find nothing of interest.", "You explore the area and find a chest."]
    result = random.choice(explore_outcomes2)
    print(result)
    open2 = prompt_choice(
        "\nType [open] to open the chest or [leave] to leave it alone: ",
        ["open", "leave"],
        "Invalid choice. Please type [open] or [leave]."
    )
    if open2.lower() == "open":
        chest_outcomes2 = ["You found a health potion!.", "You found a damage potion!.", "You found 5 gold coins!."]
        result = random.choice(chest_outcomes2)
        print(result)
        if "5 gold coins" in result.lower():
            knight.gold += 5
            print(f"You gained 5 gold coins. Total gold: {knight.gold}")
        knight.experience += 5
        print(f"\nYou also earned 5 experience points for opening the chest! Total XP: {knight.experience}")
        stats2 = safe_input("\nwould you like to see your updated stats? type [yes] or [no]: ")
        if stats2.lower() == "yes":
            show_player_stats(knight)
        else:
            print("You chose not to view your stats.")
    elif open2.lower() == "leave":
        print("You leave the chest alone and continue exploring.")

if player_next_action2 == "talk":
    repair_or_not1 = safe_input("\nYou talk to the blacksmith, John. He tells you about how he can improve one your weapons damage stat if you give him 5 gold coins. Would you like to pay him? type [yes] or [no]: ")
    if repair_or_not1.lower() == "yes":
        if knight.gold >= 5:
            knight.gold -= 5
            if knight.class_name.lower() == "archer":
                knight.attack_power += 4
                print(f"\nYou paid John 5 gold coins and improved your dagger and bow damage! New attack power: {knight.attack_power}")
            else:
                knight.attack_power += 2
                print(f"\nYou paid John 5 gold coins and improved your weapon's damage! New attack power: {knight.attack_power}")
        else:
            print("You don't have enough gold coins.")
    elif repair_or_not1.lower() == "no":
        print("You decide not to pay the blacksmith and continue your journey.")

third_location_choice = prompt_choice(
        "\nYou can either travel to another location in the same tier or move on to the next tier of locations. You cannot go back to a previous tier once you have moved on so be careful to not move on too quickly.\n"
        "Type [same] to travel to another location in the same tier or type [next] to move on to the next tier of locations: ",
        ["same", "next"],
        "Invalid choice. Please type [same] or [next]."
    )

if player_next_action1 == "travel":
    third_location_choice = prompt_choice(
        "\nYou can either travel to another location in the same tier or move on to the next tier of locations. You cannot go back to a previous tier once you have moved on so be careful to not move on too quickly.\n"
        "Type [same] to travel to another location in the same tier or type [next] to move on to the next tier of locations: ",
        ["same", "next"],
        "Invalid choice. Please type [same] or [next]."
    )

    if third_location_choice.lower() == "same":
        print("\nYou have chosen to travel to another location in the same tier. Here are your options:")
        print(third_location)
    elif third_location_choice.lower() == "next":
        print("\nYou have chosen to move on to the next tier of locations. Here are your options:")
        print(third_location)

if player_next_action2 == "status":
    show_player_stats(knight)
