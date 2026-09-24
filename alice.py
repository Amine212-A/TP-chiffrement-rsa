import random

def pgcd(a, b):
    # On calcule le Plus Grand Commun Diviseur (PGCD) avec l'algorithme d'Euclide
    # Tant que le reste de la division (b) n'est pas nul, on continue
    while b != 0:
        a, b = b, a % b
    # Quand b vaut 0, la variable a contient notre PGCD
    return a

def euclide_etendu(a, b):
    # Cette fonction sert à trouver l'inverse modulaire pour la clé privée (d)
    # On sauvegarde le modulo de base pour éviter d'avoir un résultat négatif à la fin
    modulo_initial = b
    
    # Initialisation des coefficients de Bézout
    x_prec, x = 1, 0
    y_prec, y = 0, 1

    # On déroule l'algorithme d'Euclide étendu tant que le reste n'est pas nul
    while b != 0:
        # On récupère le quotient de la division entière
        quotient = a // b
        a, b = b, a % b
        
        # Mise à jour des coefficients pour remonter l'algorithme à l'envers
        x_prec, x = x, x_prec - quotient * x
        y_prec, y = y, y_prec - quotient * y

    # Si l'inverse qu'on a trouvé est négatif, on lui ajoute le modulo pour le rendre positif
    if x_prec < 0:
        x_prec += modulo_initial
        
    return x_prec

def est_premier_fermat(n, k=10):
    # On utilise le petit théorème de Fermat pour tester si un nombre est premier
    # Tout ce qui est inférieur ou égal à 1 n'est pas premier
    if n <= 1:
        return False
        
    # 2 et 3 sont des nombres premiers évidents, on gagne du temps
    if n == 2 or n == 3:
        return True
        
    # On fait k tests au hasard pour être sûr (la probabilité d'erreur devient infime)
    for i in range(k):
        # On choisit un nombre aléatoire 'a' entre 2 et n-2
        a = random.randint(2, n - 2)
        
        # Si a^(n-1) modulo n n'est pas égal à 1, on est certain que le nombre n'est pas premier
        if pow(a, n - 1, n) != 1:
            return False
            
    # Si ça passe la boucle sans renvoyer False, on le considère comme premier
    return True

def generer_premier(mini, maxi):
    # Boucle infinie jusqu'à ce qu'on tombe sur un nombre premier valide
    while True:
        # On tire un nombre au hasard dans l'intervalle donné en paramètre
        candidat = random.randint(mini, maxi)
        # On vérifie sa primalité avec notre fonction de test de Fermat
        if est_premier_fermat(candidat):
            return candidat

def generer_cles_alice():
    # Étape 1 : Alice choisit deux nombres premiers p et q
    p = generer_premier(100, 999)
    q = generer_premier(100, 999)
    
    # Il faut impérativement que p et q soient distincts
    while p == q:
        q = generer_premier(100, 999)

    # Étape 2 : On calcule n, c'est le module de chiffrement public
    n = p * q
    
    # Étape 3 : On calcule l'indicatrice d'Euler, notée phi_n
    # C'est le nombre d'entiers premiers avec n
    phi_n = (p - 1) * (q - 1)

    # Étape 4 : On cherche la première partie de la clé publique 'e'
    # e doit être compris entre 2 et phi_n - 1
    e = random.randint(2, phi_n - 1)
    
    # e doit aussi être strictement premier avec phi_n (donc leur PGCD vaut 1)
    while pgcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)

    # Étape 5 : On calcule la clé privée 'd' avec l'algorithme d'Euclide étendu
    # d est l'inverse de e modulo phi_n
    d = euclide_etendu(e, phi_n)

    # On renvoie un tuple contenant la clé publique (n, e) et la clé privée (n, d)
    return (n, e), (n, d)

def dechiffrer_message(message_chiffre, cle_privee):
    # On extrait n et d depuis la clé privée d'Alice
    n, d = cle_privee
    message_clair = ""
    
    # Le message reçu par Bob est une liste de nombres chiffrés
    for c in message_chiffre:
        # Pour chaque nombre, on applique la formule de déchiffrement : m = c^d modulo n
        m = pow(c, d, n)
        # On retransforme le nombre m en vrai caractère texte (table ASCII) et on l'ajoute au texte
        message_clair += chr(m)
        
    return message_clair

if __name__ == "__main__":
    # Lancement de la génération des clés pour Alice
    cle_publique, cle_privee = generer_cles_alice()
    
    # Affichage des clés générées pour le test
    print("La clé publique générée est :", cle_publique)
    print("La clé privée générée est :", cle_privee)
    
    # -- Zone de test interne (simule ce que Bob va coder de son côté) --
    texte_de_bob = "Projet RSA"
    n_pub, e_pub = cle_publique
    
    # Bob chiffre chaque caractère du texte avec la clé publique d'Alice (formule : m^e modulo n)
    message_intercepte = [pow(ord(caractere), e_pub, n_pub) for caractere in texte_de_bob]
    
    # C'est ce tableau de nombres que les hackers vont essayer d'intercepter sur le réseau
    print("Alice reçoit ce message :", message_intercepte)
    
    # Alice utilise sa clé privée secrète pour retrouver le texte d'origine
    texte_retrouve = dechiffrer_message(message_intercepte, cle_privee)
    print("Le message déchiffré est :", texte_retrouve)