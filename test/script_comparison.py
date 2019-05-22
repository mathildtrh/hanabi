import hanabi
import hanabi.ai
import hanabi.ai_recommandation_strategy as rec
import compare_ai as c

ai1 = hanabi.ai.Cheater()
ai2 = hanabi.ai.Random()
ai3 = rec.Recom_Strategist()

a,b = c.compare([ai1, ai2, ai3], 10000)
c.affichage_alone(b[0], a[0], "AI named Cheater")
c.affichage_alone(b[1], a[1], "AI named Random")
c.affichage_alone(b[2], a[2], "AI that plays with a recommandation strategy")
c.affichage_general(b,a)
