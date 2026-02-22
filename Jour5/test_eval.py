def compter(valeurs):
    freq = {}
    for v in valeurs:
        if v in freq:
            freq[v] += 1
        else:
            freq[v] = 1
    return freq


def evaluer_main(cartes):
    valeurs  = sorted([c.valeur for c in cartes], reverse=True)
    couleurs = [c.couleur for c in cartes]
    freq     = compter(valeurs)

    is_flush = len(set(couleurs)) == 1
    is_suite = (valeurs == list(range(valeurs[0], valeurs[0]-5, -1)))

    if not is_suite and set(valeurs) == {14, 2, 3, 4, 5}:
        is_suite = True
        valeurs  = [5, 4, 3, 2, 1]

    groupes = sorted(freq.items(), key=lambda x: (x[1], x[0]), reverse=True)
    freqs   = [g[1] for g in groupes]
    vg      = [g[0] for g in groupes]

    if is_flush and is_suite and valeurs[0] == 14:
        return (9,) + tuple(valeurs)
    if is_flush and is_suite:
        return (8,) + tuple(valeurs)
    if freqs[0] == 4:
        return (7,) + tuple(vg)
    if freqs[0] == 3 and freqs[1] == 2:
        return (6,) + tuple(vg)
    if is_flush:
        return (5,) + tuple(valeurs)
    if is_suite:
        return (4,) + tuple(valeurs)
    if freqs[0] == 3:
        return (3,) + tuple(vg)
    if freqs[0] == 2 and freqs[1] == 2:
        return (2,) + tuple(vg)
    if freqs[0] == 2:
        return (1,) + tuple(vg)
    return (0,) + tuple(valeurs)


def combinaisons_5(cartes):
    result = []
    n = len(cartes)
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                for l in range(k+1, n):
                    for m in range(l+1, n):
                        result.append([cartes[i], cartes[j], cartes[k], cartes[l], cartes[m]])
    return result


def meilleure_main(cartes):
    if len(cartes) < 5:
        return (0,)
    best = None
    for combo in combinaisons_5(cartes):
        score = evaluer_main(combo)
        if best is None or score > best:
            best = score
    return best