import random

def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def euclide_etendu(a, b):
    modulo_initial = b
    x_prec, x = 1, 0
    y_prec, y = 0, 1

    while b != 0:
        quotient = a // b
        a, b = b, a % b
        x_prec, x = x, x_prec - quotient * x
        y_prec, y = y, y_prec - quotient * y

    if x_prec < 0:
        x_prec += modulo_initial
        
    return x_prec

def est_premier_fermat(n, k=10):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
        
    for i in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
            
    return True

def generer_premier(mini, maxi):
    while True:
        candidat = random.randint(mini, maxi)
        if est_premier_fermat(candidat):
            return candidat

def generer_cles_alice():
    p = generer_premier(100, 999)
    q = generer_premier(100, 999)
    
    while p == q:
        q = generer_premier(100, 999)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = random.randint(2, phi_n - 1)
    
    while pgcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)

    d = euclide_etendu(e, phi_n)

    return (n, e), (n, d)

def dechiffrer_message(message_chiffre, cle_privee):
    n, d = cle_privee
    message_clair = ""
    
    for c in message_chiffre:
        m = pow(c, d, n)
        message_clair += chr(m)
        
    return message_clair

if __name__ == "__main__":
    cle_publique, cle_privee = generer_cles_alice()
    
    print("La clé publique générée est :", cle_publique)
    print("La clé privée générée est :", cle_privee)
    
    texte_de_bob = "Projet RSA"
    n_pub, e_pub = cle_publique
    message_intercepte = [pow(ord(caractere), e_pub, n_pub) for caractere in texte_de_bob]
    
    print("Alice reçoit ce message :", message_intercepte)
    
    texte_retrouve = dechiffrer_message(message_intercepte, cle_privee)
    print("Le message déchiffré est :", texte_retrouve)