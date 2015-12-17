import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from mimetypes import guess_type
from email.encoders import encode_base64
from smtplib import SMTP

class Email:
    """
    Classe utilitaire permettant de construire la forme du courriel (From, To, Message , Attachement, etc.)
    """
    def __init__(self, from_, to, subject, message, message_type='plain', attachments=None, message_encoding='utf-8'):

        self.email = MIMEMultipart()
        self.email['From'] = from_
        self.email['To'] = to
        self.email['Subject'] = subject

        # Text brute
        text = MIMEText(message, message_type, message_encoding)
        self.email.attach(text)

        # Attachements (image par exemple)
        if attachments is not None:
            self.attach_files(attachments)

    """
    Permet d'attacher des fichiers (images par exemple) dans un courriel
    """
    def attach_files(self, attachments):

        for file_name in attachments:
            # Récupérer le type de fichier
            mimetype, encoding = guess_type(file_name)
            mimetype = mimetype.split('/', 1)
            # Lire le fichier
            fp = open(file_name, 'rb')
             # Ajouter l'attachement
            attachment = MIMEBase(mimetype[0], mimetype[1])
            attachment.set_payload(fp.read())
            fp.close()
            encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_name))
            self.email.attach(attachment)

    def __str__(self):
        return self.email.as_string()


class EmailConnection:
    """
    Classe utilitaire permettant gérer la connexion au serveur SMTP et l'envoi de courriel
    """
    def __init__(self, smtp, port, username, password):
        self.smtp = smtp
        self.port = port
        self.username = username
        self.password = password
        self.connect()

    """
    Connection au serveur SMTP de la messagerie avec No. de port
    """
    def connect(self):
        self.connection = SMTP(self.smtp, self.port)
        self.connection.ehlo()
        self.connection.starttls()
        self.connection.ehlo()
        self.connection.login(self.username, self.password)

    """
    Déconnection du serveur
    """
    def close(self):
        self.connection.close()

    """
    Envoyer un courriel
    """
    def send(self, message, from_=None, to=None):
        if type(message) == str:
            if from_ is None or to is None:
                raise Exception("Vous devez spécifier un champ 'from' et un champ 'to' pour envoyer votre courriel.")
        else:
            from_ = message.email['From']
            to = message.email['To']
            message = str(message)

        return self.connection.sendmail(from_, to, message)
