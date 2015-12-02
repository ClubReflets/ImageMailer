#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from getpass import getpass
from email_utils import Email, EmailConnection

print '================================================'
print '           Bievenue sur ImageMailer! V1.0       '
print
print '     Écrit par Skander pour le club photo       '
print '                 R E F L E T S                  '
print '================================================'

print

print "Veuillez d'abord entrer quelques informations..."

server_name = raw_input("- Entrer le serveur de messagerie ('g' pour Gmail): ")

if server_name == 'g' or server_name == 'G':
    server_smtp = 'smtp.gmail.com'
    port = 587

email = raw_input('- Votre email: ')
password = getpass('- Your mot de passe: ')
to_email = raw_input(' - Destination email: ')
to_name = raw_input(' - Name of destination: ')
subject = 'Sending mail easily with Python'
message = 'here is the message body'
attachments = [sys.argv[0]]

print 'Connecting to server...'
server = EmailConnection(server_smtp, port, email, password)
print 'Preparing the email...'
email = Email(email, to_email, subject, message)
print 'Sending...'
server.send(email)
print 'Disconnecting...'
server.close()
print 'Done!'

