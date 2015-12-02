import os
import sys
import csv
import re
from getpass import getpass
from email_utils import Email, EmailConnection
from file_utils import FileUtils

f_utils = FileUtils()

# ------ Variables gloables de configuration ------
SERVER_SMTP = "smtps.etsmtl.ca"  # Serveur SMTP
SERVER_PORT = 587  # Port SMTP
FROM = "reflets@etsmtl.net"  # Courriel Reflets
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
print(root_dir)

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

                #print(photos)

                email = Email("lol@gmail.com", "lol@gmail.com", "lol", "lol")
                email.attach_files(photos)

#
# server_name = input("- Entrer le serveur de messagerie ('g' pour Gmail): ")
#
# if server_name == 'g' or server_name == 'G':
#     server_smtp = 'smtp.gmail.com'
#     port = 587
#
# email = input('- Votre email: ')
# password = getpass('- Your mot de passe: ')
# to_email = input(' - Destination email: ')
# to_name = input(' - Name of destination: ')
# subject = 'Sending mail easily with Python'
# message = 'here is the message body'
# attachments = [sys.argv[0]]
#
# print 'Connecting to server...'
# server = EmailConnection(server_smtp, port, email, password)
# print 'Preparing the email...'
# email = Email(email, to_email, subject, message)
# print 'Sending...'
# server.send(email)
# print 'Disconnecting...'
# server.close()
# print 'Done!'

