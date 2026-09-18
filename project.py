# opening title
title_card = r"""
Welcome To:
  _  __           _             _______ _            _               _     _  __                  _                 
 | |/ /          | |        _  |__   __| |          | |             | |   | |/ (_)               | |                
 | ' / _ __ _   _| | ___   (_)    | |  | |__   ___  | |     ___  ___| |_  | ' / _ _ __   __ _  __| | ___  _ __ ___  
 |  < | '__| | | | |/ _ \         | |  | '_ \ / _ \ | |    / _ \/ __| __| |  < | | '_ \ / _` |/ _` |/ _ \| '_ ` _ \ 
 | . \| |  | |_| | | (_) |        | |  | | | |  __/ | |___| (_) \__ \ |_  | . \| | | | | (_| | (_| | (_) | | | | | |
 |_\|\_\|   \__, |_|\___/  (_)    |_|  |_| |_|\___| |______\___/|___/\__| |_|\_\_|_| |_|\__, |\__,_|\___/|_| |_| |_|
             __/ |                                                                       __/ |                      
            |___/                                                                       |___/                                                                                                                                                                                            
"""

print(title_card)

enter = input("input 1 to continue. input 2 to exit: ")

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
