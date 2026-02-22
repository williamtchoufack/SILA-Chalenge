import random

from main_du_joueur import Main
from test_eval import meilleure_main


class Joueur:
    def __init__(self, nom, jetons=1000, bot=False):
        self.nom       = nom
        self.jetons    = jetons
        self.bot       = bot
        self.main      = Main()
        self.couche    = False
        self.mise_tour = 0

    def reset(self):
        self.main.vider()
        self.couche    = False
        self.mise_tour = 0

    def miser(self, montant):
        montant = min(montant, self.jetons)
        self.jetons    -= montant
        self.mise_tour += montant
        return montant

    def action_bot(self, a_suivre, pot, board):
        toutes = self.main.cartes + board
        if toutes:
            score = meilleure_main(toutes)
            force = score[0]
        else:
            force = 0

        if force >= 6:
            relance = min(pot, self.jetons)
            return 'raise', max(relance, a_suivre * 3)
        elif force >= 4:
            if random.random() < 0.6:
                return 'raise', max(a_suivre * 2, pot // 3)
            return 'call', a_suivre
        elif force >= 2:
            if a_suivre == 0:
                return 'check', 0
            if a_suivre <= self.jetons // 4:
                return 'call', a_suivre
            return 'fold', 0
        else:
            if a_suivre == 0:
                return 'check', 0
            if random.random() < 0.1:
                return 'raise', a_suivre
            if a_suivre <= self.jetons // 8:
                return 'call', a_suivre
            return 'fold', 0

    def __str__(self):
        return self.nom + " (" + str(self.jetons) + " jetons)"