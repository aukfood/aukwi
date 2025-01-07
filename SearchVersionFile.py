import os, fnmatch, sys

listFileVersName = []
listFileJsonName = []

# Recherche de fichiers correspondant à un pattern dans tous les dossiers à partir de la racine du serveur
def searchFiles(currentpath, pattern, fileList):
    listPath = []
    for path, dirs, files in os.walk(currentpath):
        for fname in fnmatch.filter(files, pattern):
            chemin = os.path.join(path, fname)
            listPath.append(chemin)
            fileList.append(fname)
    return listPath

# Recherche du fichier version.php (où se trouve la version des cms Moodle, Wordpress, Nextcloud)
def SearchVers(currentpath):
    return searchFiles(currentpath, 'version.php', listFileVersName)

# Recherche du fichier package.json (où se trouve la version du cmc PhpMyAdmin)
def SearchJson(currentpath):
    return searchFiles(currentpath, 'package.json', listFileJsonName)
