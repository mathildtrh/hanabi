import hanabi
import hanabi.ai
import compare_ai as c
import hanabi.ai_recom

ai1 = hanabi.ai_recom.Recom_Strategist()
ai2 = hanabi.ai.Random()

a,b = c.compare([ai1, ai2], 1000)
c.affichage_alone(b[0], a[0], "AI named Recom")
c.affichage_alone(b[1], a[1], "AI named Random")
c.affichage_general(b,a)
