import os
import csv
import re
from getpass import getpass
from email_utils import Email, EmailConnection
from file_utils import FileUtils
from datetime import datetime

f_utils = FileUtils()

# ------ Variables gloables de configuration ------
SERVER_SMTP = "smtp.gmail.com"
SERVER_PORT = 587  # Port SMTP
#FROM = "reflets@etsmtl.net" # Adresse Reflets par défaut
FROM = "skander.kc@gmail.com"
# -------------------------------------------------

print('================================================')
print('           Bievenue sur ImageMailer! V1.0       ')
print()
print('        Écrit par Skander pour le club photo    ')
print('                 R E F L E T S                  ')
print()
print('         Contact: skander.kc AT gmail.com       ')
print('================================================')
print()
print("°°° Connexion au serveur de messagerie Gmail °°°")

# Connexion au serveur SMTP Gmail
password = getpass(" - Entrer le mot de passe de " + FROM + " : ")
print("Connexion au serveur de messagerie...")

try:
    server = EmailConnection(SERVER_SMTP, SERVER_PORT, FROM, password)
except:
    raise Exception("Il y a une erreur de connexion au serveur de messagerie. Réessayez.")

print("Connexion établie!")

print()

print("°°° Spécification du dossier image  et des données en .CSV °°°")
# Récupérer le dossier contenant les photos
# Dans ce dossier, on devrait retrouver pleins de dossier ayant comme nom l'index des participants
root_dir = input(" - Indiquer le nom du dossier contenant les photos (laisse vide si actuel) : ")
photos_dir_content = f_utils.get_directory_content(root_dir)
#print(photos_dir_content)

# Récupérer fichier CSV
csv_file_name = input(" - Indiquer le nom du fichier CSV contenant les emails: ")
# Vérification validité fichier csv
f_utils.check_if_csv(csv_file_name)

print()

count_rows = sum(1 for line in open(csv_file_name))
total_participant = count_rows - 1

if count_rows == 0:
    raise Exception("Le fichier .Csv est vide.")

# Lire les données en csv et envoyer les courriels
print("°°° Envoi de " + str(total_participant) + " courriels °°°")
with open(csv_file_name, 'r', encoding="utf-8") as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    next(reader)   # Skip la première ligne (nom des colonnes)


    emails_not_sent = []

    index_row = 1

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
        formatted_index = f_utils.formatted_index(int(index))  # Ex. si index 1 => 001

        participant = (index + " - " + name + " - " + email)

        # Chercher nom dossier ayant le même numero que l'index
        for directory in photos_dir_content:
            directory_path = root_dir + "/" + directory
            # Youpi ! On a trouvé le participant et son dossier contenant les photos
            # On peut maintenant envoyer ses photos !
            if os.path.isdir(directory_path) and directory == formatted_index:

                photos = [f for f in os.listdir(directory_path) if f_utils.is_photo(f)]  # Ne récuperer que les images

                print('---------------------- ' + str(index_row) + '/' + str(total_participant) + ' ----------------------')
                print(participant)

                if len(photos) > 0:
                    # Remplacer la photo par le chemin complet
                    for i, photo in enumerate(photos):
                        photos[i] = directory_path + "/" + photo

                    subject = 'Votre photo LinkedIn est prête!'
                    message = f_utils.read_file_content("mails/email.html")
                    print("Préparation du courriel à envoyer à " + name )
                    email = Email(FROM, email, subject, message, attachments=photos, message_type="html")
                    print("Envoi...")

                    try:
                        server.send(email)
                        print("Courriel envoyé!")
                    except:
                        print("ÉCHEC de l'envoi du courriel à " + name)
                        print("On passe au suivant...")
                        reason = "Échec envoi"
                        participant = participant + " - " + reason
                        emails_not_sent.append(participant)
                        pass
                else:
                    print("Aucune photo trouvée")
                    reason = "Aucune photo"
                    participant = participant + " - " + reason
                    emails_not_sent.append(participant)

        index_row += 1
print()

# Afficher les emails non envoyés si c'est le cas
count_emails_not_sent = len(emails_not_sent)
if count_emails_not_sent > 0:
    print("°°° Oyé! Oyé! il y a eu " + str(count_emails_not_sent) + " courriels inacheminés °°°")
    print("Voici la liste, sous la forme : index - nom - courriel ")

    # Afficher & enregistrer la liste dans un fichier texte
    now = datetime.strftime(datetime.now(), '%Y-%m-%d-%H_%M_%S')
    file_emails_not_sent = "emails_not_sent_" + now + ".txt"

    if not os.path.exists("log"):
        os.makedirs("log")

    with open("log/" + file_emails_not_sent, 'w') as text_file:
        text_file.write("Liste des courriels inacheminés \n")
        text_file.write("Format id - nom - courriel - raison : \n\n")
        for email in emails_not_sent:
            email_str = str(email)
            print(email_str)
            text_file.write(email_str + "\n")
    print("Pas de panique, vous pouvez consulter cette liste dans le fichier : log/" + file_emails_not_sent)

else:
    print("°°° Succès! Tous les courriels ont été envoyés. °°°")

print()

# Déconnexion
print("Déconnexion du serveur...")
server.close()
print("Déconnecté!")
