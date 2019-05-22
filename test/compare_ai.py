# ce petit bout de code est fait pour comparer les performances de 2 ou plusieurs IA

# on cherche a connaitre :
#score maxi
#score mini
#score moyen
#frequence du score parfait
#frequence de defaite
#raisons des defaites

#on cherche à tracer l'histogramme des réussites

# si on veut enlever les affichages des jeux pendant cette execution il faut redefinir print dans deck.py
#def print(*args, **kwargs):
#    pass

import numpy as np
import matplotlib.pyplot as plt

# attention il faut bien importer toutes les IA qu on veut comparer si elles sont dans des fichiers differents

def compare (list_of_ai, N):
    
    """
    compare a pour but d'executer un game de hanabi pour chaque IA demandée
    retourne les statistiques de base pour chaque IA : score maxi; score mini, score moyen; la fréquence du score maxi et la fréquence des défaites
    A AJOUTER : pour chaque défaite, elle enregistre les raisons de la défaite
    """
    
    stats = [[0, 25, 0, 0, 0]]*len(list_of_ai) #max_score, min_score, moy_score, freq_25, freq_defeat

    list_of_scores = [[]]*len(list_of_ai) #liste de len(list_of_ai) listes de N scores
    
    i = 0
    for ai in list_of_ai:
        for j in range (N):
            # print("Game numero", j, " avec IA numero",i)
            game = hanabi.Game(2)  # 2 players
            game.ai = hanabi.ai.Cheater(game)
            ai.game = game
            game.run()

            list_of_scores[i].append(game.score)

            if game.score > stats[i][0]:
                stats [i][0] = game.score
            if game.score < stats[i][1]:
                stats [i][1] = game.score
            stats [i][2] += game.score
            if game.score == 25:
                stats [i][3] += 1
            if game.score == 0:
                stats [i][4] += 1
        stats[i][i] = stats[i][2]/N
        i += 1
        
    return (stats, list_of_scores)
    
def affichage_alone (scores, stat, ai): #stat = liste de longueur 5
    
    """
    affichage_alone a pour but de visualiser les statistiques d'une IA seulement
    l'histogramme résume tous les scores
    A AJOUTER : symboliser les valeurs intéressantes pour une IA, ie liste stats renvoyée par compare
    """
    
    titre = "Répartition des scores pour: " + ai
    plt.figure()
    n, bins, patches = plt.hist(scores, 26, alpha=0.5)
    plt.axvline(x=stat[2], color = 'red', label = "Score moyen")
    plt.plot([0,25],[stat[3], stat[3]], color = 'yellow', label = "Nombre de jeux parfaits")
    plt.plot([0,25],[stat[4], stat[4]], color = 'black', label = "Nombre de défaites")
    plt.xlabel('Score')
    plt.ylabel('Pourcentage')
    plt.title(titre)
    plt.axis([-1, 26, 0, 1000])
    plt.grid(True)

    plt.legend()
    plt.show()

def affichage_general (list_of_scores, stats):
    
    """
    affichage_alone a pour but de visualiser les statistiques d'une IA seulement
    l'histogramme résume tous les scores
    A AJOUTER : symboliser les valeurs intéressantes pour une IA, ie liste stats renvoyée par compare
    """

    couleurs = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    plt.figure()
    n, bins, patches = plt.hist(list_of_scores, 25, alpha=0.5)
    for i in range(len(stats)):
        plt.axvline(x=stats[i][2], label = "Score moyen", color = couleurs[i])
    plt.xlabel('Score')
    plt.ylabel('Pourcentage')
    plt.title("Histogramme Comparatif")
    plt.axis([0, 25, 0, 1000])
    plt.grid(True)

    plt.show()

## main script

#a, b = compare([1,2,3], 1000)
# affichage_alone(b[0], a[0], "AI named Alan")
# print("okay for Alan")
# affichage_alone(b[1], a[1], "AI named Betty")
# print("okay for Betty")
#affichage_general(b,a)
#print("okay for comparison")
