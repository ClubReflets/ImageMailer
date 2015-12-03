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

    """
    Vérifie si l'objet passé en paramètre est un dossier.
    Si oui, retourner le contenu du dossier
    Si non, retourner le contneu du dossier actuel
    """
    def get_directory_content(self, dir):
        if os.path.isdir(dir):
            photos_dir_content = os.listdir(dir)
        else:
            photos_dir_content = os.listdir(os.curdir)
        return photos_dir_content

    def read_html(self, file_html):
        html = None
        if file_html:
            with open(file_html, 'r', encoding="utf-8") as file:
                html = file.read()
        return html
