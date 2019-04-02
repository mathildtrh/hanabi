"""
Artificial Intelligence to play Hanabi.
"""

import random

class AI:
    """
    AI base class: some basic functions, game analysis.
    """
    def __init__(self, game):
        self.game = game


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

        if playable:
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
                         if card in game.hands[game.other_player].cards
                       ]
        if discardable2 and (game.blue_coins<8):
            print ('Cheater would discard2:', "d%d"%discardable2[0], discardable2)
            return "d%d"%discardable2[0]
        

        ## Look at precious cards in other hand, to clue them
        precious = [ card for card in
                     game.hands[game.other_player].cards
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
            return 'cw'

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
    This player will play randomly
    try to not lose but won't try to win
    Algorithm:
     (randomly choose one of actions below)
     * choose from the cards which don't belong to cards not playable
     * discard
     * give a clue
    """

    def play(self):
        game = self.game
        action = random.randint(1,3) # 1 play, 2 discard, 3 clue

        while action==1:
            "play one card"
            # not play the card that not match the pile now
            # select randomly from unknown cards or the matched cards
            not_playable = [ (i+1, card.number) for (i,card) in
                     enumerate(game.current_hand.cards)
                     if card.number_clue==True and game.piles[card.color]+1 != card.number ]
    
            num_not_playable = len(not_playable)
            if num_not_playable==5:
                # cannot play, so do action 2 or 3
                action = random.randint(2,3)
                break
            else:
                """
                # find card playable
                playable = [ (i+1, card.number) for (i,card) in
                            enumerate(game.current_hand.cards)
                            if card.number_clue==True and game.piles[card.color]+1 == card.number ]
                """
                # play randomly a card
                card_to_play = random.randint(1, 5-num_not_playable)
                k = 0
                for j in range(0, card_to_play):
                        k = k + 1
                        if (k+1,game.current_hand.cards[k]) in not_playable:
                            k = k + 1 
                    print ('Random would play:', "p%d"%(k+1), end=' ')
                    return "p%d"%(k+1)   

        while action==2:
            pass

        while action==3:
            pass