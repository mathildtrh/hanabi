"""
Artificial Intelligence to play Hanabi with the information strategy.
"""

from . import deck
import random
import itertools
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

    @property
    def other_hands(self):
        "The list of other players' hands."
        return self.game.hands[1:]

    @property
    def other_players_cards(self):
        "All of other players's cards, concatenated in a single list."
        #return sum([x.cards for x in self.other_hands], [])
        return list(itertools.chain.from_iterable([hand.cards for hand in self.other_hands]))
    

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
    p_table = np.ones((5, 4, 5, 5))
    color_p_table = { 0:34, 1:32, 2:31, 3:37, 4:33 } # Figure 3 of Hanabi_final.pdf


    def cards_possible(self, p_table_current):
        # 5 players
        possibility_current = []
        for (i, card) in enumerate(self.game.current_hand.cards):
            card.possible = []
            n_p_card = 0
            for j in range(0, 5):
                for k in range(0, 5):
                    if p_table_current[i][j][k]==1 :
                        n_p_card += 1
                        card.possible.append(deck.Card(self.color_p_table[j], k+1))
            if n_p_card==1:
                card.color_clue = True
                card.number_clue = True
                card = card.possible[0]
            possibility_current.append(card.possible)
        return possibility_current

    def if_playable(self, i, card, possibility_current):
        if card.color_clue == True and card.number_clue==True and self.game.piles[card.color]+1 == card.number:
            return True
        for (index, p) in enumerate(possibility_current[i]):
            if (self.game.piles[p.color]+1!=p.number):
                return False
        return True

    def if_dead(self, i, card, possibility_current):
        if card.color_clue == True and card.number_clue==True and self.game.piles[card.color]+1 > card.number:
            return True
        for (index, p) in enumerate(possibility_current[i]):
            if (self.game.piles[p.color]+1 <= p.number):
                return False
        return True

    def calcul_target(players, p_table):
        target_cards = []
        for i in players:
            hand = self.hands[i]
            probability_playable_c = 0
            for (c, card) in enumerate(hand.cards):
                t_c = 0
                a_c = 0
                for j in range(0, 5):
                    for k in range(0, 5):
                        if p_table[i][c][j][k]==1:
                            t_c += 1
                            possibility_current_c = self.cards_possible(self.p_table[i])
                            if self.if_playable(c, card, possibility_current_c):
                                a_c += 1
                if a_c/t_c > probability_playable_c:
                    probability_playable_c = a_c / t_c
                    target_c = c
            target_cards.append(target_c)
        return target_cards

    def tell_action(plyers, target_cards, p_table):
        # 4 players
        table_partition = np.zeros(4, 5, 5)
        t_ratio = 
        for i in range(0, 4):
            


    def play(self):
        game = self.game
        possibility_current = self.cards_possible(self.p_table[game.current_player])

        # if 1-or-more card is playable: play the lowest one, then newest one
        playable = [ (i+1, card.number) for (i,card) in
                     enumerate(game.current_hand.cards)
                     if self.if_playable(i, card, possibility_current)]

        if playable: 
            # <=> playable n'est pas vide
            # sort by ascending number, then newest
            playable.sort(key=lambda p: (p[1], -p[0]))
            print ('Stra_info would play:', "p%d"%playable[0][0], end=' ')
            return "p%d"%playable[0][0]
        
        # if less than 5 cards in the discard pile, dicard a dead card with lowest index
        dead = [ (i+1, card.number) for (i,card) in
                     enumerate(game.current_hand.cards)
                     if self.if_dead(i, card, possibility_current) ]
        if dead and len(game.discard_pile) < 5:
            print ('Stra_info would discard:', "d%d"%dead[0], dead)
            return "d%d"%dead[0]
        
        # if a token exists, give a hint
        if game.blue_coins>0:
            players = [0,1,2,3,4]
            players.remove(game.current_player)
            # find the 4 target cards, one for one player
            target_cards = self.calcul_target(self, players, self.p_table)
            action = self.tell_action(self, players, target_cards, self.p_table)



    
