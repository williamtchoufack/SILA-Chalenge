Poker william_X— Python POO

Simulateur de poker en ligne de commande.  
bibliothèque random uniquement.

---
Lancement
py main.py

Structure des fichiers

Jour5/
    ├── const.py     # Rangs, couleurs, valeurs, noms des mains
    ├── carte.py          # Classe Carte + affichage ASCII
    ├── chech.py           # Classe Deck (paquet de 52 cartes)
    ├── main_du_joueur.py    # Classe Main (cartes privées d'un joueur)
    ├── test_eval.py     # Détection des combinaisons (paire, quinte, flush...)
    ├── monte_carlo.py    # Calcul des probabilités de gain par simulation
    ├── joueur.py         # Classe Joueur (humain et bot)
    ├── partie.py            # Moteur de jeu (manches, tours de mises, showdown)
    └── main.py           # Point d'entrée

Fonctionnalités

- Partie contre 1 à 4 bots
- Affichage ASCII des cartes dans le terminal
- Tours de mises : suivre, relancer, se coucher
- Blinds, flop, turn, river, showdown
- Évaluation automatique des mains (10 combinaisons)
- Probabilités de gain calculées par simulation Monte Carlo à chaque tour

Combinaisons reconnues

| Rang | Nom                  |
|------|----------------------|
| 9    | Quinte Flush Royale  |
| 8    | Quinte Flush         |
| 7    | Carré                |
| 6    | Full House           |
| 5    | Couleur              |
| 4    | Quinte               |
| 3    | Brelan               |
| 2    | Double Paire         |
| 1    | Paire                |
| 0    | Carte Haute          |
