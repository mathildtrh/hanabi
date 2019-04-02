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
