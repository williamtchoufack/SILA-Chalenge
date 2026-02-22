from const import VALEUR, SYMBOLE


class Carte:
    def __init__(self, rang, couleur):
        self.rang    = rang
        self.couleur = couleur
        self.valeur  = VALEUR[rang]

    def __str__(self):
        return self.rang + ' ' + self.couleur

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.rang == other.rang and self.couleur == other.couleur

    def afficher(self):
        s  = SYMBOLE[self.couleur]
        r  = self.rang.ljust(2)
        rr = self.rang.rjust(2)
        print("+-------+")
        print("| " + r + "    |")
        print("|       |")
        print("|   " + s + "   |")
        print("|       |")
        print("|    " + rr + " |")
        print("+-------+")


def afficher_cartes(liste):
    if not liste:
        return
    lignes = []
    for carte in liste:
        s  = SYMBOLE[carte.couleur]
        r  = carte.rang.ljust(2)
        rr = carte.rang.rjust(2)
        lignes.append([
            "+-------+",
            "| " + r + "    |",
            "|       |",
            "|   " + s + "   |",
            "|       |",
            "|    " + rr + " |",
            "+-------+"
        ])
    for row in range(7):
        print("  ".join(l[row] for l in lignes))
    print()