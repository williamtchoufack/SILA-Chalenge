import json
from datetime import datetime


class Compte:

    def __init__(self, numero, nom, solde=0):
        self.numero = numero
        self.nom = nom
        self.solde = solde
        self.historique = []

    def ajouter_historique(self, msg):
        maintenant = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.historique.append(maintenant + " - " + msg)

    def deposer(self, montant):
        self.solde = self.solde + montant
        self.ajouter_historique("depot : +" + str(montant))
        print("depot ok, nouveau solde :", self.solde)

    def retirer(self, montant):
        if self.solde < montant:
            print("erreur : pas assez d'argent")
            return False
        self.solde = self.solde - montant
        self.ajouter_historique("retrait : -" + str(montant))
        print("retrait ok, nouveau solde :", self.solde)
        return True

    def virement(self, cible, montant):
        if self.solde < montant:
            print("erreur : solde insuffisant pour faire le virement")
            return False
        self.solde = self.solde - montant
        cible.solde = cible.solde + montant
        self.ajouter_historique("virement envoye a " + cible.nom + " : " + str(montant))
        cible.ajouter_historique("virement recu de " + self.nom + " : " + str(montant))
        print("virement ok")
        return True

    def afficher(self):
        print("\n--- Compte de", self.nom, "---")
        print("solde :", self.solde)
        print("historique :")
        for op in self.historique:
            print("  -", op)


# compte epargne : retrait maximum 1000
class CompteEpargne(Compte):

    def retirer(self, montant):
        if montant > 1000:
            print("erreur : sur un compte epargne on peut pas retirer plus de 1000")
            return False
        # sinon on fait le retrait normal
        Compte.retirer(self, montant)


# compte pro : virement maximum 5000
class ComptePro(Compte):

    def virement(self, cible, montant):
        if montant > 5000:
            print("erreur : virement max autorise est 5000 sur un compte pro")
            return False
        Compte.virement(self, cible, montant)


# sauvegarder dans un fichier
def sauvegarder(liste_comptes):
    data = []
    for c in liste_comptes:
        data.append({
            "numero" : c.numero,
            "nom"    : c.nom,
            "solde"  : c.solde,
            "histo"  : c.historique,
            "type"   : type(c).__name__
        })
    f = open("banque.json", "w", encoding="utf-8")
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.close()
    print("\nsauvegarde ok !")


# charger depuis le fichier
def charger():
    liste_comptes = []
    try:
        f = open("banque.json", "r", encoding="utf-8")
        data = json.load(f)
        f.close()
        for d in data:
            if d["type"] == "CompteEpargne":
                c = CompteEpargne(d["numero"], d["nom"], d["solde"])
            elif d["type"] == "ComptePro":
                c = ComptePro(d["numero"], d["nom"], d["solde"])
            else:
                c = Compte(d["numero"], d["nom"], d["solde"])
            c.historique = d["histo"]
            liste_comptes.append(c)
        print("chargement ok !")
    except:
        print("pas de fichier trouve, on repart de zero")
    return liste_comptes


# --- test ---

c1 = CompteEpargne("001", "Alice", 2000)
c2 = ComptePro("002", "Bob", 3000)

c1.deposer(500)
c1.retirer(200)
c1.virement(c2, 300)

# test des erreurs
print("\n-- test retrait trop grand --")
c1.retirer(9999)

print("\n-- test virement sans assez d'argent --")
c1.virement(c2, 999999)

c1.afficher()
c2.afficher()

sauvegarder([c1, c2])
