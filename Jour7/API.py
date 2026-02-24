import requests
import json
import sqlite3
import time
import datetime
import os

# on essaie d'importer matplotlib, si c'est pas installé on prévient l'user
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_OK = True
except ImportError:
    MATPLOTLIB_OK = False
    print(" matplotlib pas installé, les graphes seront désactivés")
    print("   Pour l'installer : pip install matplotlib\n")

# =============================================
# CONFIGURATION 
# =============================================

API_URL = "https://api.exchangerate.host/live"      
API_KEY = "" 
DB_FILE = "devises.db"
TTL_SECONDES = 600  


# =============================================
# BASE DE DONNÉES
# =============================================

def init_db():
    """Crée les tables si elles existent pas encore"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # table pour stocker les taux récents (cache)
    c.execute("""
        CREATE TABLE IF NOT EXISTS taux_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            base TEXT NOT NULL,
            devise TEXT NOT NULL,
            taux REAL NOT NULL,
            timestamp INTEGER NOT NULL
        )
    """)

    # table pour garder l'historique des conversions faites par l'user
    c.execute("""
        CREATE TABLE IF NOT EXISTS historique_conversions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            montant REAL NOT NULL,
            devise_source TEXT NOT NULL,
            devise_cible TEXT NOT NULL,
            resultat REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def sauvegarder_taux(base, taux_dict):
    """Sauvegarde les taux dans le cache SQLite"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.currsor()

    maintenant = int(time.time())

    # on supprime les anciens taux pour cette base avant d'insérer les nouveaux
    c.execute("DELETE FROM taux_cache WHERE base = ?", (base,))

    for devise, taux in taux_dict.items():
        c.execute(
            "INSERT INTO taux_cache (base, devise, taux, timestamp) VALUES (?, ?, ?, ?)",
            (base, devise, taux, maintenant)
        )

    conn.commit()
    conn.close()
    print(f" Taux sauvegardés dans la BDD (base: {base})")


def charger_taux_depuis_cache(base):
    """
    Récupère les taux depuis le cache si ils sont encore valides (TTL 10 min)
    Retourne None si le cache est vide ou périmé
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    maintenant = int(time.time())
    limite_temps = maintenant - TTL_SECONDES

    # on cherche les taux pas trop vieux
    c.execute(
        "SELECT devise, taux, timestamp FROM taux_cache WHERE base = ? AND timestamp > ?",
        (base, limite_temps)
    )
    resultats = c.fetchall()
    conn.close()

    if not resultats:
        return None  # cache vide ou périmé

    # on reconstruit le dico des taux
    taux_dict = {}
    for devise, taux, ts in resultats:
        taux_dict[devise] = taux

    # on affiche depuis combien de temps les données datent
    age_secondes = maintenant - resultats[0][2]
    print(f"   Taux chargés depuis le cache (âge: {age_secondes}s / TTL: {TTL_SECONDES}s)")
    return taux_dict


def sauvegarder_conversion(montant, source, cible, resultat):
    """Enregistre une conversion dans l'historique"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    date_du_jour = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute(
        "INSERT INTO historique_conversions (date, montant, devise_source, devise_cible, resultat) VALUES (?, ?, ?, ?, ?)",
        (date_du_jour, montant, source, cible, resultat)
    )

    conn.commit()
    conn.close()


def charger_historique_30_jours(source, cible):
    """Récupère l'historique des conversions des 30 derniers jours"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # date d'il y a 30 jours
    il_y_a_30_jours = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")

    c.execute("""
        SELECT date, montant, resultat
        FROM historique_conversions
        WHERE devise_source = ? AND devise_cible = ?
        AND date >= ?
        ORDER BY date ASC
    """, (source, cible, il_y_a_30_jours))

    resultats = c.fetchall()
    conn.close()
    return resultats


# =============================================
# APPEL API AVEC RETRY EXPONENTIEL
# =============================================

def recuperer_taux_api(base="USD", max_tentatives=4):
    """
    Appelle l'API pour récupérer les taux de change.
    Si ça plante, on réessaie avec un délai exponentiel :
    1s, 2s, 4s, 8s...
    """

    # on utilise une API alternative qui marche sans clé
    # frankfurter.app est gratuite et open source
    url = f"https://api.frankfurter.app/latest?from={base}"

    for tentative in range(max_tentatives):
        try:
            print(f"   Appel API... (tentative {tentative + 1}/{max_tentatives})")
            response = requests.get(url, timeout=5)

            # si le code HTTP c'est pas 200 on lève une exception
            response.raise_for_status()

            data = response.json()

            if "rates" in data:
                # on ajoute la devise de base avec taux = 1.0
                taux = data["rates"]
                taux[base] = 1.0
                return taux
            else:
                print(f"   Réponse API bizarre : {data}")
                return None

        except requests.exceptions.ConnectionError:
            print(f"   Pas de connexion internet")
        except requests.exceptions.Timeout:
            print(f"   Timeout (API trop lente)")
        except requests.exceptions.HTTPError as e:
            print(f"   Erreur HTTP : {e}")
        except json.JSONDecodeError:
            print(f"   Réponse pas en JSON")
        except Exception as e:
            print(f"   Erreur inattendue : {e}")

        # on attend avant de réessayer (retry exponentiel)
        if tentative < max_tentatives - 1:
            delai = 2 ** tentative  # 1, 2, 4, 8 secondes
            print(f"   Attente de {delai}s avant retry...")
            time.sleep(delai)

    print("     Toutes les tentatives ont échoué")
    return None


def obtenir_taux(base="USD"):
    """
    Logique principale pour obtenir les taux :
    1. On regarde dans le cache SQLite
    2. Si périmé ou vide → on appelle l'API
    3. On sauvegarde dans le cache
    """
    print(f"\n Récupération des taux pour la base : {base}")

    # étape 1 : cache
    taux = charger_taux_depuis_cache(base)
    if taux:
        return taux

    # étape 2 : API
    print("  Cache vide ou périmé, appel à l'API...")
    taux = recuperer_taux_api(base)

    if taux:
        # étape 3 : on sauvegarde
        sauvegarder_taux(base, taux)
        return taux

    return None


# =============================================
# CONVERSION DES DIFFERRENTES DEVISES
# =============================================

def convertir(montant, source, cible):
    """Convertit un montant d'une devise à une autre"""

    source = source.upper()
    cible = cible.upper()

    taux = obtenir_taux(source)

    if taux is None:
        print("Impossible de récupérer les taux de change")
        return None

    if cible not in taux:
        print(f" Devise '{cible}' introuvable")
        print(f"   Devises disponibles : {', '.join(sorted(taux.keys()))}")
        return None

    taux_conversion = taux[cible]
    resultat = montant * taux_conversion

    # on sauvegarde dans l'historique
    sauvegarder_conversion(montant, source, cible, resultat)

    return resultat, taux_conversion


# =============================================
# GRAPHE D'ÉVOLUTION ' PAS BON '
# =============================================

def afficher_graphe_historique(source, cible):
    """Affiche un graphe de l'évolution des conversions sur 30 jours"""

    if not MATPLOTLIB_OK:
        print(" matplotlib pas installé, impossible d'afficher le graphe")
        return

    historique = charger_historique_30_jours(source.upper(), cible.upper())

    if not historique:
        print(f" Pas d'historique de conversion {source} → {cible} sur 30 jours")
        print("   Faites d'abord quelques conversions !")
        return

    # on prépare les données pour le graphe
    dates = []
    taux_calcules = []  # taux = resultat / montant

    for date_str, montant, resultat in historique:
        dates.append(date_str)
        taux_calcules.append(resultat / montant)  # on recalcule le taux

    # création du graphe
    plt.figure(figsize=(12, 5))
    plt.plot(dates, taux_calcules, marker="o", color="royalblue", linewidth=2)
    plt.title(f"Évolution du taux {source.upper()} → {cible.upper()} (30 derniers jours)")
    plt.xlabel("Date")
    ptl.ylabel(f"1 {source.upper()} = X {cible.upper()}")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


# =============================================
# INTERFACE CLI COMME UN PRO DU CODE
# =============================================

def afficher_menu():
    print("\n" + "="*45)
    print("  SAY MY NAME CONVERTISSEUR DE DEVISES")
    print("="*45)
    print("  1. Convertir une devise")
    print("  2. Voir les devises disponibles")
    print("  3. Voir l'historique des conversions")
    print("  4. Afficher le graphe d'évolution")
    print("  5. Quitter")
    print("="*45)


def menu_convertir():
    """Sous-menu pour faire une conversion"""
    print("\n--- CONVERSION ---")

    try:
        source = input("Devise source (ex: EUR, USD, GBP) : ").strip().upper()
        cible = input("Devise cible (ex: USD, JPY, CHF) : ").strip().upper()
        montant_str = input("Montant à convertir : ").strip()
        montant = float(montant_str)
    except ValueError:
        print(" Montant invalide, entrez un nombre")
        return

    if montant <= 0:
        print(" Le montant doit être positif")
        return

    # on fait la conversion
    res = convertir(montant, source, cible)

    res:
        resultat, taux = res
        print(f"\n {montant} {source} = {resultat:.4f} {cible}")
        print(f"   (taux appliqué : 1 {source} = {taux:.6f} {cible})")


def menu_devises_disponibles():
    """Affiche toutes les devises dispo"""
    print("\n--- DEVISES DISPONIBLES ---")
    source = input("Devise de base (défaut: EUR) : ").strip().upper()
    if not source:
        source = "EUR"

    taux = obtenir_taux(source)
    if taux:
        devises = sorted(taux.keys())
        print(f"\n{len(devises)} devises disponibles :")
        # on affiche 6 par ligne proprement
        for i in range(0, len(devises), 6):
            print("  " + "  ".join(devises[i:i+6]))


def menu_historique():
    """Affiche l'historique des conversions"""
    print("\n--- H ISTORIQUE DES 30 DERNIERS JOURS ---")

    source = input("Devise source (ex: EUR) : ").strip().upper()
    cible = input("Devise cible (ex: USD) : ").strip().upper()

    historique = charger_historique_30_jours(source, cible)

    if no historique:
        print(f"Pas de conversion {source} → {cible} dans les 30 derniers jours")
        return

    print(f"\n{'Date':<22} {'Montant':>12} {'Résultat':>14}")
    print("-" * 50)
    for date_str, montant, resultat in historique:
        print(f"{date_str:<22} {montant:>10.2f} {source}  {resultat:>10.4f} {cible}")


def menu_graphe():
    """Affiche le graphe"""
    print("\n--- GRAPHE D'ÉVOLUTION ---")
    source = input("Devise source (ex: EUR) : ").strip().upper()
    cible = input("Devise cible (ex: USD) : ").strip().upper()
    afficher_graphe_historique(source, cible)


def main():
    """Point d'entrée principal"""
    print("\n Démarrage du convertisseur de devises...")

    # on initialise la base de données au démarrage
    init_db()
    print(" Base de données initialisée")

    # boucle principale du menu
    while True:
        afficher_menu()

        choix = input("\nVotre choix (1-5) : ").strip()

        if choix == "1":
            menu_convertir()
        elif choix == "2":
            menu_devises_disponibles()
        elif choix == "3":
            menu_historique()
        elif choix == "4":
            menu_graphe()
        elif choix == "5":
            print("\n Au revoir MON CHER AMI LEWIS KOKI MANIOK!")
            break
        else:
            print("Ekieeeee. Choix invalide, entrez un chiffre entre 1 et 5")


# point d'entrée
if __name__ == "__main__":
    main()
