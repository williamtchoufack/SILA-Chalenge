from joueur import Joueur
from partie  import Jeu


def main():
    print("Combien de bots ? (1 a 4)")
    try:
        nb_bots = int(input("> "))
        nb_bots = max(1, min(4, nb_bots))
    except ValueError:
        nb_bots = 2

    nom = input("Votre nom : ").strip()
    if nom == '':
        nom = "Joueur"

    noms_bots = ["Erudi_X☠️", "Sudo👽", "CAROLE😂😂", "Lydianna🤣🤣🤣"]
    joueurs   = [Joueur(nom, 1000, bot=False)]
    for i in range(nb_bots):
        joueurs.append(Joueur(noms_bots[i], 1000, bot=True))

    jeu = Jeu(joueurs)
    jeu.jouer()


main()
