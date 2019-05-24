import hanabi
import hanabi.ai
import hanabi.ai_recommandation_strategy as rec1
import hanabi.ai_recom as rec2
import compare_ai as c
import hanabi.ai_recom

""" Avez-vous pensez à décommenter def print dans les fichiers ai.py, ai_recom.py and deck.py ?
"""
ai1 = rec2.Recom_Strategist_2()
ai2 = hanabi.ai.Random()
ai3 = hanabi.ai.Cheater()

nb_players = 5 #à modifier
nb_parties = 1000 #idem si jamais

a,b = c.compare([ai1, ai2, ai3], nb_parties, nb_players)
c.affichage_alone(b[0], a[0], "AI named Recom")
c.affichage_alone(b[1], a[1], "AI named Random")
c.affichage_alone(b[2], a[2], "AI named Cheater")
c.affichage_general(b,a)
