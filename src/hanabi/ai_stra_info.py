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
        self.game = game(5)
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
    color_inverse = { 34:0, 32:1, 31:2, 37:3, 33:4 }
    card_count = {1:3, 2:2, 3:2, 4:2, 5:1 }


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

    def if_duplicate(self, i, card_i):
        other_players = [0,1,2,3,4]
        other_players.remove(self.game.current_player)
        for i in range(0, 4):
            hand = self.game.hands[i]
            for (c, card) in enumerate(hand.cards):
                if card.color==card_i.color and card.number==card_i.number:
                    return True
        return False
    
    def if_dispensable(self, i, card_i):
        number = card_i.number
        n_discard = 0
        for (c, card) in enumerate(self.game.discard_pile):
            if card.number==number and card.color==card_i.color:
                n_discard += 1
        if sefl.card_count[number]-n_discard<1:
            return False
        else:
            return True

    # determine the target card for each player
    def calcul_target(self, players, p_table):
        target_cards = []
        for i in players:
            hand = self.game.hands[i]
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

    # build the partition table to determine the action of the current player
    def tell_action(self, players, target_cards, p_table):
        # 4 players
        table_partition = np.zeros(4, 5, 5)
        j = 0 # j-th card in target_cards
        ratio_playable = 0
        ratio_table = []
        for i in range(0, 4):
            player = players[i]
            card_number = target_cards[i]
            ratio_i_cards = 1 # the ratio of possibilities of this card
            for k in range(0, 5): # 5 ranks
                for l in range(0, 5): # 5 suits
                    if p_table[player][card_number][l][k]==1:
                        if self.game.piles[self.color_p_table[l]]+1 > k+1:
                            table_partition[i][k][l] = 0
                        else:
                            if ratio_i_cards<7:
                                table_partition[i][k][l] = ratio_i_cards
                                ratio_i_cards += 1
                            else:
                                table_partition[i][k][l] = 7
                    else:
                        table_partition[i][k][l] = -1 # to represent its impossibility
            # tell the ratio of this card
            hand = self.game.hands[player]
            for (c, card) in enumerate(hand.cards):
                if c==card_number:
                    color = card.color
                    ratio_i_card = table_partition[i][c-1][self.color_inverse[color]]
            ratio_table.append(ratio_i_card)
            ratio_playable += ratio_i_card
        action = ratio_playable%8
        return [action, ratio_table, table_partition]

    def adjust_p_table(self, players, target_cards, action, ratio_table, table_partition):
        for i in range(0,4): # 4 other players
            ratio_he_knows = 0 # this player knows others ratio except his
            for j in range(0, 4):
                if i==j:
                    continue
                else:
                    ratio_he_knows += ratio_table[j]
            # then he uses the action to tell his own ratio of his target card
            total_ratio = action
            while total_ratio<ratio_he_knows:
                total_ratio += 8
            ratio_his = total_ratio - ratio_he_knows
            # he can use this information to change the possibility table
            if ratio_his<7:
                # then this card is known by all
                hand = self.game.hands[players[i]]
                for (c, card) in enumerate(hand.cards):
                    if c==target_cards[i]:
                        card.color_clue = True
                        card.number_clue = True
            for i in range(0,5): # 5 colors
                for j in range(0, 5): # 5 ranks
                    if table_partition[i][i][j]!=ratio_his:
                        self.p_table[players[i]][target_cards[i]][i][j] = 0

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
            target_cards = self.calcul_target(players, self.p_table)
            [action, ratio_table, table_partition] = self.tell_action(players, target_cards, self.p_table)
            if action<4:
                # rank hint to the player in position 'action'
                hand = self.game.hands[players[action]]
                for (c, card) in enumerate(hand.cards):
                    if c==target_cards[action]:
                        rank = card.number
                        clue = "c%d"%card.number
                        # problem with print...
                        #
                # new possibility table
                for (c, card) in enumerate(hand.cards):
                    if card.number==rank:
                        card.number_clue = True
                        for i in range(0, 5): # 5 suits
                            for j in range(0, 5): # 5 ranks
                                if j!= card.number-1:
                                    self.p_table[players[action]][c][i][j] = 0
                print ('Stra_info would clue :',
                       clue, ' of player ', players[action])
            else:
                #suit hint to the player in position 'action-4'
                hand = self.game.hands[players[action-4]]
                for (c, card) in enumerate(hand.cards):
                    if c==target_cards[action-4]:
                        color = card.color
                        clue = "c%d"%card.color
                        # problem with print...
                        #
                # new possibility table
                for (c, card) in enumerate(hand.cards):
                    if c==target_cards[action-4]:
                        card.color_clue = True
                        clue = "c%d"%card.color
                        for i in range(0, 5): # 5 suits
                            for j in range(0, 5): # 5 ranks
                                if i!= self.color_inverse[card.color]:
                                    self.p_table[players[action]][c][i][j] = 0
                print ('Stra_info would clue :',
                       clue, ' of player ', players[action-4])
            # possibility table needs to be changed according to the action
            # everyone profits from the action
            self.adjust_p_table(players, target_cards, action, ratio_table, table_partition)
            return clue


        # discard the dead card with lowest index
        if dead:
            print ('Stra_info would discard:', "d%d"%dead[0], dead)
            return "d%d"%dead[0]


        # discard the duplicate card
        duplicate = [ (i+1, card) for (i,card) in
                     enumerate(game.current_hand.cards)
                     if self.if_duplicate(i, card) ]
        if duplicate:
            print ('Stra_info would discard:', "d%d"%duplicate[0], duplicate)
            return "d%d"%duplicate[0]
        

        # discard the dispensable card 
        dispensable = [ (i+1, card) for (i,card) in
                     enumerate(game.current_hand.cards)
                     if self.if_dispensable(i, card) ]
        if dispensable:
            print ('Stra_info would discard:', "d%d"%dispensable[0], dispensable)
            return "d%d"%dispensable[0]


        # discard the first card
        cards = [ (i+1, card) for (i,card) in
                     enumerate(game.current_hand.cards) ]
        print ('Stra_info would discard:', "d%d"%cards[0], cards)
        return "d%d"%cards[0]

