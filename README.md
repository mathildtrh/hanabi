# Camille, Ruonan and Mathilde's Hanabi project

This project is for educational purposes: 
its current status represents the student's work until May, 24th, 2019.

# Hanabi module

A python3 module that knows Hanabi:

* card deck and dealer,
* CLI (command line interface), lets you play and verifies that your moves are allowed (currently limited to 2 players),
* GUI (to do),
* AI (currently six different AI, but they do not necesseraly work well).
  * Cheater, which was already available when we started the project
  * Random, which plays quite randomly like a human who would discover this game
  * Human, which doesn't work (should be an improvement of Random)
  * two different versions of Recom, an IA which uses a recommandation strategy
  * Strat_info, which doesn't work (should use a information strategy)


## Suggested tasks and installation of the module

See the [README_STARTING_POINT](https://github.com/mathildtrh/hanabi/blob/master/README_STARTING_POINT.md)


## Completed tasks

There are many possible tasks:

- [x] read the current state of the module, 
  - [x] complete its documentation when needed,
  - [x] share with everyone this improvement,

- [x] add AIs. Some suggestions:
  - [x] RandomAI (plays randomly)
  - [x] HansimAI (both strategies)
  - [x] train a machine learning (I'm not sure if this will give anything interesting without powerful CPU/GPU resources)
  - [x] design your own, by progressively improving the Random one

- [x] we kept track of scores and compared our different AIs : you will find the results [here](https://github.com/mathildtrh/hanabi/blob/master/rapport/Report.md)


- [x] make it workable for up to 5 players : hanabi module is workable for 2, 3, 4 and 5 players, thanks to the contributions of the whole group. We also made Cheater, Random and Recom able to play with 2, 3, 4 or 5 players.


## Improvements to come

- [ ] improve the CheaterAI : we chose instead to develop new AIs but it could be interesting to achieve a perfect score 100% of the time, or understanf why this is not possible.
- [ ] make it workable from two separate screens : it would have been fun to be able to play with our friends or with our AIs.
- [ ] design a GUI that looks like a real *professional* game (for the moment, you only have some colored ascii art on your terminal).
- [ ] make all our AIs able to play, in particular the one with a information strategy because it has great chances of making high scores more frequently than the other AIS we developped.

## Bibliography

### Other Hanabi projects

* [A C++ bot: some strategies and success rates](https://github.com/Quuxplusone/Hanabi)
* [HanSim: the Hat guessing strategy](https://d0474d97-a-62cb3a1a-s-sites.googlegroups.com/site/rmgpgrwc/research-papers/Hanabi_final.pdf?attachauth=ANoY7cp_mjjD7lCb5HFxBphRWpSkE8SabM7PiOVWFwcNKSnpxENRLwTsQEgDMC6PIHuBmzP4oixvH_B8PZQmrHDyfA-ZLSKWb-Lx1WJNIUKUoxV1w0K0bWXelLPCi5MbXaByoVcukH4CEg-5N_iJP7mKSDHiV5ImwGDBCwQoT4mwvppVyA0BVb2Lhr-mGYFtUw3uBlds77azk5RjFZHGvAtvx6idYLvunLLj6BStHWHrNovX8p5KGFk%3D&attredirects=0)
* [HanSim: source code](https://github.com/rjtobin/HanSim)
* [boardgame arena](https://fr.boardgamearena.com/#!gamepanel?game=hanabi)
* [hanabi conventions (hanabi-live)](https://github.com/Zamiell/hanabi-conventions), and references therein.


### AI

* [deepmind: Atari](https://arxiv.org/pdf/1312.5602v1.pdf)
* [deepmind: SC2](https://arxiv.org/abs/1708.04782)
* [deepmind: Hanabi](https://arxiv.org/abs/1902.00506)
* todo: find non-deepmind references?



### Misc (coding principles, project, ...)

* [keep it simple](https://en.wikipedia.org/wiki/KISS_principle)
* [rule of least surprise](http://www.catb.org/esr/writings/taoup/), [catbaz](http://www.catb.org/esr/writings/cathedral-bazaar/)
* [rubber duck debugging](https://en.wikipedia.org/wiki/Rubber_duck_debugging)
* [markdown (overview)](https://guides.github.com/features/mastering-markdown/), [markdown (in details)](https://github.github.com/gfm/)
* [BGA state machine](https://www.slideshare.net/boardgamearena/bga-studio-focus-on-bga-game-state-machine)

## Note for our teacher

* Pour lancer les parties sur nos deux IA opérationnelles : 
    ```
    make module
    python3 play_a_game.py
    ```
    - suivre les instructions : ce fichier permet de choisir entre les deux IA développées (Random ou Recom), de choisir le nombre de joueurs, permet de faire jouer une partie entière à l'IA, ou de la faire jouer tour par tour.



* Pour afficher les stats : 
    - décommenter les deux lignes suivantes (redéfinit la fonction print pour éviter l'affichage des 1000 parties) : 
    ```
    def print(*args, **kwargs):
        pass 
    ```
    - en tête des fichiers suivants :
        - deck.py
        - ai.py
        - ai_recommandation_strategy.py
        - ai_recom.py

 
    - Modifier dans *hanabi/test/script_comparison.py* le nombre de joueurs (par défaut à 5) 
    ```
    make module
    python3 test/script_comparison.py
    ```
    - Donne 4 figures : AI de Recommandation, AI Random et AI Cheater puis un graphe qui superpose les résultats.



