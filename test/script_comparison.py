import hanabi
import hanabi.ai
import compare_ai as c

ai1 = hanabi.ai.Cheater()
ai2 = hanabi.ai.Random()

a,b = c.compare([ai1, ai2], 1000)
c.affichage_alone(b[0], a[0], "AI named Cheater")
c.affichage_alone(b[1], a[1], "AI named Random")
c.affichage_general(b,a)
