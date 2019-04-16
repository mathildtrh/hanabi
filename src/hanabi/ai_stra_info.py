"""
Artificial Intelligence to play Hanabi with the information strategy.
"""

import random
import numpy as np

class AI:
    """
    AI base class: some basic functions, game analysis.
    """
    def __init__(self, game):
        self.game = game
        # possibility table
        # Suppose there is 5 players in this game
        # each has 4 cards
        # each card has 5 suits x 5 ranks = 25 possibilities
        # 1 possible, 0 impossible
        p_table = np.ones((5, 4, 5, 5))



class Stra_info(AI):
    """
    Use the information strategy.
    Algorithm:
      * if 1-or-more card is playable: play the lowest one, then newest one
      * if less than 5 cards in the discard pile, dicard a dead card with lowest index
      * if a token exists, give a hint
      * discard the dead card with lowest index
      * discard the duplicate card
      * discard the dispensable card 
      * discard the first card
    """
    def play(self):
        game = self.game
        playable = [ (i+1, card.number) for (i,card) in
                     enumerate(game.current_hand.cards)
                     if card.number_clue==True and game.piles[card.color]+1 == card.number ]

        if playable: 
            # <=> playable n'est pas vide
            # sort by ascending number, then newest
            playable.sort(key=lambda p: (p[1], -p[0]))
            print ('Stra_info would play:', "p%d"%playable[0][0], end=' ')
            """
            if (len(playable)>1):
                print('but could also pick:', playable[1:])
            else: print()
            """
            return "p%d"%playable[0][0]
        

