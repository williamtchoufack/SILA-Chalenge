class Main:
    def __init__(self):
        self.cartes = []

    def recevoir(self, carte):
        self.cartes.append(carte)

    def vider(self):
        self.cartes = []

    def __str__(self):
        return str(self.cartes)