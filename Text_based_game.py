with open('title_card.txt', 'r') as file:
    for line in file:
        print(line.strip())

enter = input("press 1 to continue. press 2 to exit: ")

if enter == "1":
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
else:
  quit()

#character creation
print("Before you begin your journey, you must first create your character.")

character_name = input("\nWhat is your name, brave knight? ")
print(f"What an amazing choice, {character_name}!")

while True:
    try:
        character_lives = int(input("Now it's time to choose the amount of lives you want. The default is 3,\nso going higher than 3 would make the game more forgiving and going below will make it more of a challenge: "))
        break
    except ValueError:
        print("Invalid input. Please enter a valid number.")

if character_lives > 3:
    print("You have chosen to have more than the default amount of lives; it would be a bit embarrassing if you fail! Good luck!")
elif character_lives < 3:
    print("You have chosen to have less than the default amount of lives; this is going to be a challenge. Good luck!")
else:
    print("You chose the default amount of lives. A fair start.")
