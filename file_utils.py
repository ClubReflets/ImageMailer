#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class FileUtils:

    def __init__(self): pass

    """
    Renvoie True si le fichier est une photo (jpg/png)
    """
    def is_photo(self, file):
        return (file.endswith(".jpg")
            or file.endswith(".jpeg")
            or file.endswith(".JPG")
            or file.endswith(".JPEG")
            or file.endswith(".png"))

    """
    Renvoie True si le fichier est de type Csv
    """
    def check_if_csv(self, file):

        if not file or not os.path.isfile(file):
            raise Exception("Fichier CSV Introuvable.")
        elif not file.endswith(".csv"):
            raise Exception("Le fichier doit être un CSV")