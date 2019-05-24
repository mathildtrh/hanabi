import hanabi
import hanabi.ai
import hanabi.ai_recom


nom_de_IA = input("quelle IA voulez-vous tester ? [Random/Recom] :")
nb_players = int(input("combien de joueurs ? [2/3/4/5]:"))
mode = input("lancer toute la partie [R] ou jouer tour par tour [T] ? :")

while nom_de_IA not in ['Random','Recom'] :
    nom_de_IA = input("quelle IA voulez-vous tester ? [Random/Recom] :")

while nb_players > 5 or nb_players <2 :
    nb_players = input("combien de joueurs ? [2/3/4/5]:")

while mode not in 'RT' :
    mode = input("lancer toute la partie [R] ou jouer tour par tour [T] ? :")

if mode == 'R' : 
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

if mode == 'T' :
    
    if nom_de_IA == 'Random' :
            game = hanabi.Game(nb_players)
            ai = hanabi.ai.Random(game)
            game.ai = ai
    
    if nom_de_IA == 'Recom' :
            game = hanabi.Game(nb_players)
            ai = hanabi.ai_recom.Recom_Strategist_2(game)
            game.ai = ai
    
    Turn = True 
    
    while Turn is True :
        game.turn(ai)
        Turn = input("continuer à jouer [True] ou arrêter et finir la partie [False] ? :")
    
    game.run()

