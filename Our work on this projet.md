# Projet IN104 : Intelligence artificielle pour le jeu Hanabi

Ce projet à visée pédagogique avait pour buts l'acquisition de compétences en programmation et en gestion de projet:
* programmation orientée objet en Python
* prise en main d'un module préconçu par un autre programmeur
* extension de ce module et construction d'intelligence artificielle
* sensibilisation à la maintenabilité d'un code et à l'élaboration progressive de tests unitaires en cas de bugs
* initialisation à GitHub et ses fonctionnalités
* sensibilisation à l'utilisation de la syntaxe Markdown

## Ce que nous avons accompli pour ce projet

### Evaluation des performances d'une intelligence artificielle

Bien que ce travail ait été fait plus tard dans la chronologie du projet, il est important de le signaler maintenant car il nous a permis une analyse plus quantitative des performances de nos différentes intelligences artificielles.
Nous avons donc réalisé une étude statistique sommaire des performances de l'IA Cheater pour débuter notre programme comparatif. Sur un nombre N de parties (N de l'ordre de 10 000 pour avoir une estimation raisonnable), nous avons relevé :
* le meilleur score
* le score le plus faible
* le score moyen (moyenne arithmétique)
* la fréquence d'apparition d'un score parfait (25)
* la fréquence d'apparition d'un échec (score nul)
Ces cinq informations nous permettent de classer les IA entre elles et surtout de percevoir les points forts et points faibles de chacune. 
*Exemple 1 : Cheater réalise un score parfait 90% du temps et a un score moyen égal à 24,7. Nous pouvons donc nous demander pourquoi un tricheur ne peux pas s'assurer un score parfait systématiquement.* 
*Exemple 2 : Doit-on préférer une IA ayant un bon score moyen mais qui échoue souvent à une IA ayant un socre moyen plus faible mais qui n'échoue jamais?*

### Conception d'une IA aléatoire

Le but de cette partie était essentiellement de prendre en main le module de jeu hanabi et l'intelligence artificielle tricheuse (Cheater) qui nous était proposée comme modèle. Tout l'intérêt d'une IA aléatoire repose bien entendu sur l'*absence de stratégie* à implémenter : notre travail s'est ainsi concentré sur la **syntaxe** particulière qu'impliquait le module hanabi et sur l'écriture de **tests unitaires** nous permettant de vérifier le bon fonctionnement de notre IA.

Ainsi, nous avons commencé par lui faire choisir une action au hasard parmi "play", "discard" et "clue", puis un autre choix aléatoire s'effectuait pour déterminer la carte à jouer, défausser ou sur laquelle donner un indice.
A ce stade de la conception, le reste du groupe commentait les possibilités qui so'ffraient à nous pour pouvoir jouer à **plus de deux joueurs**. C'est pourquoi la phase de choix pour l'action "clue" s'est est trouvée compliquée.
Très rapidement, nous nous sommes rendues compte des exigences imposées par le module, qui pouvaient différer les règles du jeu hanabi à proprement parler. 
*Exemple : le module interdit à un joueur de se défausser d'une carte si l'équipe possède déjà 8 jetons bleus. Même si cette action n'est pas recommandée, elle n'est pas formellement interdite par les règles du jeu*
Nous avons donc fait évoluer cette IA afin qu'elle joue plutôt comme un enfant : elle connait les règles du jeu tel qu'il est implémenté dans le module et n'effectue pas une action qui ferait échouer la partie. Cependant, face à de multiples possibilités de jeu, elle est incapable de prioriser les actions et joue au hasard.

Nous pouvons résumer ses perfomances par le graphique suivant:
*à gauche les performances de notre IA Random - à droite, la comparaison avec l'IA Cheater*

### Conception d'une IA utilisant la stratégie de recommandation 
La stratégie utilisée par cette IA est décrite dans le document suivant: [HanSim : the Hat Guessing Strategy](https://sites.google.com/site/rmgpgrwc/research-papers/Hanabi_final.pdf?attredirects=1)

### Conception d'une IA utilisant la stratégie d'information
La stratégie utilisée par cette IA est décrite dans le document suivant: [HanSim : the Hat Guessing Strategy](https://sites.google.com/site/rmgpgrwc/research-papers/Hanabi_final.pdf?attredirects=1)
