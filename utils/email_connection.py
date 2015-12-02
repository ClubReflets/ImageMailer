import os
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class Email:
    """
    Classe utilitaire permettant d'envoyer des emails avec des images en attachement
    """

    #def __init__(self,

class EmailConnection:

    def __init__(self, server, port, username, password):
        self.server = server
        self.port = port
        self.username = username
        self.password = password

        try:
            self.connect()
        except:
            print "Erreur de connexion à la messagerie"

    """
    Connection au serveur SMTP de la messagerie avec No. de port
    """
    def connect(self):
        self.connection =  SMTP(self.server, self.port)
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
    Envoyer un mail
    """
    def send_mail(self, message, from_, to=):
        if type(message) is not str:
            message = str(message)
        return self.connection.sendmail(from_, to, message)








