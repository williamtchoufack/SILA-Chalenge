import random

from const import RANGS, COULEURS
from carte import Carte


class Deck:
    def __init__(self):
        self.cartes = [Carte(r, c) for c in COULEURS for r in RANGS]
        random.shuffle(self.cartes)

    def piocher(self):
        return self.cartes.pop(0)

    def retirer(self, carte):
        for i in range(len(self.cartes)):
            if self.cartes[i] == carte:
                self.cartes.pop(i)
                return

    def taille(self):
        return len(self.cartes)