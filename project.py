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
