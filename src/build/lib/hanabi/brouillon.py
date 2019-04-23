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


            ## other version
                    switch (nb_players)
            case 2:
                how_to_clue = {
                    0 : "c1",
                    1 : "c2",
                    2 : "c3",
                    3 : "c4",
                    4 : "c5",
                    5 : "cr",
                    6 : "cb",
                    7 : "cg",
                    8 : "cy",
                    9 : "cw"
                }

            case 3: #demands an extension of the way of giving clues : the 3rd char should be the number of the player who receives the clue
                how_to_clue = {
                    0 : "c11",
                    1 : "c12",
                    2 : "c21",
                    3 : ("c31", "c41", "c51"),
                    4 : ("c22", "c32", "c42", "c52"),
                    5 : "cr1",
                    6 : "cr2",
                    7 : "cb1",
                    8 : ("cg1", "cy1", "cw1"),
                    9 : ("cb2", "cg2", "cy2", "cw2")
                }

            case 4:
                how_to_clue = {
                    0 : "c11",
                    1 : ("c21", "c31", "c41", "c51"),
                    2 : ("c12", "c22", "c32", "c42", "c52"),
                    3 : ("c13", "c23", "c33", "c43", "c53"),
                    #4 : (),
                    5 : "cr1",
                    6 : ("cb1", "cg1", "cy1", "cw1"),
                    7 : ("cr1", "cb2", "cg2", "cy2", "cw2"),
                    8 : ("cr3", "cb3", "cg3", "cy3", "cw3")
                    #9 : ()
                }

            case 5:
                how_to_clue = {
                    0 : ("c11", "c21", "c31", "c41", "c51"),
                    1 : ("c12", "c22", "c32", "c42", "c52"),
                    2 : ("c13", "c23", "c33", "c43", "c53"),
                    3 : ("c14", "c24", "c34", "c44", "c54")
                    #4 : (),
                    5 : ("cr1", "cb1", "cg1", "cy1", "cw1"),
                    6 : ("cr1", "cb2", "cg2", "cy2", "cw2"),
                    7 : ("cr3", "cb3", "cg3", "cy3", "cw3"),
                    8 : ("cr4", "cb4", "cg4", "cy4", "cw4")
                    #9 : ()
                }
