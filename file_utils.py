#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class FileUtils:

    def is_photo(self, file):
        return (file.endswith(".jpg")
            or file.endswith(".jpeg")
            or file.endswith(".JPG")
            or file.endswith(".JPEG")
            or file.endswith(".png"))

    def check_if_csv(self, file):
        print file
        if not os.path.isfile(file):
            raise FileNotFoundError("Fichier CSV Introuvable.")
        elif not file.endswith(".csv"):
            raise ImportError("Le fichier doit être un CSV")