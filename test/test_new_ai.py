<<<<<<< HEAD
#attention à bien faire un "make module"

import hanabi
import hanabi.my-new_random_ai as new_ai

game = hanabi.Game(2) #2 players

ai = new_ai.random(game)

ai.play()

#pour jouer juste un tour
game.turn(["conseil"])


#pour jouer toute une partie d'un coup
game.run()
=======

# bien faire un "make module"

import hanabi
import hanabi.ai

import hanabi.my_new_smart_ai as new_ai

game = hanabi.Game(2)  # 2 players

ai = new_ai.random(game)
ai = hanabi.ai.Cheater(game)


ai.play()

# pour jouer juste un tour:
game.turn()      # prompt
game.turn(ai)    # c'est l'ai qui joue
game.turn('c1')  # ou je peux donner une commande
game.turn(['c1', 'c2', 'p2'])  # ... ou toute une serie 

# pour jouer toute une partie
game.ai = ai
game.run()



>>>>>>> ce575cf159cbddcdd9e9d8ecdd848d238959ef26
