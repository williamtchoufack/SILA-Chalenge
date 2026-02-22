from const import NOMS_MAINS
from carte import afficher_cartes
from check import Deck
from test_eval import meilleure_main
from monte_carlo import monte_carlo


class Jeu:
    def __init__(self, joueurs):
        self.joueurs = joueurs
        self.deck    = Deck()
        self.board   = []
        self.pot     = 0
        self.bouton  = 0
        self.pb      = 10
        self.gb      = 20

    def humain(self):
        for j in self.joueurs:
            if not j.bot:
                return j
        return None

    def distribuer(self):
        self.deck  = Deck()
        self.board = []
        self.pot   = 0
        for j in self.joueurs:
            j.reset()
            j.main.recevoir(self.deck.piocher())
            j.main.recevoir(self.deck.piocher())

    def blinds(self):
        actifs = [j for j in self.joueurs if j.jetons > 0]
        sb = actifs[(self.bouton + 1) % len(actifs)]
        bb = actifs[(self.bouton + 2) % len(actifs)]
        self.pot += sb.miser(self.pb)
        self.pot += bb.miser(self.gb)
        print(sb.nom + " paie la petite blind :", self.pb)
        print(bb.nom + " paie la grande blind :", self.gb)

    def afficher_etat(self):
        print("\n" + "="*50)
        print("POT :", self.pot, "jetons")
        print("="*50)
        print("\nJOUEURS :")
        for j in self.joueurs:
            statut = " [COUCHE]" if j.couche else ""
            print(" -", j.nom, ":", j.jetons, "jetons" + statut)
        if self.board:
            print("\nTABLE :")
            afficher_cartes(self.board)

    def lire_choix(self, options):
        while True:
            rep = input("Votre choix " + str(options) + " : ").strip()
            if rep in options:
                return rep
            print("Choix invalide.")

    def tour_de_mises(self, h, mise_min=0):
        actifs = [j for j in self.joueurs if not j.couche]
        if len(actifs) <= 1:
            return True

        mise_courante = mise_min
        file    = actifs[:]
        dernier = None
        i = 0

        while i < len(file):
            j = file[i]
            if j.couche:
                i += 1
                continue
            if j == dernier:
                break

            a_suivre = mise_courante - j.mise_tour

            if not j.bot:
                self.afficher_etat()
                print("\nVOTRE MAIN :")
                afficher_cartes(j.main.cartes)

                print("Calcul Monte Carlo en cours...")
                p = monte_carlo(j.main, self.board, len(self.joueurs)-1, 2000)
                print("Victoire:", p['victoires'], "%  Egalite:", p['egalites'], "%  Defaite:", p['defaites'], "%")

                if a_suivre > 0:
                    print("\nMise a suivre :", a_suivre, "| Vos jetons :", j.jetons)
                    print("[1] Suivre  [2] Relancer  [3] Se coucher")
                else:
                    print("\nVos jetons :", j.jetons)
                    print("[1] Parole  [2] Miser  [3] Se coucher")

                choix = self.lire_choix(['1','2','3'])

                if choix == '1':
                    if a_suivre > 0:
                        self.pot += j.miser(a_suivre)
                        print("Vous suivez.")
                    else:
                        print("Parole.")
                elif choix == '2':
                    try:
                        montant = int(input("Montant : "))
                        montant = max(montant, a_suivre + self.gb)
                        self.pot += j.miser(montant)
                        mise_courante = j.mise_tour
                        dernier = j
                        print("Vous relancez a", mise_courante)
                    except ValueError:
                        print("Entree invalide, parole.")
                else:
                    j.couche = True
                    print("Vous vous couchez.")

            else:
                action, montant = j.action_bot(a_suivre, self.pot, self.board)
                if action == 'fold':
                    j.couche = True
                    print(j.nom, ": se couche")
                elif action == 'call':
                    if a_suivre > 0:
                        self.pot += j.miser(a_suivre)
                        print(j.nom, ": suit")
                    else:
                        print(j.nom, ": parole")
                elif action == 'raise':
                    montant = min(max(montant, a_suivre + self.gb), j.jetons)
                    self.pot += j.miser(montant)
                    mise_courante = j.mise_tour
                    dernier = j
                    print(j.nom, ": relance a", mise_courante)
                else:
                    print(j.nom, ": parole")

            i += 1
            if i >= len(file) and dernier is not None:
                reste = [x for x in file if not x.couche and x != dernier and x.mise_tour < mise_courante]
                if reste:
                    file    = reste
                    i       = 0
                    dernier = None

        for j in self.joueurs:
            j.mise_tour = 0

        return sum(1 for j in self.joueurs if not j.couche) > 1

    def gagnants(self):
        actifs = [j for j in self.joueurs if not j.couche]
        if len(actifs) == 1:
            return actifs
        meilleur = None
        result   = []
        for j in actifs:
            score = meilleure_main(j.main.cartes + self.board)
            if meilleur is None or score > meilleur:
                meilleur = score
                result   = [j]
            elif score == meilleur:
                result.append(j)
        return result

    def showdown(self, h):
        print("\n--- SHOWDOWN ---")
        for j in [x for x in self.joueurs if not x.couche]:
            score    = meilleure_main(j.main.cartes + self.board)
            nom_main = NOMS_MAINS[score[0]]
            print(j.nom, "->", nom_main)
            afficher_cartes(j.main.cartes)

    def fin_manche(self, h):
        gagnants = self.gagnants()
        gain     = self.pot // len(gagnants)
        print("\n--- RESULTAT ---")
        for g in gagnants:
            g.jetons += gain
            if g == h:
                print("LA VICTOIRE VOUS REVIENT", gain, "jetons !")
            else:
                score = meilleure_main(g.main.cartes + self.board)
                print(g.nom, "gagne", gain, "jetons avec", NOMS_MAINS[score[0]])
        self.bouton = (self.bouton + 1) % len(self.joueurs)

    def jouer_manche(self):
        h = self.humain()
        self.distribuer()
        print("\n" + "="*50)
        print("NOUVELLE MANCHE")
        print("="*50)
        self.blinds()

        print("\n--- PRE-FLOP ---")
        if not self.tour_de_mises(h, self.gb):
            self.fin_manche(h)
            return

        print("\n--- FLOP ---")
        for _ in range(3):
            self.board.append(self.deck.piocher())
        if not self.tour_de_mises(h):
            self.fin_manche(h)
            return

        print("\n--- TURN ---")
        self.board.append(self.deck.piocher())
        if not self.tour_de_mises(h):
            self.fin_manche(h)
            return

        print("\n--- RIVER ---")
        self.board.append(self.deck.piocher())
        self.tour_de_mises(h)

        actifs = [j for j in self.joueurs if not j.couche]
        if len(actifs) > 1:
            self.showdown(h)

        self.fin_manche(h)

    def jouer(self):
        h = self.humain()
        print("="*50)
        print("  POKER By WILLIAM_TCHOUFACK ")
        print("  Joueurs :", [str(j) for j in self.joueurs])
        print("="*50)
        input("Appuyez sur Entree pour commencer...")

        while len(self.joueurs) > 1:
            if h not in self.joueurs:
                print("Vous etes elimine. Game over😭.")
                break

            self.jouer_manche()
            self.joueurs = [j for j in self.joueurs if j.jetons > 0]

            if len(self.joueurs) == 1:
                print("\n" + self.joueurs[0].nom + " remporte la partie !🔥🔥🔥🔥🔥🔥🔥🔥🔥")
                break

            if h in self.joueurs:
                rep = input("\nContinuer ? (o/n) : ").strip().lower()
                if rep == 'n':
                    print("Partie terminee. Vos jetons :", h.jetons)
                    break