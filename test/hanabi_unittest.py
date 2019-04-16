import unittest
import hanabi
import random



class ColorTest(unittest.TestCase):
    def test_1(self):
        pass


class CardTest(unittest.TestCase):
    def test_1(self):
        pass


class HandTest(unittest.TestCase):
    # test __special__ functions
    

    # test normal functions
    pass

class DeckTest(unittest.TestCase):
    # test __special__ functions
    

    # test normal functions
    pass



class GameTest(unittest.TestCase):

    def setUp(self):
        self.unshuffled_game = hanabi.Game()
        self.random_game = hanabi.Game()
        # ... group G here! 
        self.predefined_game = hanabi.Game()
        # ...

    def test_init(self):

        game=hanabi.Game(3)
        self.assertEqual(len(game.hands),3)
        for i in range (3):
            self.assertEqual(len(game.hands[i]), 5)
        n_player = random.randint(2, 5)
        # print(n_player)
        # start a game
        game = hanabi.Game(n_player) # bug in Game __init__
        self.assertNotEqual(game.deck.cards, None)
        self.assertEqual(len(game.hands), n_player)
        # self.assertEqual(game.players, ("Alice", "Benji"))
        for hand in game.hands: # bug in hands __init__
            # print(len(hand.cards))
            # print(game.deck.cards_by_player[n_player])
            self.assertEqual(len(game.discard_pile), 0)
            self.assertEqual(len(hand.cards), game.deck.cards_by_player[n_player])

    def test_predifined(self):
        # bug in game.turn() close the file!
        self.predefined_game.load("game1.py")
        self.assertEqual(self.predefined_game.players, ('Alice', 'Benji'))
        self.assertEqual(len(self.predefined_game.deck.cards), 35)

        self.predefined_game.load("unittest_game_1.py")
        self.assertEqual(self.predefined_game.players, ('Alice', 'Benji'))
        self.assertEqual(len(self.predefined_game.deck.cards), 39)

        # self.predefined_game.load("game2.py")
        # self.assertEqual(self.predifined_game.cards, game1.cards[5:])

        #start a game _ essai de Camille
        #game=hanabi.Game(2)
        #self.assertEqual(len(game.hands),2)
        #game=hanabi.Game(3)
        #self.assertEqual(len(game.hands),3)
        #for i in range (3):
        #    self.assertEqual(len(game.hands[i],5))
        #self.assertEqual(len(game.discard_pile), 0)
        #game=hanabi.Game(4)
        #for i in range (4):
        #    self.assertEqual(len(game.hands[i],4))

    # lines 193, 227
    def test_A1(self):
        pass

    # lines 227, 261
    def test_B1(self):
        pass


    # lines 261, 295


    # lines 295, 329


    # lines 329, 363


    # lines 363, 397


    # lines 397, 431


    pass



if __name__ == '__main__':
    unittest.main()
