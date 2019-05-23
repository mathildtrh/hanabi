"""
Artificial Intelligence to play Hanabi.
"""

import random
import hanabi
import itertools


def print(*args, **kwargs):
    pass

class AI:
    """
    AI base class: some basic functions, game analysis.
    """
    def __init__(self, game=None):
        self.game = game
        self.GAME_CHANGED = False
        self.CLUES = []

    @property
    def other_hands(self):
        "The list of other players' hands."
        return self.game.hands[1:]

    @property
    def other_players_cards(self):
        "All of other players's cards, concatenated in a single list."
        #return sum([x.cards for x in self.other_hands], [])
        return list(itertools.chain.from_iterable([hand.cards for hand in self.other_hands]))


class Cheater(AI):

    """
    This player can see his own cards!

    Algorithm:
      * if 1-or-more card is playable: play the lowest one, then newest one
      * if blue_coin<8 and an unnecessary card present: discard it.
      * if blue_coin>0: give a clue on precious card (so a human can play with a Cheater)
      * if blue_coin<8: discard the largest one, except if it's the last of its kind or in chop position in his opponent.
    """

    def play(self):
        "Return the best cheater action."
        game = self.game
        playable = [ (i+1, card.number) for (i,card) in
                     enumerate(game.current_hand.cards)
                     if game.piles[card.color]+1 == card.number ]

        if playable: #<=> playable n'est pas vide
            # sort by ascending number, then newest
            playable.sort(key=lambda p: (p[1], -p[0]))
            print ('Cheater would play:', "p%d"%playable[0][0], end=' ')
            if (len(playable)>1):
                print('but could also pick:', playable[1:])
            else: print()

            return "p%d"%playable[0][0]


        discardable = [ i+1 for (i,card) in
                        enumerate(game.current_hand.cards)
                        if ( (card.number <= game.piles[card.color])
                             or (game.current_hand.cards.count(card)>1)
                        ) ]
        # discard already played cards, doubles in my hand
        # fixme: discard doubles, if I see it in partner's hand
        # fixme: il me manque les cartes sup d'une pile morte

        if discardable and (game.blue_coins<8):
            print ('Cheater would discard:', "d%d"%discardable[0], discardable)
            return "d%d"%discardable[0]

        ## 2nd type of discard: I have a card, and my partner too

        discardable2 = [ i+1 for (i,card) in enumerate(game.current_hand.cards)
                         if card in self.other_players_cards
                       ]
        if discardable2 and (game.blue_coins<8):
            print ('Cheater would discard2:', "d%d"%discardable2[0], discardable2)
            return "d%d"%discardable2[0]


        ## Look at precious cards in other hand, to clue them
        precious = [ card for card in
                     self.other_players_cards
                     if (1+game.discard_pile.cards.count(card))
                         == game.deck.card_count[card.number]
                   ]
        if precious:
            clue = False
            # this loop is such that we prefer to clue an card close to chop
            # would be nice to clue an unclued first, instead of a already clued
            for p in precious:
                #print (p, p.number_clue, p.color_clue)
                if p.number_clue is False:
                    clue = "c%d"%p.number
                    break
                if p.color_clue is False:
                    clue = "c%s"%p.color
                    clue = clue[:2]   # quick fix, with 3+ players, can't clue cRed anymore, only cR
                    break
                # this one was tricky:
                # don't want to give twice the same clue
            if clue:
                print ('Cheater would clue a precious:',
                       clue, precious)
                if game.blue_coins>0:
                    return clue
                print ("... but there's no blue coin left!")


        # if reach here, can't play, can't discard safely, no card to clue-save
        # Let's give a random clue, to see if partner can unblock me
        if game.blue_coins >0:
            print ('Cheater would clue randomly: cW')
            return 'cw' #fixme : clue really randomly

        # If reach here, can't play, can't discard safely
        # No blue-coin left.
        # Must discard a card. Let's choose a non-precious one (preferably a 4)
        mynotprecious = [ (card.number,i+1) for (i,card) in
                          enumerate(game.current_hand.cards)
                          if not (
                                  (1+game.discard_pile.cards.count(card))
                                  == game.deck.card_count[card.number])
                     ]
        mynotprecious.sort(key=lambda p: (-p[0], p[1]))
        if mynotprecious:
            act = 'd%d'%mynotprecious[0][1]
            print('Cheater is trapped and must discard:', act, mynotprecious)
            return act

        # Oh boy, not even a safe discard, this is gonna hurt!
        # it's a loss. Discard the biggest
        myprecious = [ (card.number,i+1) for (i,card) in enumerate(game.current_hand.cards) ]
        myprecious.sort(key=lambda p: (-p[0], p[1]))
        act = 'd%d'%myprecious[0][1]
        print('Cheater is doomed and must discard:', act, myprecious)
        return act


class Random(AI):
    """
    This AI plays like a child, which is partially random but use the clue given and try not to fail the game

    Algorithm : 
        * if the AI knows some useful clue about its card, make it play one at random among the useful ones.
        * Do not play at random if there are two red coins
        * if 0 < blue_coins < 8 pick randomly between play, discard or clue.
            * if play is chosen, pick randomly between the unclued cards and other cards that won't make the game fail (ie : +1 red_coin)
            * if clue is chosen, give clue on a random card among the ones unclued.
            * if discard is chosen, discard any card in hand
        * if blue_coins == 8 pick randomly between play or clue
        * if blue_coins == 0 pick randomly between play or discard.
    
    This AI is supposed to lose after discarding all the cards
    
    """

    def play(self):

        "Return a random action."
        game = self.game

        #if the cards fit, make it play one of them
        precious = [(i+1, card.number) for (i,card) in enumerate(game.current_hand.cards) if card.number_clue and game.piles[card.color]+1 == card.number]
        num_precious = len(precious)

        #find the cards in our own hand that we don't know anything about, or the one that we know match.
        playable = [ (i+1, card.number) for (i,card) in enumerate(game.current_hand.cards) if not card.number_clue or ( card.number_clue and game.piles[card.color]+1 == card.number )]
        num_playable = len(playable)

        #find the unclued cards in the other players hands
        unclued = [ card for card in game.hands[game.other_player].cards if ((not card.color_clue) or (not card.number_clue)) ]
        num_unclued = len(unclued)
        
        #if blue coins are not restrictive, choose randomly
        if (game.blue_coins>0) and (game.blue_coins<=8):
            action = random.randint(1,4) # 1 = play ; 2 = discard ; 3 >= clue ; I made it clue more so that the parties can last a bit longer 
        
            # cannot clue an already clued card
            if num_unclued == 0 :
                action = random.randint(1,2)

            # cannot play if we know all the cards and they don't match the pile now, cannot play randomly if the game is about to be lost
            if num_playable==0 or game.red_coins == 2 :
                # cannot play, so do action 2 or 3
                action = random.randint(2,3) #it can clue if it cannot play
            

        elif game.blue_coins == 0 : #no more blue coins
            action = random.randint(1,2)
            if num_playable==0 or game.red_coins == 2 :
                # cannot play, so discard
                action = 2

        if precious :
            "play one precious card"
            card_to_play = random.randint(1, num_precious)
            ind = precious[card_to_play-1][0]
            print ('Random would play wisely:', "p%d"%ind)
            return "p%d"%ind

        
            
        if action == 1:
            "play one card at random"
            # do not play the card that we know doesn't match the pile now
            # select randomly from unknown cards

            card_to_play = random.randint(1, num_playable)
            ind = playable[card_to_play-1][0]
            print ('Random would play:', "p%d"%ind)
            return "p%d"%ind
              
              
        if action == 2:
            "discard one card"
            to_discard = random.randint(1, 4) #if the game is set to less than 4 players it doesn't really matter, it is still quite random
            print ('Random would discard: ', "d%d"%to_discard)
            return ("d%d"%to_discard)


        if action >= 3:
            "clue"

            #if you can't play or discard
            if not unclued:
                number_card = random.randint(1,4)
                random_card = game.current_hand.cards[number_card-1] 
                piece = random.randint(1,2)
                if piece == 1 :
                    clue = "c%d"%random_card.number
                else :
                    clue = "c%s"%random_card.color
                    clue = clue[:2]

            
            else : #choose randomly among the unclued cards
                number_card = random.randint(1,num_unclued)
                random_card = unclued[number_card-1] 
                

                if random_card.color_clue :         #si on a déjà l'indice de couleur c'est qu'il manque l'indice de nombre
                    clue = "c%d"%random_card.number
                elif random_card.number_clue :      #si on a déjà l'indice de nombre c'est qu'il manque l'indice de couleur
                    clue = "c%s"%random_card.color
                    clue = clue[:2]
                else :                              #sinon on tire au hasard si on va donner l'indice de couleur ou de nombre puisqu'aucun n'est connu
                    piece = random.randint(1,2)
                    if piece == 1 :
                        clue = "c%d"%random_card.number
                    else :
                        clue = "c%s"%random_card.color
                        clue = clue[:2]
            print("Random would clue: ", clue)

            return clue

       



## blablabla
