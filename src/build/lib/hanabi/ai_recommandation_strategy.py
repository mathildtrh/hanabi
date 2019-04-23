"""
Artificial Intelligence to play Hanabi.
"""

class AI:
    """
    AI base class: some basic functions, game analysis.
    """
    def __init__(self, game):
        self.game = game


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

    def play(self, latest_clue, game_changed):
        "Return the most relevant action according to the recommandation strategy."
        game = self.game

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

        playable = [ (i+1, card.number) for (i,card) in
                     enumerate(game.current_hand.cards)
                     if game.piles[card.color]+1 == card.number ]
        discardable = [ i+1 for (i,card) in
                        enumerate(game.current_hand.cards)
                        if ( (card.number <= game.piles[card.color])
                             or (game.current_hand.cards.count(card)>1)
                        ) ]
        # fixme: il me manque les cartes sup d'une pile morte
        # fixme: penser aussi aux doubles dans les mains des partenaires?
        precious = [ card for card in
             self.other_players_cards
             if (1+game.discard_pile.cards.count(card))
                 == game.deck.card_count[card.number]]

        act = "d1" #action by default
        latest_clue = latest_clue #passed in arg
        game_changed = False #idem




        
        # if the latest clue was to play a card AND if no card was played, then play the recommended card
        if latest_clue < play_limit and !game_changed :
            act = how_to_play[latest_clue]
            game_changed = True
            return act, latest_clue, game_changed
        # if the latest clue was to play a card AND if a card was played AND there is less than 2 red coins, then play the recommended card
        elif latest_clue < play_limit and red_coins < 2 :
            act = how_to_play[latest_clue]
            game_changed = True
            return act, latest_clue, game_changed
        # if there is some blue coin available, give a clue
        elif blue_coins > 0:
            latest_clue = give_a_clue(len(game.players), playable, discardable, precious)
            act = how_to_play[latest_clue]
            game_changed = False
            return act, latest_clue, game_changed
        # if the latest clue was to discard a card, then discard the recommended card
        ####-----------------------issue if it becomes an indispensable card!!-------------------------####
        elif latest_clue >= play_limit :
            act = how_to_play[latest_clue]
            return act, latest_clue, game_changed
        # else, discard 1st card of the hand
        else :
            return act, latest_clue, game_changed






        
    def give_a_clue(self, nb_players, playable, discardable, precious): #returns an int
        
        #the code we use varies with the number of players, this is why we use a switch structure
                switch (nb_players)
            case 2:
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

            case 3: #demands an extension of the way of giving clues : the 3rd char should be the number of the player who receives the clue
                how_to_clue = {
                    "c1A" = 0,
                    "c2A" = 2,
                    "c3A" = 3,
                    "c4A" = 3,
                    "c5A" = 3,
                    "c1B" = 1,
                    "c2B" = 4,
                    "c3B" = 4,
                    "c4B" = 4,
                    "c5B" = 4,
                    "crA" = 5,
                    "cbA" = 7,
                    "cgA" = 8,
                    "cyA" = 8,
                    "cwA" = 8,
                    "crB" = 6,
                    "cbB" = 9,
                    "cgB" = 9,
                    "cyB" = 9,
                    "cwB" = 9 }

            case 4:
                 how_to_clue = {
                    "c1A" = 0,
                    "c2A" = 1,
                    "c3A" = 1,
                    "c4A" = 1,
                    "c5A" = 1,
                    "c1B" = 2,
                    "c2B" = 2,
                    "c3B" = 2,
                    "c4B" = 2,
                    "c5B" = 2,
                    "c1C" = 3,
                    "c2C" = 3,
                    "c3C" = 3,
                    "c4C" = 3,
                    "c5C" = 3,
                    "crA" = 5,
                    "cbA" = 6,
                    "cgA" = 6,
                    "cyA" = 6,
                    "cwA" = 6,
                    "crB" = 7,
                    "cbB" = 7,
                    "cgB" = 7,
                    "cyB" = 7,
                    "cwB" = 7,
                    "crC" = 8,
                    "cbC" = 8,
                    "cgC" = 8,
                    "cyC" = 8,
                    "cwC" = 8 }

            case 5:
                how_to_clue = {
                    "c1A" = 0,
                    "c2A" = 0,
                    "c3A" = 0,
                    "c4A" = 0,
                    "c5A" = 0,
                    "c1B" = 1,
                    "c2B" = 1,
                    "c3B" = 1,
                    "c4B" = 1,
                    "c5B" = 1,
                    "c1C" = 2,
                    "c2C" = 2,
                    "c3C" = 2,
                    "c4C" = 2,
                    "c5C" = 2,
                    "c1D" = 3,
                    "c2D" = 3,
                    "c3D" = 3,
                    "c4D" = 3,
                    "c5D" = 3,
                    "crA" = 5,
                    "cbA" = 5,
                    "cgA" = 5,
                    "cyA" = 5,
                    "cwA" = 5,
                    "crB" = 6,
                    "cbB" = 6,
                    "cgB" = 6,
                    "cyB" = 6,
                    "cwB" = 6,
                    "crC" = 7,
                    "cbC" = 7,
                    "cgC" = 7,
                    "cyC" = 7,
                    "cwC" = 7,
                    "crD" = 8,
                    "cbD" = 8,
                    "cgD" = 8,
                    "cyD" = 8,
                    "cwD" = 8 }
                
            #how to setup a default reaction? raise exception?

            sum = 0
            for hand in game.hands:
                color = how_to_clue[value_hand(hand, playable, discardable, precious)]
                sum = sum + color
            clue = sum%10

            return clue




        

    def value_hand (self, hand, playable, discardable, precious):
        # play the "5" card with lowest index
        # play the card with lowest rank (+ lowest index if conflict)
        # play the dead card with lowest index
        # discard the not indispensable card with highest rank (+ lowest index if conflict)
        # discard 1st card of the hand

        solution = False
        miniplay = 5
        maxinotprecious = 1
        i=1
        code = -1

        while solution == False and i <= len(hand):
            card = hand[i]
            if card in playable:
                if card.number == 5:
                    code = "p%d"%i
                    solution = True
                elif card.number < miniplay:
                    code = "p%d"%i
                    miniplay = card.number
                    i += 1
                else :
                    pass
            elif card in discardable:
                code = "d%d"%i
                i += 1
            elif card not in precious:
                if card.number > maxinotprecious:
                    code = "d%d"%i
                    maxinotprecious = card.number
                    i += 1
                else:
                    pass
            else: #if the current card is not playable, not discardable and precious, go to the next card
                i += 1

        if code == -1:
            code = "d1"
        return code

##to do : faire la bonne définition de playable, discardable, precious







