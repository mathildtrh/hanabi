# bien faire un "make module"

import hanabi
# import hanabi.ai
import hanabi.ai as aai
import hanabi.ai_stra_info as info
# import hanagabi.my_new_smart_ai as new_ai

game = hanabi.Game(5)  # 5 players
print ("Here are the hands:")
print (game.hands)
ai = info.Stra_info(game)
# ai = all_ai.Cheater(game)
ai.play()
"""
# pour jouer juste un tour:
game.turn()      # prompt
game.turn(ai)    # c'est l'ai qui joue
game.turn('c1')  # ou je peux donner une commande
game.turn(['c1', 'c2', 'p2'])  # ... ou toute une serie 

"""
# pour jouer toute une partie
game.ai = ai

game.run()

