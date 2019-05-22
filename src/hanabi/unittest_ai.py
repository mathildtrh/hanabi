""" unittest for Cheater and Random """

import unittest
import hanabi


class RandomTest(unittest.TestCase) :
    """ Test de l'IA Random : basically test if Random play by the rules. 
    Rappel de la stratégie : 
    Algorithm : 
        * if 0 < blue_coins <= 8 pick randomly between play, discard or clue.
            * if play is chosen, pick randomly between the unclued cards and other cards that won't make the game fail (ie : +1 red_coin)
            * if clue is chosen, give clue on a random card among the ones unclued.
            * if discard is chosen, discard any card in hand
        * if blue_coins == 0 pick randomly between play or discard."""
    
    def test_predefined(self):
        
        #teste si l'ia ne joue pas quand il y a 8 jetons bleus
        game = hanabi.Game(4)
        game.blue_coins = 8
        ai = hanabi.ai.Random(game)
        play = ai.play()
        self.assertNotEqual(play[0],'p')

        #teste si l'ia ne donne pas d'indice quand il y a zéro jeton bleu
        game = hanabi.Game(4)
        game.blue_coins = 0
        ai = hanabi.ai.Random(game)
        play = ai.play()
        self.assertNotEqual(play[0],'c')

        #teste si l'ia ne donne pas d'indice sur une carte dont on connaît déjà quelque chose
        game = hanabi.Game(3)
        for hand in game.hands :
            for card in hand.cards :
                card.color_clue = True
                card.number_clue = True
        ai = hanabi.ai.Random(game)
        play = ai.play()
        self.assertNotEqual(play[0],'c')

        #teste si l'ia ne joue pas alors qu'elle peut faire échouer la partie
        game = hanabi.Game(3)
        for card in game.current_hand.cards :
            card.number = 3
        game.red_coins = 2
        ai = hanabi.ai.Random(game)
        play = ai.play()
        self.assertNotEqual(play[0],'p')






        

    