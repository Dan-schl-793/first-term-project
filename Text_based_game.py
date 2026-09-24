import time
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
print("\n\n    -    next we must determine your starting weapon. You can choose from a sword and shield, a bow and sword, or a spear and shield. Each weapon set has its own strengths and weaknesses, so choose wisely.")
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
First_location = ["the lowlands", "ronderdale", "the wastelands", "the dark forest", "kyrlo castle"]
Second_location = ["the midlands", "clonsel", "hebra village", "the forgotten tavern", "kyrlo castle"]
Third_location = [ "the highlands", "the cursed swamp", "the haunted castle", "the dragon's lair", "kyrlo castle"]
Fourth_location = ["the frosty peaks", "valcano pass", "the great temple", "kyrlo castle"]
Final_battle = ["krylo castle"]


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

if travel_or_back1 == "travel":
    print(f"Traveling to {first_location_choice}...")
    time.sleep(1)
    print(f"Traveling to {first_location_choice}...")
    time.sleep(1)
    print(f"Traveling to {first_location_choice}...")
    time.sleep(1)
    print(f"Traveling to {first_location_choice}...")
    time.sleep(1)

    welcome_message = input(f"\nYou have arrived at {first_location_choice}, would you like to either [flee] or [battle] nearby enemies?: ")
    battle_message1 = ("your first battle is with a chulu, a chimp looking creature with medium health but low dmg output")
    
    print(welcome_message)
    if welcome_message == "flee":
        print("\nyou have fleed Ronderdale, you can now choose where you would like to go from here")
        print(First_location)
        first_location_choice = safe_input("\nby entering the name of a location you will be given details about the location and you will be able to choose whether to go there or not: ")
        
    elif welcome_message == "battle":
        print(battle_message1)
