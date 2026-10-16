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

print("In this game when inputing your options will be the words or letters in square brackets. if there is nothing in square brackets it is numbers")

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
#(the 0 or less check has to come first, otherwise the "less than 3" branch catches it and it never runs)
if character_lives <= 0:
    print("\nYou can't have 0 or less lives, so you will be given the default amount of lives. Good luck!")
    character_lives = 3
elif character_lives > 3:
    print("\nYou have chosen to have more than the default amount of lives; it would be a bit embarrassing if you fail! Good luck!")
elif character_lives < 3:
    print("\nYou have chosen to have less than the default amount of lives; this is going to be a challenge. Good luck!")
elif character_lives == 3:
    print("\nYou have chosen to have the default amount of lives; this is a balanced choice. Good luck!")

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
first_location = ["the lowlands", "ronderdale", "the dark forest", "krylo castle"]
# second_location = ["the midlands", "clonsel", "hebra village", "krylo castle"]
# third_location = [ "the highlands", "the cursed swamp", "the dragon's lair", "krylo castle"]
# fourth_location = ["the frosty peaks", "valcano pass", "krylo castle"]
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
        self.agility = 0
        self.is_dodging = False

    def is_alive(self) -> bool:
        return self.hp > 0
#calculating damage taken by the player and enemy based on their attack power and defense stats
    def take_damage(self, raw_damage: int):
        """Calculates mitigated damage and reduces health points."""
        #dodging: each point of agility gives a 10% chance to take no damage at all
        if self.is_dodging:
            if random.random() < self.agility * 0.10:
                print(f"{self.name} dodges the attack and takes no damage!")
                return
            print(f"{self.name} tried to dodge but wasn't fast enough!")
        final_damage = max(1, raw_damage - self.defense)
        #blocking: each point of defense reduces the damage taken by a further 10%
        if self.is_defending:
            block_reduction = min(1.0, self.defense * 0.10)
            final_damage = max(1, int(final_damage * (1 - block_reduction)))
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
        self.is_dodging = False

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
        self.agility = 0
        self.inventory = {}
#adding items to the inventory logic
    def add_item(self, item_name, quantity=1):
        """Add a found item to the player's inventory."""
        #item names are stored lowercase so they can be matched against what the player types in
        item_name = item_name.lower()
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
    def use_inventory(self, enemy=None, item_name=None):
        """Lets the player use an item they have collected on the journey."""
        if not self.inventory or not any(count > 0 for count in self.inventory.values()):
            print("Your inventory is empty.")
            return False

        #if the battle loop already asked which item to use, don't ask a second time
        if item_name is None:
            self.view_inventory()
            choice = safe_input("\nType the item name to use it, or [cancel] to leave: ").strip().lower()
        else:
            choice = item_name.strip().lower()

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

#explains the combat actions, shown once before the very first fight
combat_explained = False

def explain_combat():
    """Explain what each combat action does."""
    print("\n=== How combat works ===")
    print("Each turn you choose one action:")
    print(" 1. Attack    - hit the enemy using your strength. Every attack has a 10% chance to be a critical hit for extra damage.")
    print(" 2. Block     - brace for the enemy's attack. The damage you take this turn is reduced by 10% for every 1 point of defense you have.")
    print(" 3. Dodge     - try to avoid the enemy's attack completely. Every 1 point of agility gives you a 10% chance to take no damage at all.")
    print("                You can only dodge twice per fight, and if the dodge fails you still take the full damage.")
    print(" 4. Inventory - check or use your items. Looking at your items does not use up your turn.")
    print("Your defense also lowers every hit you take by a flat amount, even when you are not blocking.")
    print("Your defense and agility are shown on your status screen, and some people you meet can help you improve them.")
    safe_input("\nPress [Enter] to begin the fight...")


#battle loop function that manages the turn-based system
def battle_loop(player: Player, enemy: Enemy):
    """Manages the loop of the turn-based system."""
    global combat_explained
    if not combat_explained:
        explain_combat()
        combat_explained = True
    print(f"\nA wild {enemy.name} appeared! It engages you in battle!\n")
    turn_counter = 1
    dodges_left = 2
#deciding if another turn should be taken based on the health of the player and enemy
    while player.is_alive() and enemy.is_alive():
        print(f"\n=== TURN {turn_counter} ===")
        print(f"{player.name}: {player.hp}/{player.max_hp} HP | {enemy.name}: {enemy.hp}/{enemy.max_hp} HP")
        print("-" * 30)
#player chooses action
        player.reset_status()
        print("Choose your action:")
        print("1. Attack")
        print("2. Block")
        print(f"3. Dodge ({dodges_left} left)")
        print("4. Inventory")

        choice = safe_input("Enter choice (1-4): ").strip()
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
            if dodges_left <= 0:
                print("You have no dodges left this fight, choose another action.")
                continue
            dodges_left -= 1
            player.is_dodging = True
            print(f"{player.name} prepares to dodge the next attack! ({dodges_left} dodge(s) left this fight)")
        elif choice == "4":
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

                inventory_used = player.use_inventory(enemy, inventory_choice)
                break

            if choice == "4" and not inventory_used:
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
                if player.lives <= 0:
                    #last life lost, lose_life already announced the game over
                    return "loss"
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
                if player.lives <= 0:
                    #last life lost, lose_life already announced the game over
                    return "loss"
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


#final boss encounter, uses the same battle logic as the chulu fight (flee/battle choice, art, battle loop, retry on a loss)
def yohl_encounter(player, location_name):
    """Offer the flee/battle choice for Yohl and run the fight."""
    battle_message1 = ("you have entered krylo castle, where yohl awaits your challenge ")

    while True:
        yohl_choice = prompt_choice(
            f"\nYou have arrived at {location_name}, would you like to either [flee] or [battle] the mighty Yohl?: ",
            ["flee", "battle"],
            "Invalid choice. Please type [flee] or [battle]."
        )

        if yohl_choice.lower() == "flee":
            print("\nYou flee from Krylo Castle. You can return when you are ready to face Yohl.")
            return

        if yohl_choice.lower() == "battle":
            #yohl's art file, if it isn't found the fight just starts without art
            try:
                with open("yohl.txt", "r") as file:
                    content = file.read().splitlines()
                    for line in content:
                        print(line)
            except FileNotFoundError:
                pass
            print(f"\n\n{battle_message1}")

            yohl = Enemy(name="Yohl", max_hp=200, attack_power=random.randint(15, 25), defense=10)
            yohl_battle_result = battle_loop(player, yohl)

            if yohl_battle_result == "win":
                print("\nYohl has been defeated! You have won the game.")
                sys.exit(0)
            else:
                if player.lives <= 0:
                    print("\nYohl defeats you. Your journey ends here.")
                    sys.exit(0)
                print("\nYohl defeats you and the battle ends.")
                print(f"{player.name}, you have lost a life and returned to full health.")
                print("\nYou can try again from the start of this encounter.")


#enemies found near each location, the chulu only lives around ronderdale (art is skipped for locations without an art file yet)
location_enemies = {
    "ronderdale": {
        "name": "Chulu", "max_hp": 30, "attack": (5, 9), "defense": 1, "art": "chulu.txt",
        "intro": "your first battle is with a chulu, a chimp looking creature with medium health but low damage output",
    },
    "the lowlands": {
        "name": "Zoli Raider", "max_hp": 35, "attack": (6, 10), "defense": 2, "art": None,
        "intro": "a zoli raider blocks your path, a low level soldier with average health and damage output",
    },
    "the dark forest": {
        "name": "Forest Beast", "max_hp": 60, "attack": (9, 14), "defense": 4, "art": None,
        "intro": "a forest beast stalks out of the trees, a powerful creature with high health and a heavy bite",
    },
    "the wastelands": {
        "name": "Scavenger", "max_hp": 25, "attack": (4, 7), "defense": 1, "art": None,
        "intro": "a lone scavenger spots you in the dust, a weak enemy with low health and low damage output",
    },
}


#the flee/battle choice for the enemies near a new location (the old chulu fight, now works for every location except krylo castle)
def arrival_encounter(player, location_name):
    """Returns True once the nearby enemies are beaten, False if the player flees."""
    foe = location_enemies[location_name.lower()]

    while True:
        welcome_message2 = prompt_choice(
            f"\nYou have arrived at {location_name}, would you like to either [flee] or [battle] nearby enemies?: ",
            ["flee", "battle"],
            "Invalid choice. Please type [flee] or [battle]."
        )

        if welcome_message2.lower() == "flee":
            print(f"\nyou have fled {location_name}, you can now choose where you would like to go from here")
            print(first_location)
            return False

        if welcome_message2.lower() == "battle":
            if foe["art"]:
                with open(foe["art"], "r") as file:
                    content = file.read().splitlines()
                    for line in content:
                        print(line)
            print(f"\n\n{foe['intro']}")

            villain = Enemy(name=foe["name"], max_hp=foe["max_hp"], attack_power=random.randint(*foe["attack"]), defense=foe["defense"])
            battle_result = battle_loop(player, villain)

            if battle_result == "win":
                print(f"\nThe {foe['name']} has been defeated. The close area is now safe.")
                print(f"\nYou earned 10 experience points for defeating the {foe['name']}! Total XP: {player.experience}")
                print(f"\nNow that you have defeated the {foe['name']}, you can continue your journey.")
                return True
            else:
                if player.lives <= 0:
                    print(f"\nThe {foe['name']} defeats you. Your journey ends here.")
                    sys.exit(0)
                print(f"\nThe {foe['name']} defeats you and the battle ends.")
                print(f"{player.name}, you have lost a life and returned to full health.")
                print("\nYou can try again from the start of this encounter.")


#starting gameplay
print(f"\nNow that you have your character, it's time to begin your journey. Good luck, {character_name}!")

#location selection mechanic explanation
# print("\nYou will go through 5 different location tiers in this game. Theres locations that are tier 1 through 4 and then the final location, Krylo Castle.\n"
# " Where the leader of the zoli civilisation, Yohl, is located. You will have to defeat him to win the game. Each location tier has 4 locations to choose from\n"
# " and you will have to choose one of them to travel to. You will be able to travel back and forth between locations in the same tier but you will not be able\n" 
# " to go back to a previous tier once you have moved on.")
print("\nYou will go through 4 different locations on this journey. The final location, Krylo Castle, is where the leader of the Zoli civilisation,\n"
      "Yohl, is located. You will have to defeat him to win the game. Your job is to work your way through each location growing more powerful to reach and defeatthe final boss.\n"
      "Please note that you are able to travel to krylo castle at any time but it is highly advised that you travel to other locations first to level up and gain experience before\n"
      "facing the final boss.")

#first location selection
print("\nyou will first need to decide the first location you will travel to.")
print(("\nthese are your options for the first location:"))
print(first_location)
valid_locations = [location.lower() for location in first_location] + ["the wastelands"]

while True:
    first_location_choice = prompt_choice(
        "\nby entering the name of a location you will be given details about the location and you will be able to choose whether to go there or not: ",
        valid_locations,
        "Invalid location. Please choose one from the list."
    )

    if first_location_choice.lower() == "the lowlands":
        print("\n\nThe lowlands are a large area of flat land with many low level enemies. The area is home to many survivors and there are many quests to complete here.\n")
    elif first_location_choice.lower() == "ronderdale":
        print("\n\nRonderdale is a small town on the west edge of the krylo kingdom. There are many low level enemies and easier quests to complete there.\n"
        " The people of the town are really suffering from the attack and could use your help taking down some already wounded enemies and rebuilding their town.\n"
        " Going to Ronderdale will give you the opportunity to upgrade your items, battle skills and stats without taking the risk of losing lives early on.")
    elif first_location_choice.lower() == "the wastelands":
        print("\n\nThe wastelands were the first area to be attacked by the Zoli civilisation. The area is now a barren wasteland with very few enemies and no survivors. There are no quests to complete here,\n"
              "however there may be hidden treasures to discover.")
    elif first_location_choice.lower() == "the dark forest":
        print("\n\nThe dark forest is a dense and dangerous area filled with mid level enemies. The forest is home to many powerful beasts and the Zoli civilisation has set up strongholds here.\n"
              "Due to this there aren't really any survivors in the area and the quests are more difficult than in Ronderdale. However, there is lots of experience to be gained from battling higher tier enemies.")
    elif first_location_choice.lower() == "krylo castle":
        print("\n\nThis is were the leader of the Zoli civilisation, Yohl, is located. This is the final location and the most difficult to reach. You will have to defeat Yohl to win the game."
              "This location will be an option in every list but it is highly advised that you travel to others and get leveled up first.\n")

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
    knight.agility += 4
elif weapon_set == "3":
    knight.attack_power += 5
    knight.defense -= 1
    knight.agility += 1

#deciding whether to battle or flee from enemies in the new location
#(was comparing a string to a tuple which is always True, so the other branches never ran)
if first_location_choice.lower() not in ("the wastelands", "krylo castle"):
    print("\nwhen entering certain new locations you cannot do any other actions until you have slain the nearby enemies.")
elif first_location_choice.lower() == "the wastelands":
    print("\nThe wastelands is sparse for enemies. look for survivors and tressure or proceed to the next area.")
elif first_location_choice.lower() == "krylo castle":
    print("\nKrylo castle is the final location and the most difficult to reach. You will have to defeat Yohl to win the game.")
    yohl_encounter(knight, first_location_choice)

#the arrival fight is skipped if the player started at krylo castle as they already faced (or fled from) yohl
#the player is only "in" a location once its nearby enemies are beaten, that decides who they can talk to
cleared_locations = set()
current_location = None
if first_location_choice.lower() != "krylo castle":
    if arrival_encounter(knight, first_location_choice):
        current_location = first_location_choice.lower()
        cleared_locations.add(current_location)

#turn system

def explore_action(player, state):
    """Explore the area, and maybe find a chest."""
    #each location can only be explored once, the main loop stops offering it afterwards
    state["explored"].add(state["location"])
    explore_outcomes = ["\nYou explore the area and find nothing of interest.", "You explore the area and find a chest."]
    result = random.choice(explore_outcomes)
    print(result)

    if "chest" not in result:
        return

    open_or_leave = prompt_choice(
        "\nType [open] to open the chest or [leave] to leave it alone: ",
        ["open", "leave"],
        "\nInvalid choice. Please type [open] or [leave]."
    )
    if open_or_leave.lower() == "open":
        chest_outcomes = ["\nYou found a health potion!.", "You found a damage potion!.", "You found 5 gold coins!."]
        result = random.choice(chest_outcomes)
        print(result)
        if "5 gold coins" in result.lower():
            player.gold += 5
            print(f"You gained 5 gold coins. Total gold: {player.gold}")
        player.experience += 5
        print(f"\nYou also earned 5 experience points for opening the chest! Total XP: {player.experience}")
        see_stats = prompt_choice(
            "\nwould you like to see your updated stats? type [yes] or [no]: ",
            ["yes", "no"],
            "\nInvalid choice. Please type [yes] or [no]."
        )
        if see_stats.lower() == "yes":
            show_player_stats(player)
        else:
            print("\nYou chose not to view your stats.")
    else:
        print("\nYou leave the chest alone and continue exploring.")


def talk_to_patrick(player, state):
    print("\nYou talk to the villager, patrick. He tells you about the recent attacks by the Zoli civilisation and their leader Yohl.")
    print("He also mentions that there are other survivors in the area who might be able to help you on your journey.")

    if state["patrick_recruited"]:
        print("\nPatrick is already travelling with you.")
        return True

    character_accept = prompt_choice(
        "\nwould you like to [recruit] patrick or [leave] him alone?: ",
        ["recruit", "leave"],
        "Invalid choice. Please type [recruit] or [leave]."
    )
    if character_accept.lower() == "recruit":
        state["patrick_recruited"] = True
        player.party_members += 1
        print("\nYou have recruited a survivor to join your party. They will help you in battles and provide support.")
        player.add_item("Survivor Ally", 1)
        print(f"Your party now has {player.party_members} member(s).")
        return True
    else:
        print("\nYou decide not to recruit the survivor and continue on your journey.")
        return False


def talk_to_john(player, state):
    repair_or_not = prompt_choice(
        "\nYou talk to the blacksmith, John. He tells you about how he can improve one your weapons damage stat if you give him 5 gold coins. Would you like to pay him? type [yes] or [no]: ",
        ["yes", "no"],
        "Invalid choice. Please type [yes] or [no]."
    )
    if repair_or_not.lower() == "yes":
        if player.gold >= 5:
            player.gold -= 5
            if player.class_name.lower() == "archer":
                player.attack_power += 4
                print(f"\nYou paid John 5 gold coins and improved your dagger and bow damage! New attack power: {player.attack_power}")
            else:
                player.attack_power += 2
                print(f"\nYou paid John 5 gold coins and improved your weapon's damage! New attack power: {player.attack_power}")
            return True
        else:
            print("You don't have enough gold coins.")
            return False
    else:
        print("You decide not to pay the blacksmith and continue your journey.")
        return False


#lowlands npcs
def talk_to_mara(player, state):
    heal_or_not = prompt_choice(
        "\nYou talk to the healer, Mara. She tells you she can tend to your wounds and grant you an extra life if you give her 10 gold coins. Would you like to pay her? type [yes] or [no]: ",
        ["yes", "no"],
        "Invalid choice. Please type [yes] or [no]."
    )
    if heal_or_not.lower() == "yes":
        if player.gold >= 10:
            player.gold -= 10
            player.lives += 1
            print(f"\nYou paid Mara 10 gold coins and gained an extra life! Lives remaining: {player.lives}")
            return True
        else:
            print("You don't have enough gold coins.")
            return False
    else:
        print("You decide not to pay the healer and continue your journey.")
        return False


def talk_to_garrick(player, state):
    train_or_not = prompt_choice(
        "\nYou talk to Garrick, an old soldier. He tells you he can train you to hold your guard better for 5 gold coins. Would you like to pay him? type [yes] or [no]: ",
        ["yes", "no"],
        "Invalid choice. Please type [yes] or [no]."
    )
    if train_or_not.lower() == "yes":
        if player.gold >= 5:
            player.gold -= 5
            player.defense += 2
            print(f"\nYou paid Garrick 5 gold coins and he trained you to defend better! New defense: {player.defense}")
            return True
        else:
            print("You don't have enough gold coins.")
            return False
    else:
        print("You decide not to pay the soldier and continue your journey.")
        return False


#dark forest npcs
def talk_to_sylva(player, state):
    food_or_not = prompt_choice(
        "\nYou talk to the hunter, Sylva. She tells you she can teach you how to forage and survive in the forest for 5 gold coins. Would you like to pay her? type [yes] or [no]: ",
        ["yes", "no"],
        "Invalid choice. Please type [yes] or [no]."
    )
    if food_or_not.lower() == "yes":
        if player.gold >= 5:
            player.gold -= 5
            player.max_hp += 5
            player.hp = player.max_hp
            print(f"\nYou paid Sylva 5 gold coins and feel hardier than before! New max HP: {player.max_hp}")
            return True
        else:
            print("You don't have enough gold coins.")
            return False
    else:
        print("You decide not to pay the hunter and continue your journey.")
        return False


def talk_to_bram(player, state):
    print("\nYou talk to the scout, Bram.")
    if state["bram_helped"]:
        print("Bram has nothing more to tell you about the Zoli strongholds.")
        return True

    state["bram_helped"] = True
    print("He tells you where the Zoli have set up their strongholds in the forest and how their patrols move. Knowing this makes you a better fighter.")
    player.experience += 10
    print(f"You earned 10 experience points! Total XP: {player.experience}")
    return True


#wastelands npcs
def talk_to_wren(player, state):
    print("\nYou talk to the hermit, Wren.")
    if state["wren_helped"]:
        print("Wren has already shown you everything she has found out here.")
        return True

    state["wren_helped"] = True
    print("She has lived out here since the attack and points you to a spot where she found something buried in the dust.")
    player.gold += 10
    print(f"You dug up 10 gold coins. Total gold: {player.gold}")
    return True


def talk_to_vex(player, state):
    boots_or_not = prompt_choice(
        "\nYou talk to the wandering trader, Vex. He offers you a pair of lighter boots that will improve your agility for 5 gold coins. Would you like to pay him? type [yes] or [no]: ",
        ["yes", "no"],
        "Invalid choice. Please type [yes] or [no]."
    )
    if boots_or_not.lower() == "yes":
        if player.gold >= 5:
            player.gold -= 5
            player.agility += 2
            print(f"\nYou paid Vex 5 gold coins and bought the boots! New agility: {player.agility}")
            return True
        else:
            print("You don't have enough gold coins.")
            return False
    else:
        print("You decide not to pay the trader and continue your journey.")
        return False


#two npcs per location, krylo castle has none as only yohl is there
location_npcs = {
    "ronderdale": {"patrick": talk_to_patrick, "john": talk_to_john},
    "the lowlands": {"mara": talk_to_mara, "garrick": talk_to_garrick},
    "the dark forest": {"sylva": talk_to_sylva, "bram": talk_to_bram},
    "the wastelands": {"wren": talk_to_wren, "vex": talk_to_vex},
}


def talk_action(player, state):
    """Who you can talk to depends on which location you are in."""
    location = state["location"]
    if location is None:
        print("\nThere is nobody around to talk to, travel to a location and deal with the nearby enemies first.")
        return

    #an npc is only marked as done once their conversation is finished (paid, recruited or got their reward), so the player can come back to them
    finished = state["talked"].setdefault(location, set())
    npcs = {name: talk for name, talk in location_npcs[location].items() if name not in finished}
    npc_names = " or ".join(f"[{name}]" for name in npcs)
    who = prompt_choice(
        f"\nYou look around and see {npc_names}. Type a name to talk to them or type [other] to look for someone else: ",
        list(npcs) + ["other"],
        "Invalid choice. Please type a name from the list or [other]."
    ).lower()

    if who == "other":
        place = "town" if location == "ronderdale" else "area"
        print(f"\nYou look for someone else to talk to, but the rest of the {place} is busy recovering from the attack.")
        return

    if npcs[who](player, state):
        finished.add(who)

second_location_choice = ("\nYou have chosen not to see the locations again, which one would you like to travel to? ")
def travel_action(player, state):
    """Choose to stay in the same tier or move on to the next one."""
    tiers = [first_location]#, second_location, third_location, fourth_location]

    while True:
        #the locations are always shown, there is no option to skip the reminder
        print("\nHere are the locations you can travel to:")
        for tier in tiers:
            print(tier)
        print()
        #the chosen location gets its own variable, the prompt text above can't be reused as it's assigned inside this function
        destination_choice = prompt_choice(
            second_location_choice,
            valid_locations,
            "Invalid location. Please choose one from the list."
        ).lower()

        if destination_choice == "the lowlands":
            print("\n\nThe lowlands are a large area of flat land with many low level enemies. The area is home to many survivors and there are many quests to complete here.\n")
        elif destination_choice == "ronderdale":
            print("\n\nRonderdale is a small town on the west edge of the krylo kingdom. There are many low level enemies and easier quests to complete there.\n"
            " The people of the town are really suffering from the attack and could use your help taking down some already wounded enemies and rebuilding their town.\n"
            " Going to Ronderdale will give you the opportunity to upgrade your items, battle skills and stats without taking the risk of losing lives early on.")
        elif destination_choice == "the wastelands":
            print("\n\nThe wastelands were the first area to be attacked by the Zoli civilisation. The area is now a barren wasteland with very few enemies and no survivors. There are no quests to complete here,\n"
                  "however there may be hidden treasures to discover.")
        elif destination_choice == "the dark forest":
            print("\n\nThe dark forest is a dense and dangerous area filled with mid level enemies. The forest is home to many powerful beasts and the Zoli civilisation has set up strongholds here.\n"
                  "Due to this there aren't really any survivors in the area and the quests are more difficult than in Ronderdale. However, there is lots of experience to be gained from battling higher tier enemies.")
        elif destination_choice == "krylo castle":
            print("\n\nThis is were the leader of the Zoli civilisation, Yohl, is located. This is the final location and the most difficult to reach. You will have to defeat Yohl to win the game."
                  "This location will be an option in every list but it is highly advised that you travel to others and get leveled up first.\n")

        travel_or_back2 = prompt_choice(
            "\ntype [travel] to go to this location or type [back] to go back to the list of locations: ",
            ["travel", "back"],
            "Invalid choice. Please type [travel] or [back]."
        )

        if travel_or_back2.lower() == "travel":
            print()
            break

#traveling to the chosen location (this used to sit outside the function so it ran once at startup)
    print(f"Traveling to {destination_choice}...")
    time.sleep(1)
    print(f"Traveling to {destination_choice}...")
    time.sleep(1)
    print(f"Traveling to {destination_choice}...")
    time.sleep(1)
    print(f"Traveling to {destination_choice}...")
    time.sleep(1)

    #the player only counts as being in a location once its enemies are beaten (krylo castle is only the yohl fight)
    state["location"] = None
    if destination_choice == "krylo castle":
        yohl_encounter(player, destination_choice)
    elif destination_choice in state["cleared"]:
        state["location"] = destination_choice
    elif arrival_encounter(player, destination_choice):
        state["location"] = destination_choice
        state["cleared"].add(destination_choice)


#experience points can be spent on stats from the status screen, 5 experience points per point
XP_PER_STAT_POINT = 5

def status_action(player, state):
    show_player_stats(player)

    while True:
        if player.experience < XP_PER_STAT_POINT:
            print(f"\nYou need at least {XP_PER_STAT_POINT} experience points to improve a stat.")
            return

        stat_choice = prompt_choice(
            f"\nYou have {player.experience} experience points. Each stat point costs {XP_PER_STAT_POINT} experience points.\n"
            "Type [strength], [defense], [agility] or [hp] (+5 max HP) to improve it, or [done] to leave: ",
            ["strength", "defense", "agility", "hp", "done"],
            "Invalid choice. Please type strength, defense, agility, hp or done."
        ).lower()

        if stat_choice == "done":
            return

        player.experience -= XP_PER_STAT_POINT
        if stat_choice == "strength":
            player.attack_power += 1
        elif stat_choice == "defense":
            player.defense += 1
        elif stat_choice == "agility":
            player.agility += 1
        elif stat_choice == "hp":
            player.max_hp += 5
            player.hp = player.max_hp

        print(f"\nYou spent {XP_PER_STAT_POINT} experience points to improve your {stat_choice}!")
        show_player_stats(player)


# the game loop: the player picks what to do each turn until the game ends
game_state = {"tier": 1, "patrick_recruited": False, "location": current_location, "cleared": cleared_locations, "bram_helped": False, "wren_helped": False,
              "explored": set(), "talked": {}}

actions = {
    "explore": explore_action,
    "talk": talk_action,
    "travel": travel_action,
    "status": status_action,
}


def available_actions(state):
    """Explore and talk are removed once they're used up in the current location, travel and status are always available."""
    location = state["location"]
    options = []
    if location is not None:
        if location not in state["explored"]:
            options.append("explore")
        if len(state["talked"].get(location, set())) < len(location_npcs[location]):
            options.append("talk")
    options += ["travel", "status"]
    return options


#the full explanation is only shown once, after that the prompt just lists the actions that are left
print("\nYou have a few options of what you can do from here.\nYou can [explore] the area, type [talk]"
      " to other characters and find out more about them and your enemies, type [travel] to another location, or type [status]\n"
      " to check your condition and use experience points.\n"
      "Once you have explored a location or talked to everyone in it, those options are no longer offered there.")

while True:
    options = available_actions(game_state)
    option_text = " ".join(f"[{option}]" for option in options)
    where = f" in {game_state['location'].title()}" if game_state["location"] is not None else ""

    player_next_action = prompt_choice(
        f"\nWhat would you like to do{where}? {option_text}: ",
        actions,
        f"Invalid choice. Please type {', '.join(options[:-1])} or {options[-1]}."
    ).lower()

    #an action that has been used up (or isn't possible yet) just explains why instead of running
    if player_next_action not in options:
        if game_state["location"] is None:
            print("\nYou can't do that yet, travel to a location and deal with the nearby enemies first.")
        elif player_next_action == "talk":
            place = "town" if game_state["location"] == "ronderdale" else "area"
            print(f"\nYou have already talked to everyone you can, the rest of the {place} is busy recovering from the attack.")
        else:
            print("\nYou have already explored this area.")
        continue

    actions[player_next_action](knight, game_state)
