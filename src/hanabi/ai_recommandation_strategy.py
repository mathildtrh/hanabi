"""
Artificial Intelligence to play Hanabi.
"""
import itertools

import hanabi
from hanabi.ai import AI


class Recom_Strategist(AI):

    """
    This player uses the recommandation strategy, based on the principle of the guessing hat game

    Code for the clues :
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

    #those are two global variables
    latest_clue = [5] #action d1 by default
    game_changed = False

    def play(self):
        "Return the most relevant action according to the recommandation strategy."
        game = self.game
        nb_players = len(game.players)

        #is the same for every game : if there are 4 or 5 players, 4 and 9 should never be used
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
             if (1+game.discard_pile.cards.count(card))
                 == game.deck.card_count[card.number]]
        play_limit = 5
        act = "d1" #action by default

        latest_clue = [5] #passed in arg
        game_changed = False #idem

        #the code we use varies with the number of players, this is why we use a switch structure
        if nb_players == 2:
            how_to_clue = {
                "c1" : 0,
                "c2" : 1,
                "c3" : 2,
                "c4" : 3,
                "c5" : 4,
                "cr" : 5,
                "cb" : 6,
                "cg" : 7,
                "cy" : 8,
                "cw" : 9
            }
        elif nb_players == 3: #demands an extension of the way of giving clues : the 3rd char should be the number of the player who receives the clue
            how_to_clue = {
                "c1A" : 0,
                "c2A" : 2,
                "c3A" : 3,
                "c4A" : 3,
                "c5A" : 3,
                "c1B" : 1,
                "c2B" : 4,
                "c3B" : 4,
                "c4B" : 4,
                "c5B" : 4,
                "cRA" : 5,
                "cBA" : 7,
                "cGA" : 8,
                "cYA" : 8,
                "cWA" : 8,
                "cRB" : 6,
                "cBB" : 9,
                "cGB" : 9,
                "cYB" : 9,
                "cWB" : 9 }
        elif nb_players == 4:
            how_to_clue = {
                "c1A" : 0,
                "c2A" : 1,
                "c3A" : 1,
                "c4A" : 1,
                "c5A" : 1,
                "c1B" : 2,
                "c2B" : 2,
                "c3B" : 2,
                "c4B" : 2,
                "c5B" : 2,
                "c1C" : 3,
                "c2C" : 3,
                "c3C" : 3,
                "c4C" : 3,
                "c5C" : 3,
                "cRA" : 5,
                "cBA" : 6,
                "cGA" : 6,
                "cYA" : 6,
                "cWA" : 6,
                "cRB" : 7,
                "cBB" : 7,
                "cGB" : 7,
                "cYB" : 7,
                "cWB" : 7,
                "cRC" : 8,
                "cBC" : 8,
                "cGC" : 8,
                "cYC" : 8,
                "cWC" : 8 }
        elif nb_players == 5:
            how_to_clue = {
                "c1A" : 0,
                "c2A" : 0,
                "c3A" : 0,
                "c4A" : 0,
                "c5A" : 0,
                "c1B" : 1,
                "c2B" : 1,
                "c3B" : 1,
                "c4B" : 1,
                "c5B" : 1,
                "c1C" : 2,
                "c2C" : 2,
                "c3C" : 2,
                "c4C" : 2,
                "c5C" : 2,
                "c1D" : 3,
                "c2D" : 3,
                "c3D" : 3,
                "c4D" : 3,
                "c5D" : 3,
                "cRA" : 5,
                "cBA" : 5,
                "cGA" : 5,
                "cYA" : 5,
                "cWA" : 5,
                "cRB" : 6,
                "cBB" : 6,
                "cGB" : 6,
                "cYB" : 6,
                "cWB" : 6,
                "cRC" : 7,
                "cBC" : 7,
                "cGC" : 7,
                "cYC" : 7,
                "cWC" : 7,
                "cRD" : 8,
                "cBD" : 8,
                "cGD" : 8,
                "cYD" : 8,
                "cWD" : 8 }


        def give_a_clue(nb_players, playable, discardable, precious): #returns an int

                #how_to_clue = {v:k for k,v in how_to_clue.items()}
                joueurs = { "A" : 1 , "B" : 2 , "C" : 3 , "D" : 4 }
                couleurs = { "R" : hanabi.deck.Color.Red , "B" : hanabi.deck.Color.Blue , "Y" : hanabi.deck.Color.Yellow , "W" : hanabi.deck.Color.White , "G" : hanabi.deck.Color.Green }
                sum = 0
                for hand in game.hands:
                    color = value_hand(hand, playable, discardable, precious)
                    sum = sum + color
                clue = sum%10
                
                available_clues = []
                for cle, valeur in how_to_clue.items() :
                    if valeur == clue :
                        available_clues.append(cle)
                
                action = available_clues[0]

                if nb_players>2: #pour gérer la troisième lettre de l'indice
                    for clue in available_clues : #cherche à qui on peut donner l'indice parmi tous les joueurs
                        indice = clue[1]
                        joueur = joueurs[clue[2]]
                        for card in game.hands[joueur].cards:
                            if indice in "12345" :
                                if card.number == int(indice):
                                    action = clue
                            elif indice in "RWBGY" :
                                if card.color == couleurs[indice] :
                                    action = clue
                
                return action





        def value_hand (hand, playable, discardable, precious):
            # play the "5" card with lowest index
            # play the card with lowest rank (+ lowest index if conflict)
            # play the dead card with lowest index
            # discard the not indispensable card with highest rank (+ lowest index if conflict)
            # discard 1st card of the hand

            miniplay = 5
            maxinotprecious = 1
            i=1
            code = -1

            for card in hand.cards :
                if card in playable:
                    if card.number == 5:
                        code = "p%d"%i
                    elif card.number < miniplay:
                        code = "p%d"%i
                        miniplay = card.number
                elif card in discardable:
                    code = "d%d"%i  
                elif card not in precious:
                    if card.number > maxinotprecious:
                        code = "d%d"%i
                        maxinotprecious = card.number
                      
                
                #if the current card is not playable, not discardable and precious, go to the next card

            if code == -1:
                code = "d1"
            return how_to_play_reversed[code]






        # if the latest clue was to play a card AND if no card was played, then play the recommended card
        current_state_of_game = 0
        for hand in game.hands:
            color = value_hand(hand, playable, discardable, precious)
            current_state_of_game = current_state_of_game + color
        if latest_clue[-1] < play_limit :
            if not game_changed :
                act = how_to_play[(latest_clue[-1] - current_state_of_game)%10]
                game_changed = True
                return act
            # if the latest clue was to play a card AND if a card was played AND there is less than 2 red coins, then play the recommended card
            elif game.red_coins < 2 :
                act = how_to_play[(latest_clue[-1] - current_state_of_game)%10]
                game_changed = True
                return act
            # if there is some blue coin available, give a clue
            elif game.blue_coins > 0:
                latest_clue.append(how_to_clue[give_a_clue(len(game.players), playable, discardable, precious)])
                act = give_a_clue(len(game.players), playable, discardable, precious)
                game_changed = False
                return act
            # else, discard 1st card of the hand
            else :
                return act
        # if the latest clue was to discard a card, then discard the recommended card (unless it's the first turn)
        ####-----------------------issue if it becomes an indispensable card!!-------------------------####
        else :
            if game.blue_coins == 8 :
                latest_clue.append(how_to_clue[give_a_clue(len(game.players), playable, discardable, precious)])
                act = give_a_clue(len(game.players), playable, discardable, precious)
                game_changed = False
                return act
            else :
                act = how_to_play[(latest_clue[-1] - current_state_of_game)%10]
                return act
        






    
