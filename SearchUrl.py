import os, fnmatch

listFileConfName = []
listFileConfJson = []

# Fonction qui cherche des fichiers correspondant à un pattern
def searchConfigFiles(currentpath, pattern, fileList):
    listPath = []
    for path, dirs, files in os.walk(currentpath):
        for fname in fnmatch.filter(files, pattern):
            chemin = os.path.join(path, fname)
            listPath.append(chemin)
            fileList.append(fname)
    return listPath

# Fonction qui cherche le fichier config.php où se trouve l'url de certains cms
def SearchConf(currentpath):
    return searchConfigFiles(currentpath, 'config.php', listFileConfName)

# Fonction qui cherche le fichier apache.conf où se trouve l'url de certains cms
def SearchConfJson(currentpath):
    return searchConfigFiles(currentpath, 'apache.conf', listFileConfJson)