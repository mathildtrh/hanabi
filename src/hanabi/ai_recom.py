"""
Artificial Intelligence to play Hanabi.
"""
import itertools

import hanabi
from hanabi.ai import AI


class Recom_Strategist(AI):

    """
    This player uses the recommandation strategy, based on the principle of the guessing hat game

    Code for the self.CLUES :
      * from 0 to 3/4 = play cards from 1 to 4/5
      * from 4/5 to 7/9 = discard cards from 1 to 4/5
      * NB : if there are 4 or 5 players, 4 and 9 should never be used

    Algorithm to decide what action to do now:
      * if the latest clue was to play a card AND if no card was played, then play the recommended card
      * if the latest clue was to play a card AND if a card was played AND there is less than 2 red coins, then play the recommended card
      * if there is some blue coin available, give a clue
      * if the latest clue was to discard a card, then discard the recommended card  ####issue if it becomes an indispensable card!!
      * else, discard 1st card of the hand

    How to give a relevant clue:
      * play the "5" card with lowest index
      * play the card with lowest rank (+ lowest index if conflict)
      * play the dead card with lowest index
      * discard the not indispensable card with highest rank (+ lowest index if conflict)
      * discard 1st card of the hand
    """

    def play(self):
        "Return the most relevant action according to the recommandation strategy."
        game = self.game
        nb_players = len(game.players)


        #is the same for every game : if there are 4 or 5 players, 4 and 9 should never be used
        def how_to_play(nb_players) :
            if nb_players < 4 :
                how_to_play = {
                0 : "p1",
                1 : "p2",
                2 : "p3",
                3 : "p4",
                4 : "p5",
                5 : "d1",
                6 : "d2",
                7 : "d3",
                8 : "d4",
                9 : "d5"
                } #key = color of the hand // value = action
            else :
                how_to_play = {
                0 : "p1",
                1 : "p2",
                2 : "p3",
                3 : "p4",
                4 : "d1",
                5 : "d2",
                6 : "d3",
                7 : "d4",
                } #key = color of the hand // value = action

            return how_to_play

        how_to_play = how_to_play(nb_players)
        how_to_play_reversed = {v:k for k,v in how_to_play.items()} #key = action // value = color of the hand

        playable = [ card for card in
                     [hanabi.deck.Card(hanabi.deck.Color.Red, 1), hanabi.deck.Card(hanabi.deck.Color.Red, 2),  hanabi.deck.Card(hanabi.deck.Color.Red, 3), hanabi.deck.Card(hanabi.deck.Color.Red, 4), hanabi.deck.Card(hanabi.deck.Color.Red, 5),
                      hanabi.deck.Card(hanabi.deck.Color.Blue, 1), hanabi.deck.Card(hanabi.deck.Color.Blue, 2), hanabi.deck.Card(hanabi.deck.Color.Blue, 3), hanabi.deck.Card(hanabi.deck.Color.Blue, 4), hanabi.deck.Card(hanabi.deck.Color.Blue, 5),
                      hanabi.deck.Card(hanabi.deck.Color.Green, 1), hanabi.deck.Card(hanabi.deck.Color.Green, 2), hanabi.deck.Card(hanabi.deck.Color.Green, 3), hanabi.deck.Card(hanabi.deck.Color.Green, 4), hanabi.deck.Card(hanabi.deck.Color.Green, 5),
                      hanabi.deck.Card(hanabi.deck.Color.White, 1), hanabi.deck.Card(hanabi.deck.Color.White, 2), hanabi.deck.Card(hanabi.deck.Color.White, 3), hanabi.deck.Card(hanabi.deck.Color.White, 4), hanabi.deck.Card(hanabi.deck.Color.White, 5),
                      hanabi.deck.Card(hanabi.deck.Color.Yellow, 1), hanabi.deck.Card(hanabi.deck.Color.Yellow, 2), hanabi.deck.Card(hanabi.deck.Color.Yellow, 3), hanabi.deck.Card(hanabi.deck.Color.Yellow, 4), hanabi.deck.Card(hanabi.deck.Color.Yellow, 5)] #attention au cas multicolore
                     if game.piles[card.color]+1 == card.number ]

        discardable = [ card for card in [hanabi.deck.Card(hanabi.deck.Color.Red, 1), hanabi.deck.Card(hanabi.deck.Color.Red, 2),  hanabi.deck.Card(hanabi.deck.Color.Red, 3), hanabi.deck.Card(hanabi.deck.Color.Red, 4), hanabi.deck.Card(hanabi.deck.Color.Red, 5),
                      hanabi.deck.Card(hanabi.deck.Color.Blue, 1), hanabi.deck.Card(hanabi.deck.Color.Blue, 2), hanabi.deck.Card(hanabi.deck.Color.Blue, 3), hanabi.deck.Card(hanabi.deck.Color.Blue, 4), hanabi.deck.Card(hanabi.deck.Color.Blue, 5),
                      hanabi.deck.Card(hanabi.deck.Color.Green, 1), hanabi.deck.Card(hanabi.deck.Color.Green, 2), hanabi.deck.Card(hanabi.deck.Color.Green, 3), hanabi.deck.Card(hanabi.deck.Color.Green, 4), hanabi.deck.Card(hanabi.deck.Color.Green, 5),
                      hanabi.deck.Card(hanabi.deck.Color.White, 1), hanabi.deck.Card(hanabi.deck.Color.White, 2), hanabi.deck.Card(hanabi.deck.Color.White, 3), hanabi.deck.Card(hanabi.deck.Color.White, 4), hanabi.deck.Card(hanabi.deck.Color.White, 5),
                      hanabi.deck.Card(hanabi.deck.Color.Yellow, 1), hanabi.deck.Card(hanabi.deck.Color.Yellow, 2), hanabi.deck.Card(hanabi.deck.Color.Yellow, 3), hanabi.deck.Card(hanabi.deck.Color.Yellow, 4), hanabi.deck.Card(hanabi.deck.Color.Yellow, 5)] #attention au cas multicolore
                     if game.piles[card.color]+1 > card.number ]

        precious = [ card for card in
             self.other_players_cards
             if (1+game.discard_pile.cards.count(card)
                 == game.deck.card_count[card.number])]
        

        
        act = "d1" #action by default

        self.GAME_CHANGED = False #idem

        def give_a_clue(nb_players,playable,discardable,precious) :
            #return the clue to give, and also the list of the hints for all the players
            sum = 0

            i=1
            self.CLUES[0] = 'x'
            for hand in game.hands[1:]:
                ind = value_hand(hand, playable, discardable, precious)
                self.CLUES[i]=ind
                sum = sum + ind
                i+=1
            if nb_players > 3 :
                indice = sum%8
                ind_card = indice%4
            else :
                indice = sum%10
                ind_card = indice%5
            
            card = game.hands[1].cards[ind_card]

            if nb_players > 3 :
                if indice >= 4 :
                    clue = str(card.color)[0]
                else :
                    clue = card.number
            else :
                if indice >= 5 :
                    clue = str(card.color)[0]
                else :
                    clue = card.number
            
                   
            return "c%s"%clue, self.CLUES #by default the clue is given to the next player which is perfect

        def interpret_clue(nb_players) :
            #get the clue received by one player the last time a clue was given
            #I might have cheated a little here but I explained in the compte rendu
            
            if game.moves[0][0] != 'c':
                print("le premier joueur n'a pas donné d'indice")
                return False

            i = 0
            j =-1
            while game.moves[j][0] != 'c' :
                i+=1
                j-=1
            clue = self.CLUES[(i+1)%(len(self.CLUES))]

            if clue == 'x' :
                return False


            return how_to_play[clue]
            


        def value_hand (hand, playable, discardable, precious):
            # play the "5" card with lowest index
            # play the card with lowest rank (+ lowest index if conflict)
            # play the dead card with lowest index
            # discard the not indispensable card with highest rank (+ lowest index if conflict)
            # discard 1st card of the hand

            current_playable = []
            current_discardable = []
            current_not_precious = []
            for card in hand.cards :
                if card in playable :
                    current_playable.append(card)
                if card in discardable :
                    current_discardable.append(card)
                if card not in precious :
                    current_not_precious.append(card)
  

            if current_playable :
                miniplay = min(card.number for card in current_playable)
            if current_not_precious :
                maxinotprecious = max(card.number for card in current_not_precious)
            i=0
            code = -1
            sortir = False

            while sortir == False :
                card = hand.cards[i]
                if card in playable:
                    if card.number == 5:
                        code = "p%d"%(i+1)
                        sortir = True
                    elif card.number == miniplay:
                        code = "p%d"%(i+1)
                        sortir = True
                elif code == -1 and card in discardable:
                    code = "d%d"%(i+1)  
                elif code == -1 and card not in precious:                        
                    if card.number == maxinotprecious:
                        code = "d%d"%(i+1)
 
                i+=1
                if i == len(hand.cards) :
                    sortir = True


            if code == -1:
                code = "d1"
            return how_to_play_reversed[code]




        print("LAST_ACTIONS :", game.moves)
        # forces the first player to give a clue :
        if game.moves == [] or interpret_clue(nb_players) == False :
            if game.blue_coins > 0 :
                act = give_a_clue(nb_players,playable,discardable,precious)[0]
            return act
        

        clue = interpret_clue(nb_players)
        # if the latest clue was to play a card AND if no card was played, then play the recommended card
    
        if clue[0] == 'p' :
            if not self.GAME_CHANGED :
                act = clue
                self.GAME_CHANGED = True
                return act
            # if the latest clue was to play a card AND if a card was played AND there is less than 2 red coins, then play the recommended card
            elif game.red_coins < 2 :
                act = clue
                self.GAME_CHANGED = True
                return act
            # if there is some blue coin available, give a clue
            elif game.blue_coins > 0 :
                act = give_a_clue(nb_players, playable, discardable, precious)[0]
                self.GAME_CHANGED = False
                return act
            # else, discard 1st card of the hand
            else :
                return act
        # if the latest clue was to discard a card, then discard the recommended card (unless it's the first turn)
        ####-----------------------issue if it becomes an indispensable card!!-------------------------####
        else :
            if game.blue_coins == 8 :
                act = give_a_clue(nb_players, playable, discardable, precious)[0]
                self.GAME_CHANGED = False
                return act
            else :
                act = clue
                self.GAME_CHANGED = True
                return act