import random

from const import RANGS, COULEURS
from carte import Carte
from main_du_joueur import Main
from test_eval import meilleure_main


def monte_carlo(main_joueur, board, nb_adversaires, nb_simul=3000):
    victoires = 0
    egalites  = 0
    defaites  = 0
    connues   = main_joueur.cartes + board

    for _ in range(nb_simul):
        deck_sim = [Carte(r, c) for c in COULEURS for r in RANGS]
        deck_sim = [c for c in deck_sim if c not in connues]
        random.shuffle(deck_sim)

        ptr = 0
        board_sim = board[:]
        while len(board_sim) < 5:
            board_sim.append(deck_sim[ptr])
            ptr += 1

        mains_adv = []
        ok = True
        for _ in range(nb_adversaires):
            if ptr + 2 > len(deck_sim):
                ok = False
                break
            m = Main()
            m.recevoir(deck_sim[ptr])
            m.recevoir(deck_sim[ptr+1])
            ptr += 2
            mains_adv.append(m)

        if not ok:
            continue

        score_j = meilleure_main(main_joueur.cartes + board_sim)
        gagne   = True
        egal    = True

        for adv in mains_adv:
            score_a = meilleure_main(adv.cartes + board_sim)
            if score_a > score_j:
                gagne = False
                egal  = False
                break
            elif score_a != score_j:
                egal = False

        if gagne and egal:
            egalites += 1
        elif gagne:
            victoires += 1
        else:
            defaites += 1

    total = victoires + egalites + defaites
    if total == 0:
        return {'victoires': 0, 'egalites': 0, 'defaites': 0}

    return {
        'victoires': round(victoires / total * 100, 1),
        'egalites':  round(egalites  / total * 100, 1),
        'defaites':  round(defaites  / total * 100, 1)
    }