#script d'execution des IA

import hanabi
import hanabi.ai
import hanabi.ai_recommandation_strategy as rec

##IA cheater seule

game = hanabi.Game(5) #5 players
#ai_cheater = hanabi.ai.Cheater()
#game.turn() #input laissé à utilisateur

##IA Random == child seule

#ai_random = hanabi.ai.Random()

##IA avec stratégie de recommandation seule

#ai_recom = rec.Recom_Strategist()
#ai_recom.game = game
#game.ai = ai_recom
#game.turn(ai_recom) #input laissé à l'IA

## IA Human seule

ai_human = hanabi.ai.Human()
game.ai = ai_human
ai_human.game = game
game.run() #jeu entier joué par l'IA


##IA avec stratégie d'information seule