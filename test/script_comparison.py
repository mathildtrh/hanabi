import hanabi
import hanabi.ai
import hanabi.ai_recommandation_strategy as rec1
import hanabi.ai_recom as rec2
import compare_ai as c
import hanabi.ai_recom

ai1 = rec2.Recom_Strategist_2()
ai2 = hanabi.ai.Random()
ai3 = hanabi.ai.Cheater()

nb_players = 5 #à modifier

a,b = c.compare([ai1, ai2, ai3], 1000)
c.affichage_alone(b[0], a[0], "AI named Recom")
c.affichage_alone(b[1], a[1], "AI named Random")
c.affichage_alone(b[1], a[1], "AI named Cheater")
c.affichage_general(b,a)
