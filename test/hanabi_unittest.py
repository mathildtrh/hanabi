import unittest
import hanabi
import random



class ColorTest(unittest.TestCase):
    def test_str(self):
        colors=[(31,"Red"),(32,"Green"),(34,"Blue"),(33,"Yellow"),(37,"White")]
        trouve=True
        for (c,color) in colors:
            a=str(hanabi.deck.Color(c))
            self.assertEqual(a,color)
    def test_valid(self):
        for s in (54,78,46,54,-5,3):
            self.assertRaises(ValueError, hanabi.deck.Color, s)


class CardTest(unittest.TestCase):
    def test_not_equaled_cards(self):
        c1=hanabi.deck.Card('B',4)
        c2=hanabi.deck.Card('R',4)
        self.assertNotEqual(c1,c2)

    def test_equal(self):
        c1=hanabi.deck.Card('R',4)
        string_card="R4"
        self.assertEqual(c1,string_card)

    def test_number(self):
        #self.assertRaises(hanabi.deck.Card('R',7), AssertionError)
        with self.assertRaises(AssertionError):
            hanabi.deck.Card('R',7)

class HandTest(unittest.TestCase):
    # test __special__ functions
    
    def setUp(self):
        self.deck1 = hanabi.deck.Deck()
        self.hand1 = hanabi.deck.Hand(self.deck1)
        self.deck1.shuffle()

        self.deck3 = hanabi.deck.Deck()
        self.hand3 = hanabi.deck.Hand(self.deck3,1)

    def test_basic_hand(self):
        self.assertEqual(self.hand3.__str__(),hanabi.deck.Card(hanabi.deck.Color.Red,1).str_color())

    def test_len(self):
        self.assertEqual(5, len(self.hand1))
    
    def test_shuffle(self):
        self.deck1.shuffle()
        mem = str(self.deck1)[0:len(repr(self.hand1))]
        self.hand2 = hanabi.deck.Hand(self.deck1)
        self.assertEqual(str(self.hand2), mem)


    # test normal functions
    pass

class DeckTest(unittest.TestCase):
    # test __special__ functions
    

    # test normal functions
    def setUp(self):
        pass


    def test_shuffle(self):
        Paquet = hanabi.Deck()
        b=0
        Paquet_aux = hanabi.Deck()
        Paquet_aux.cards = Paquet.cards

        for k in range(10):

            # On test si sur 10 melange le deck est bien different au moins 2 fois

            Paquet_aux.cards = Paquet.cards
            Paquet.shuffle()
            if Paquet!=Paquet_aux:
                b+=1
        self.assertTrue(b>2)

    def test_draw(self):

        # On teste si la carte piochee est la bonne et si le deck a bien ete deleste d'une carte

        Paquet = hanabi.Deck()
        Paquet.shuffle()
        LaCarte = Paquet.cards[0]
        nombre_cartes = len(Paquet.cards)
        LaCarte2 = Paquet.draw()
        self.assertEqual(len(Paquet.cards),nombre_cartes-1)
        self.assertEqual(LaCarte,LaCarte2)


    def test_deal(self):

        #On test si le nombre de carte par main est le bon pour 5, 4 et 3 et si les mains retournees sont de la classe Hand

        Paquet = hanabi.Deck()
        Hands = Paquet.deal(5)
        b = True
        for x in Hands:
            self.assertTrue(isinstance(x,hanabi.deck.Hand))
            if len(x)!=4:
                b = False
        self.assertEqual(b,True)

        Paquet = hanabi.Deck()
        Hands = Paquet.deal(3)
        b = True
        for x in Hands:
            self.assertTrue(isinstance(x,hanabi.deck.Hand))
            if len(x)!=5:
                b = False
        self.assertEqual(b,True)

        Paquet = hanabi.Deck() 
        Hands = Paquet.deal(4)

        b = True
        for x in Hands:
            self.assertTrue(isinstance(x,hanabi.deck.Hand))
            if len(x)!=4:
                b = False
        self.assertEqual(b, True)


class DeckTest2(unittest.TestCase):
    # contributed by I. Abdouli
    # test normal functions
    def test_shuffle(self):
        self.deck_init = hanabi.deck.Deck()
        self.deck_init.shuffle()
        self.deck_init_2=hanabi.deck.Deck()
        self.assertNotEqual(self.deck_init,self.deck_init_2)
        #On verifie qu'on obtient bien un paquet different.
        self.assertEqual(len(self.deck_init.cards),len(self.deck_init_2.cards))
        #On verifie que le nombre de cartes est reste identique.

    def test_draw(self):
        self.deck_init = hanabi.deck.Deck()
        card=self.deck_init.cards[0]
        card2=self.deck_init.draw()
        self.assertEqual(len(self.deck_init.cards),len(hanabi.deck.Deck().cards)-1)
        #On verifie que la carte piochee a bien ete retiree de la pioche.
        self.assertEqual(card,card2)
        #On verifie que la carte piochee est bien celle qui etait en haut du paquet.

    def test_deal(self):
        for nhands in range(2,6):
            self.deck_init=hanabi.deck.Deck()
            self. deck_init.deal(nhands)
            self.assertEqual(len(self.deck_init.cards),len(hanabi.deck.Deck().cards)-nhands*self.deck_init.cards_by_player[nhands])
            #On verifie que le bon nombre de cartes a ete distribue, et que celles-ci ont bien ete retirees de la pioche.
    


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
        game = hanabi.Game(2)
        game.quiet = True
        game.turn('p3')  # check that we can play blindly

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
