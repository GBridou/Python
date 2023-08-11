import re
import sqlite3

# Définition de la classe personne
class personne:
    def __init__(self, nom, prenom, age, login, mdp):
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.login = login
        self.mdp = mdp

# Fonction pour afficher le menu
def menu():
    print("[I]nscription")
    print("[C]onnexion")
    print("[Q]uitter")
    choix = input("Votre choix -> ")
    return choix

# Vérification des informations pour éviter les informations personnelles dans le mot de passe
def verif_info(nom, prenom, login, mdp):
    nom = str(nom)
    prenom = str(prenom)
    login = str(login)
    mdp = str(mdp)
    if (mdp.find(nom) != -1 or mdp.find(prenom) != -1 or mdp.find(login) != -1):
        print("Erreur, votre mot de passe ne doit pas contenir d'informations personnelles")
        return False
    return True

# Vérification si le mot de passe est trop souvent utilisé
def verif_fichier(mdp):
    mdp = str(mdp)
    try:
        with open("Seclist.txt", encoding="latin-1") as f:
            for line in f:
                line = line.replace("\n", "")
                if (mdp.find(line) != -1 and len(line) >= 5):
                    print(line)
                    print(mdp)
                    f.close()
                    print("Votre mot de passe est trop souvent utilisé")
                    return False
    except:
        print("Impossible d'ouvrir le fichier")
    f.close()
    return True

# Vérification si le login est déjà pris
def verif_login(utilisateur, login):
    if (len(login) == 0):
        print("Erreur, le champ de saisie du login ne peut pas être vide")
        return False
    for user in utilisateur:
        if (user.login == login):
            print("Ce nom est déjà pris")
            return False
    return True

# Saisie des informations de l'utilisateur
def prise_info(utilisateur):
    regx = re.compile("([A-Z]+)([a-z]+)")
    nom = input("Quel est votre nom ? : ")
    if (regx.match(nom)):
        prenom = input("Quel est votre prénom ? : ")
        if (regx.match(prenom)):
            age = input("Quel est votre âge ? : ")
            regx = re.compile("([1-9][0-9]*)")
            if (regx.match(age)):
                login = input("Entrer login : ")
                if (verif_login(utilisateur, login)):
                    mdp = input("Entrer mdp : ")
                    regx = re.compile("(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[-+!.*@_])([-+!.*@_\w]{12,})")
                    if (regx.match(mdp)):
                        if (verif_fichier(mdp)):
                            if (verif_info(nom, prenom, login, mdp)):
                                return True, nom, prenom, age, login, mdp
                    else:
                        print("Votre mot de passe ne correspond pas à la politique")
                else:
                    print("Erreur de saisie du login")
            else:
                print("Erreur de saisie de l'âge (ce champ ne peut pas être vide et ne peut contenir que des chiffres)")
        else:
            print("Erreur de saisie du prénom (ce champ ne peut pas être vide et doit commencer par une majuscule et contenir une minuscule)")
    else:
        print("Erreur de saisie du nom (ce champ ne peut pas être vide et doit commencer par une majuscule et contenir une minuscule)")
    return False, "", "", "", "", ""

# Connexion de l'utilisateur
def connexion(utilisateur, login, mdp):
    for user in utilisateur:
        if (user.login == login and user.mdp == mdp):
            print("Bienvenue " + user.nom + " " + user.prenom)
            return True
    print("Échec de connexion")
    return False

# Établir la connexion à la base de données
conn = sqlite3.connect('utilisateurs.db')
cur = conn.cursor()

# Créer la table des utilisateurs si elle n'existe pas déjà
cur.execute('''
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY,
        nom TEXT,
        prenom TEXT,
        age INTEGER,
        login TEXT,
        mdp TEXT
    )
''')
conn.commit()

choix = str()
utilisateur = list()
while True:
    choix = menu()
    if choix == "I":
        verif, nom, prenom, age, login, mdp = prise_info(utilisateur)
        verif = bool(verif)
        if verif:
            # Insérer les données de l'utilisateur dans la base de données
            cur.execute('''
                INSERT INTO utilisateurs (nom, prenom, age, login, mdp)
                VALUES (?, ?, ?, ?, ?)
            ''', (nom, prenom, age, login, mdp))
            conn.commit()
            utilisateur.append(personne(nom, prenom, age, login, mdp))
            print("Inscription réussie")
    elif choix == "C":
        login = input("Entrer login : ")
        mdp = input("Entrer mdp : ")
        connexion(utilisateur, login, mdp)
    elif choix == "Q":
        conn.close()
        exit()
    else:
        print("Mauvais choix")
