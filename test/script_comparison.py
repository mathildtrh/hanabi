import hanabi
import hanabi.ai
import hanabi.ai_recommandation_strategy as rec1
import hanabi.ai_recom as rec2
import compare_ai as c
import hanabi.ai_recom

ai1 = hanabi.ai_recom.Recom_Strategist_2()
ai2 = hanabi.ai.Random()
ai3 = hanabi.ai.Cheater()

a,b = c.compare([ai1, ai3], 1000)
c.affichage_alone(b[0], a[0], "AI named Recom")
c.affichage_alone(b[1], a[1], "AI named Cheater")
#c.affichage_alone(b[1], a[1], "AI that plays with a recommandation strategy")
c.affichage_general(b,a)
