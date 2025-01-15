import os, fnmatch

listFileConfName = []
listFileConfJson = []

# Fonction qui cherche des fichiers correspondant à un pattern
def searchConfigFiles(currentpath, pattern, fileList):
    """
    Recherche des fichiers correspondant à un pattern donné dans un répertoire et ses sous-répertoires.
    """
    listPath = []
    for path, dirs, files in os.walk(currentpath):
        for fname in fnmatch.filter(files, pattern):
            chemin = os.path.join(path, fname)
            listPath.append(chemin)
            fileList.append(fname)
    return listPath

# Fonction qui cherche le fichier config.php où se trouve l'url de certains cms
def SearchConf(currentpath):
    """
    Recherche des fichiers config.php dans le répertoire courant et ses sous-répertoires.
    """
    return searchConfigFiles(currentpath, 'config.php', listFileConfName)

# Fonction qui cherche le fichier apache.conf où se trouve l'url de certains cms
def SearchConfJson(currentpath):
    """
    Recherche des fichiers apache.conf dans le répertoire courant et ses sous-répertoires.
    """
    return searchConfigFiles(currentpath, 'apache.conf', listFileConfJson)

def SearchConfWp(url):
    """
    Recherche le fichier wp-config.php dans le répertoire spécifié.
    """
    return searchConfigFiles(f"/var/www/{url}/", 'wp-config.php', listFileConfName)[0]