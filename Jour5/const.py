RANGS    = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
COULEURS = ['Coeur','Carreau','Trefle','Pique']
VALEUR   = {r: i+2 for i, r in enumerate(RANGS)}
SYMBOLE  = {'Coeur':'v', 'Carreau':'^', 'Trefle':'#', 'Pique':'S'}

NOMS_MAINS = [
    'Carte Haute', 'Paire', 'Double Paire', 'Brelan',
    'Quinte', 'Couleur', 'Full House', 'Carre',
    'Quinte Flush', 'Quinte Flush Royale'
]