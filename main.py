import os
import csv
import re
from getpass import getpass
from email_utils import Email, EmailConnection
from file_utils import FileUtils

f_utils = FileUtils()

# ------ Variables gloables de configuration ------
#SERVER_SMTP = "smtps.etsmtl.ca"  # Serveur SMTP
SERVER_SMTP = "smtp.gmail.com"
SERVER_PORT = 587  # Port SMTP
#FROM = "reflets@etsmtl.net"  # Courriel Reflets
FROM = "skander.kc@gmail.com"
# -------------------------------------------------

print('================================================')
print('           Bievenue sur ImageMailer! V1.0       ')
print()
print('        Écrit par Skander pour le club photo    ')
print('                 R E F L E T S                  ')
print()
print('         Contact: skander.kc@gmail.com          ')
print('================================================')
print()
print("°°° Connexion au serveur de messagerie Gmail °°°")

# Connexion au serveur SMTP Gmail
password = getpass(" - Entrer le mot de passe Gmail de Reflets (" + FROM + ") : ")
print("Connexion au serveur Gmail...")
server = EmailConnection(SERVER_SMTP, SERVER_PORT, FROM, password)
print("Connexion établie!")

print()
print("°°° Spécification du dossier image  et des données en .CSV °°°")
# Récupérer le dossier contenant les photos
# Dans ce dossier, on devrait retrouver pleins de dossier ayant comme nom l'index des participants
root_dir = input(" - Indiquer le nom du dossier contenant les photos (laisse vide si actuel) : ")
photos_dir_content = f_utils.get_directory_content(root_dir)
print(photos_dir_content)

# Récupérer fichier CSV
csv_file_name = input(" - Indiquer le nom du fichier CSV contenant les emails: ")
# Vérification validité fichier csv
f_utils.check_if_csv(csv_file_name)

# Lire les données
with open(csv_file_name, 'r', encoding="utf-8") as csv_file:
    reader = csv.reader(csv_file, delimiter=',')

    next(reader)   # Skip la première ligne (nom des colonnes)

    for row in reader:
        row_str = str(row)
        row_array = row_str.split(',')

        name = row_array[1].strip()
        email = row_array[2].strip()
        # Formatage: supprimer les guillemets (') au début et à la fin
        name = name[1:-1]
        email = email[1:-1]

        index_raw = row_array[-1] # >>> '177'] (par exemple)
        # Formatage: re permet de garder que des nombres (regex \D).
        index = re.sub(r"\D", "", index_raw) # >>> 177 (même exemple)

        print(index, name, email)

        # Chercher nom dossier ayant le même numero que l'index
        for directory in photos_dir_content:
            directory_path = root_dir + "/" + directory
            # Youpi ! On a trouvé le participant et son dossier contenant les photos
            # On peut maintenant envoyer ses photos !
            if os.path.isdir(directory_path) and directory == index:
                photos = [f for f in os.listdir(directory_path) if f_utils.is_photo(f)]  # Ne récuperer que les images

                # Remplacer la photo par le chemin complet
                for i, photo in enumerate(photos):
                    photos[i] = directory_path + "/" + photo

                print(photos)

                subject = 'Test photos'
                message ='Salut ! \n Voici tes photos!'
                print("Préparation du courriel à envoyer à " + name)
                email = Email(FROM, email, subject, message, attachments=photos)
                print("Envoi...")
                server.send(email)
                print("Email envoyé!")

# Déconnexion
print("Déconnexion du serveur...")
server.close()
print("Déconnecté!")

