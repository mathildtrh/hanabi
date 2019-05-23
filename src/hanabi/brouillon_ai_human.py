class Human(AI):
    """
    This AI is a series of improvements of a random IA

    1st improvement : looks at the dead and finiched piles + doesn't randomly choose between play clue and discard

    Algorithm : 
        * if the AI knows some useful clue about its card, make it play one at random among the useful ones.
        * if a pile is finished or dead
            * don't play this color
            * clue this color to other players
        * if 0 < blue_coins < 8 pick in order play then clue then discard.
            * if play is chosen, pick randomly between the unclued cards and other cards that won't make the game fail (ie : +1 red_coin)
            * if clue is chosen, give clue on a random card among the unclued ones.
            * if discard is chosen, discard any card in hand
        * if blue_coins == 8 pick randomly between play or clue
        * if blue_coins == 0 pick randomly between play or discard.
    
    This AI is supposed to lose after discarding all the cards
    
    """

    def play(self):

        "Return an action according to the algorithm updated from random."
        game = self.game

        #find the cards in our own hand that we know can be safely played.
        playable = [(i+1, card.number) for (i,card) in enumerate(game.current_hand.cards) if (card.number_clue and game.piles[card.color]+1 == card.number)]
        num_playable = len(playable)
        print("Nombre de cartes jouables ", num_playable)

        #find the unclued cards in the other players hands
        unclued = [card for card in game.hands[game.other_player].cards if ((not card.color_clue) or (not card.number_clue))]
        num_unclued = len(unclued)

        #find the cards that we know are safely discardable
        discardable = [ card for card in [hanabi.deck.Card(hanabi.deck.Color.Red, 1), hanabi.deck.Card(hanabi.deck.Color.Red, 2),  hanabi.deck.Card(hanabi.deck.Color.Red, 3), hanabi.deck.Card(hanabi.deck.Color.Red, 4), hanabi.deck.Card(hanabi.deck.Color.Red, 5),
            hanabi.deck.Card(hanabi.deck.Color.Blue, 1), hanabi.deck.Card(hanabi.deck.Color.Blue, 2), hanabi.deck.Card(hanabi.deck.Color.Blue, 3), hanabi.deck.Card(hanabi.deck.Color.Blue, 4), hanabi.deck.Card(hanabi.deck.Color.Blue, 5),
            hanabi.deck.Card(hanabi.deck.Color.Green, 1), hanabi.deck.Card(hanabi.deck.Color.Green, 2), hanabi.deck.Card(hanabi.deck.Color.Green, 3), hanabi.deck.Card(hanabi.deck.Color.Green, 4), hanabi.deck.Card(hanabi.deck.Color.Green, 5),
            hanabi.deck.Card(hanabi.deck.Color.White, 1), hanabi.deck.Card(hanabi.deck.Color.White, 2), hanabi.deck.Card(hanabi.deck.Color.White, 3), hanabi.deck.Card(hanabi.deck.Color.White, 4), hanabi.deck.Card(hanabi.deck.Color.White, 5),
            hanabi.deck.Card(hanabi.deck.Color.Yellow, 1), hanabi.deck.Card(hanabi.deck.Color.Yellow, 2), hanabi.deck.Card(hanabi.deck.Color.Yellow, 3), hanabi.deck.Card(hanabi.deck.Color.Yellow, 4), hanabi.deck.Card(hanabi.deck.Color.Yellow, 5)] #attention au cas multicolore
            if game.piles[card.color]+1 >= card.number ]
        num_discardable = len(discardable)     

        # little piece of code to know whether a pile is dead or not
        completed_pile = []
        for color in list(hanabi.deck.Color):
            if hanabi.deck.Card(color, 5) in discardable:
                completed_pile.append(color)
        num_completed_pile = len(completed_pile)


        # 1 = play ; 2 = discard ; 3 = clue 
        #is it able to play anything succesfully?
        if num_playable > 0:
            action = 1
        #if blue coins are not restrictive and there is at least one unclued card, choose to clue
        if game.blue_coins>0 and num_unclued > 0:
            action = 3 
        
        #if there is at least one discardable card or if we cannot play and haven't any blue coin left
        if game.blue_coins == 0 : #no more blue coins
            action = 2
        
        if game.blue_coins == 8 :
            action = 3

        else:
            for (ind,card) in enumerate(game.current_hand.cards):
                if (ind+1,card.number) not in playable:
                    print ('Human would ragequit and discard:', "d%d"%(ind+1))
                    return "d%d"%(ind+1)
                else:
                    print ('Human would double-ragequit and discard this f****** first card')
                    return "d1"

        if action == 1:
            "play one playable card"
            card_to_play = random.randint(1, num_playable)
            ind = playable[card_to_play-1][0]
            print ('Human would play wisely:', "p%d"%ind)
            return "p%d"%ind

              
        if action == 2:
            "discard a discardable card"
            x = random.randint(1, num_discardable) #choose randomly between the discardable cards
            to_discard = discardable[x][0]
            print ('Human would discard: ', "d%d"%to_discard)
            return ("d%d"%to_discard)


        if action == 3:
            "clue"

            #if there isn't any useful clue to give, this case has already been avoided, you shouldn't be in this part of the code... stupid piece of sh**
            #if there is any dead or completed pile, give a color clue of this pile
            if num_completed_pile > 0:
                c = random.randint(1,num_completed_pile)
                clue = "c%s"%completed_pile[c]
                clue = clue[:2]
                print("Human would wisely clue: ")

            
            else : 
                if num_unclued == 0:
                    print ('Human would ragequit and clue: ', "c1") #action par défaut si cas critique
                    return ("c1")
                
                
                #choose randomly among the unclued cards
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
                print("Human would randomly clue: ", clue)
            return clue