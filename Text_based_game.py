
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

enter = input("press [S]tart. press [E]xit, you can also press [ESC] to exit the game at any time: ")

if enter.lower() == "s":
    # opening message
    print(
        "Hello player. In this game you will be playing a royal knight of the"
        " kingdom Krylo, the kingdom has been overrun with evil ancient beasts"
        " and you’re needed to save it.\nIt is your job to extinguish the land"
        " of these monsters and re-gain control of the place you once called"
        " home. All your fellow knights fell in battle\ntrying to keep the"
        " beasts out of the town walls so it is up to you and you alone to"
        " regain control of the kingdom. You may find other survivors"
        " along\nthe way and you must decide whether what they bring to the"
        " party outweighs what they cost you. Be careful, there's a reason all"
        " that came before you fell\nto these beasts. They are not to be"
        " trifled with."
    )
elif enter.lower() == "e":
    print("You chose to exit.")
    sys.exit(0)
else:
    print("Invalid choice. Exiting.")
    sys.exit(0)

#character creation
print("Before you begin your journey, you must first create your character.")
    #character name input
character_name = safe_input("\nWhat is your name, brave knight? ")
print(f"What an amazing choice, {character_name}!")

#character health input
while True:
    try:
        character_lives = int(safe_input("\nNow it's time to choose the amount of lives you want. The default is 3,\nso going higher than 3 would make the game more forgiving and going below will make it more of a challenge. what will you choose?: "))
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
print("\n\nnext we must determine your starting weapon. You can choose from a sword and shield, a bow and sword, or a spear and shield. Each weapon set has its own strengths and weaknesses, so choose wisely.")
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
