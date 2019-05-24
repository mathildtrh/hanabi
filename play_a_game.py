import hanabi
import hanabi.ai
import hanabi.ai_recom

#nom_de_IA = 'Random' #Use Random strat in ai.py file"
nom_de_IA = 'Recom' #Use Recom strat in ai_recom.py file"

nb_players = 4 #à modifier

if nom_de_IA == 'Random' :
    game = hanabi.Game(nb_players)
    ai = hanabi.ai.Random(game)
    game.ai = ai
    game.run()

if nom_de_IA == 'Recom' :
    game = hanabi.Game(nb_players)
    ai = hanabi.ai_recom.Recom_Strategist_2(game)
    game.ai = ai
    game.run()

