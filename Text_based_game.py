import time
import random

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

#start of game
with open("title_card.txt", "r") as file:
    content = file.read().splitlines()
    for line in content:
        print(line)

enter = safe_input("press [S]tart. press [E]xit, you can also press [ESC] to exit the game at any time: ")

if enter.lower() == "s":
    print("\nplease ensure to have your terminal window is enlarged for the best playing experience.")
    time.sleep(3)
    # opening message
    print(
        " \nHello player. In this game you will be playing a royal knight of the"
        " kingdom Krylo, the kingdom has been overrun with\nevil ancient beasts"
        " cast upon it by the rival civilisation The Zoli led by their leader Yohl."
        " \nIt is your job to extinguish the land of these monsters and re-gain control of the casle"
        " All your fellow knights fell in battle\ntrying to keep the"
        " enemy out of the town walls so it is up to you and you alone to"
        " regain control of the kingdom. You may find other survivors"
        " along\nthe way and you must decide whether what they bring to the"
        " party outweighs what they cost you. Be careful, there's a reason all"
        " that came before you\nfell to these beasts. They are not to be"
        " trifled with."
    )
elif enter.lower() == "e":
    print("You chose to exit.")
    sys.exit(0)
else:
    print("Invalid choice. Exiting.")
    sys.exit(0)

#character creation
player_exp = 0
print("\n   -   Before you begin your journey, you must first create your character.")
    #character name input
character_name = safe_input("\nWhat is your name, brave knight?: ")
print(f"\nWhat an amazing choice, {character_name} is such a heroic name!")

#character health input
while True:
    try:
        character_lives = int(safe_input("\nNow it's time to choose the amount of lives you want. The default is 3, going higher than 3 would make\nthe game more forgiving and going below will make it more of a challenge. what will you choose?: "))
        break
    except ValueError:
        print("Invalid input. Please enter a valid number.")

#response to character health input
if character_lives > 3:
    print("\nYou have chosen to have more than the default amount of lives; it would be a bit embarrassing if you fail! Good luck!")
elif character_lives < 3:
    print("\nYou have chosen to have less than the default amount of lives; this is going to be a challenge. Good luck!")
else:
    print("\nYou chose the default amount of lives. A repectable choice.")

#weapon set selection
print("\n\n - next we must determine your starting weapon.\n - You can choose from a sword and shield, a bow and sword, or a spear and shield. Each weapon set has its own strengths and weaknesses, so choose wisely.")
    #weapon set input
weapon_set = safe_input("\nWhat weapon set do you choose? (press [1] for sword and shield, [2] for spear and shield, [3] for bow and sword): ")

if weapon_set == "1":
  with open("sword_shield_char.txt", "r") as file:
    content = file.read().splitlines()
    for line in content:
        print(line)
    print("\n\nYou have chosen the sword and shield. A classic choice, good for both offense and defense.")

elif weapon_set == "2":
    with open("spear_shield_char.txt", "r") as file:
        content = file.read().splitlines()
        for line in content:
            print(line)
    print("\nYou have chosen the spear and shield. A safe choice, good for defense and thrusting attacks to keep enemies at a safe distance.")
elif weapon_set == "3":
    with open("bow_sword_char.txt", "r") as file:
            content = file.read().splitlines()
            for line in content:
                print(line)
    print("\nYou have chosen the bow and sword. A versatile choice, good for ranged and melee combat but bad for defense.")
else:
    print("\nInvalid choice. Exiting game.")
    sys.exit(0)

#location lists
First_location = ["the lowlands", "ronderdale", "the dark forest", "kyrlo castle"]
Second_location = ["the midlands", "clonsel", "hebra village", "kyrlo castle"]
Third_location = [ "the highlands", "the cursed swamp", "the dragon's lair", "kyrlo castle"]
Fourth_location = ["the frosty peaks", "valcano pass", "the great temple", "kyrlo castle"]
Final_battle = ["krylo castle"]

#battle system
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

    def take_damage(self, raw_damage: int):
        """Calculates mitigated damage and reduces health points."""
        mitigation = self.defense if not self.is_defending else self.defense * 2
        final_damage = max(1, raw_damage - mitigation)
        self.hp = max(0, self.hp - final_damage)
        print(f"{self.name} takes {final_damage} damage! (HP: {self.hp}/{self.max_hp})")

    def attack(self, target: 'Character'):
        """Deals randomized damage to a target based on base attack power."""
        print(f"{self.name} attacks {target.name}!")
        variance = random.randint(-2, 4)
        raw_damage = self.attack_power + variance

        if random.random() < 0.10:
            raw_damage = int(raw_damage * 1.5)
            print("CRITICAL HIT!")

        target.take_damage(raw_damage)

    def reset_status(self):
        """Resets temporary defensive states at the start of a turn."""
        self.is_defending = False


class Player(Character):
    """Player subclass with life tracking, experience, and inventory items."""
    def __init__(self, name: str, max_hp: int, attack_power: int, defense: int):
        super().__init__(name, max_hp, attack_power, defense)
        self.lives = 1
        self.experience = 0
        self.inventory = {}

    def add_item(self, item_name, quantity=1):
        """Add a found item to the player's inventory."""
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity
        print(f"{self.name} picked up {quantity} {item_name}.")

    def view_inventory(self):
        """Shows the player's inventory without spending a turn."""
        if not self.inventory:
            print("Your inventory is empty.")
            return

        print("\nInventory:")
        for item, count in self.inventory.items():
            if count > 0:
                print(f"- {item} x{count}")

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

    def lose_life(self):
        """When HP reaches 0, lose one life and restore the full HP bar."""
        if self.lives > 0:
            self.lives -= 1
            self.hp = self.max_hp
            print(f"{self.name} lost a life! Remaining lives: {self.lives}")
            if self.lives <= 0:
                self.hp = 0
                print(f"{self.name} has no lives left. Game over.")


class Enemy(Character):
    """Enemy subclass with basic automated AI."""
    def take_turn(self, target: Character):
        """Simple AI: Defends if low on health, otherwise attacks."""
        if self.hp < (self.max_hp * 0.25) and random.random() < 0.5:
            self.is_defending = True
            print(f"{self.name} takes a defensive stance!")
        else:
            self.attack(target)


def battle_loop(player: Player, enemy: Enemy):
    """Manages the loop of the turn-based system."""
    print(f"\nA wild {enemy.name} appeared! Battle begins!\n")
    turn_counter = 1

    while player.is_alive() and enemy.is_alive():
        print(f"\n=== TURN {turn_counter} ===")
        print(f"{player.name}: {player.hp}/{player.max_hp} HP | {enemy.name}: {enemy.hp}/{enemy.max_hp} HP")
        print("-" * 30)

        player.reset_status()
        print("Choose your action:")
        print("1. Attack")
        print("2. Defend")
        print("3. Inventory")

        choice = safe_input("Enter choice (1-3): ").strip()
        print()

        inventory_used = False

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
            print(f"\n{enemy.name} has been defeated! {player.name} wins!")
            print(f"{player.name} gains 10 experience points! Total XP: {player.experience}")
            return "win"

        if not player.is_alive():
            if player.lives > 0:
                player.lose_life()
                print(f"{player.name} is back at full HP and the battle is over.")
                print(f"{enemy.name} wins this round.")
                return "loss"
            else:
                print(f"\n{player.name} has fallen in battle. Game Over.")
                return "loss"

        time.sleep(1)

        enemy.reset_status()
        print(f"\n--- {enemy.name}'s Turn ---")
        enemy.take_turn(player)

        if not player.is_alive():
            if player.lives > 0:
                player.lose_life()
                print(f"{player.name} is back at full HP and the battle ends here.")
                print(f"{enemy.name} wins this round.")
                return "loss"
            else:
                print(f"\n{player.name} has fallen in battle. Game Over.")
                return "loss"

        turn_counter += 1
        time.sleep(1)

    if enemy.hp <= 0 and player.hp > 0:
        return "win"
    if player.hp <= 0:
        return "loss"
    return "loss"


#starting gameplay
print("\nNow that you have your character, it's time to begin your journey. Good luck, brave knight!")

#location selection mechanic explanation
print("\nYou will go through 5 different location tiers in this game. Theres locations that are tier 1 through 4 and then the final location, Krylo Castle. Where the leader of the ")

#first location selection
print("\nyou will first need to decide the first location you will travel to.")
print(("\nthese are your options for the first location:"))
print(First_location)
first_location_choice = safe_input("\nby entering the name of a location you will be given details about the location and you will be able to choose whether to go there or not: ")


if first_location_choice == "the lowlands":
    print()
    travel_or_back1 = safe_input("\ntype [travel] to go to this location or type [back] to go back to the list of locations: ")
elif first_location_choice == "ronderdale":
    print("\n\nRonderdale is a small town on the west edge of the krylo kingdom. There are many low level enemies and easier quests to complete there.\nThe people of the town are really suffering from the attack and could use your help taking down some already wounded enemies and rebuilding their town.\ngoing to Ronderdale will give oportunity to upgrade your items, battle skills and stats without taking the risk of losing lives early on.")
    travel_or_back1 = safe_input("\ntype [travel] to go to this location or type [back] to go back to the list of locations: ")
elif first_location_choice == "the wastelands":
    print()
    travel_or_back1 = safe_input("\ntype [travel] to go to this location or type [back] to go back to the list of locations: ")
elif first_location_choice == "the dark forest":
    print()   
    travel_or_back1 = safe_input("\ntype [travel] to go to this location or type [back] to go back to the list of locations: ")
elif first_location_choice == "kyrlo castle":
    print()
    travel_or_back1 = safe_input("\ntype [travel] to go to this location or type [back] to go back to the list of locations: ")
else:
    safe_input("Invalid choice. please enter a valid location from the list.")
    
if travel_or_back1 == "back":
    print()
    print(First_location)
    first_location_choice = safe_input("by entering the name of a location you will be given details about the location and you will be able to choose whether to go there or not: ")
else:
    safe_input("Invalid choice. please enter a valid location from the list.")

if travel_or_back1 == "travel":
    print(f"Traveling to {first_location_choice}...")
    time.sleep(1)
    print(f"Traveling to {first_location_choice}...")
    time.sleep(1)
    print(f"Traveling to {first_location_choice}...")
    time.sleep(1)
    print(f"Traveling to {first_location_choice}...")
    time.sleep(1)

    print("\nwhen entering a new location you cannot do any other actions until you have slain the nearby enemies.")

    welcome_message = safe_input(f"\nYou have arrived at {first_location_choice}, would you like to either [flee] or [battle] nearby enemies?: ")
    battle_message1 = ("your first battle is with a chulu, a chimp looking creature with medium health but low damage output")
    
    print(welcome_message)
    if welcome_message == "flee":
        print("\nyou have fled Ronderdale, you can now choose where you would like to go from here")
        print(First_location)
        first_location_choice = safe_input("\nby entering the name of a location you will be given details about the location and you will be able to choose whether to go there or not: ")
        
    elif welcome_message == "battle":
        with open("chulu.txt", "r") as file:
                    content = file.read().splitlines()
                    for line in content:
                        print(line)
        print(f"\n\n{battle_message1}")

    else:
        safe_input("Invalid choice. please enter a valid location from the list.")

        knight = Player(
            name=character_name,
            max_hp=50,
            attack_power=12,
            defense=3,
        )
        knight.lives = character_lives

        if weapon_set == "1":
            knight.attack_power += 4
            knight.defense += 3
        elif weapon_set == "2":
            knight.attack_power += 3
            knight.defense += 4
        elif weapon_set == "3":
            knight.attack_power += 5
            knight.defense -= 1

        villain = Enemy(name="Chulu", max_hp=30, attack_power=random.randint(5, 9), defense=1)
        battle_result = battle_loop(knight, villain)

        if battle_result == "win":
            print("\nThe Chulu has been defeated. The close area is now safe.")
            print(f"\nYou earned 10 experience points for defeating the Chulu! Total XP: {knight.experience}")
            print("\nNow that you have defeated the Chulu, you can continue your journey.")
        else:
            print("\nThe Chulu defeats you and the battle ends.")
            print(f"{knight.name} loses a life and returns to full health.")
            print("\nYou can try again from the start of this encounter.")

        player_next_action1 = safe_input("\nYou have a few options of what you can do from here\nYou can [explore] the area, [search] for items, [talk] to other characters and get quests, [travel] to another location, [status] to check your condition and use experience points:\n")
