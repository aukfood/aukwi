import SearchUrl

# Fonction qui cherche dans un fichier si il contient les informations liées à l'url du cms (RocketChat)     
def TakeUrlRocket(fileConfig):
    """
    Extrait l'URL de RocketChat à partir d'un fichier de configuration.
    """
    listUrlRocket = []
    fileConfig = fileConfig.split('\n')
    for line in fileConfig:
        if line.startswith('    "semver": "'):
            start = line.index('    "semver": "') + len('    "semver": "')
            end = line.index('"', start)
            url = line[start:end]
            listUrlRocket.append(url)
    return listUrlRocket

# Fonction qui crée une condition pour trier les fichiers contenant les url
def trueOrNotRock(fileConfig):
    """
    Vérifie si un fichier de configuration contient des informations liées à l'URL de RocketChat.
    """
    fileConfig = fileConfig.split('\n')
    for line in fileConfig:
        if line.startswith('    "semver": "'):
            return True
    return False

def displayUrlRock():
    """
    Affiche les URLs de RocketChat en parcourant les fichiers de configuration.
    """
    currentpath = "/" # chemin vers répertoire courant
    pathOfFileConfJson = SearchUrl.SearchConfJson(currentpath)
    listUrlRock = []

    for path in pathOfFileConfJson:
        if "Rocket.Chat" in path:
            with open(path, 'r') as file:
                fileConfig = file.read()
                listUrlRock += TakeUrlRocket(fileConfig)
    return listUrlRock
