import SearchUrl

# Fonction qui cherche dans un fichier si il contient les informations liées à l'url du cms (RocketChat)     
def TakeUrlRocket(fileConfig):
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
    fileConfig = fileConfig.split('\n')
    for line in fileConfig:
        if line.startswith('    "semver": "'):
            return True
    return False

def displayUrlRock():
    currentpath = "/" # chemin vers répertoire courant
    pathOfFileConfJson = SearchUrl.SearchConfJson(currentpath)
    listUrlRock = []

    for path in pathOfFileConfJson:
        if "Rocket.Chat" in path:
            with open(path, 'r') as file:
                fileConfig = file.read()
                listUrlRock += TakeUrlRocket(fileConfig)
    return listUrlRock
