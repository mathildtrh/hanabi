# ce petit bout de code est fait pour comparer les performances de 2 ou plusieurs IA

# on cherche a connaitre :
#score maxi 
#score mini
#score moyen
#frequence du score parfait
#frequence de defaite
#raisons des defaites

# si on veut enlever les affichages des jeux pendant cette execution il faut redefinir print dans deck.py
#def print(*args, **kwargs):
#    pass

import hanabi
import hanabi.ai

# attention il faut bien importer toutes les IA qu on veut comparer si elles sont dans des fichiers differents

def compare (list_of_ai):
    
    stats = [[0, 25, 0, 0, 0]*len(list_of_ai)] #max_score, min_score, moy_score, freq_25, freq_defeat
    
    for ai in list_of_ai:
        i = 0
        for j in range (1000):
            print("Game numero", j, " avec IA numero",i)
            game = hanabi.Game(2)  # 2 players
            game.ai = hanabi.ai.Cheater(game)
            ai.game = game
            game.run()
            
            if game.score > stats[i][0]:
                stats [i][0] = game.score
            if game.score < stats[i][1]:
                stats [i][1] = game.score
            stats [i][2] += game.score/1000.0
            if game.score == 25:
                stats [i][3] += 1
            if game.score == 0:
                stats [i][4] += 1
        i += 1
    
    return (stats)

