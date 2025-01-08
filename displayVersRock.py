import SearchVersionFile

listRocket = []

# Fonction qui cherche dans un fichier si il contient les informations liées à la version de RocketChat
def TakeVersionRocket(fileVersion):
    listVersionRocket = []
    fileVersion = fileVersion.split('\n')
    for line in fileVersion:
        if line.startswith('    "semver": "'):
            start = line.index('    "semver": "') + len('    "semver": "')
            end = line.index('"', start)
            version = line[start:end]
            cms = "RocketChat"
            listRocket.append(cms)
            listVersionRocket.append(version)
    return listVersionRocket

# Récupération de la version du cms (RocketChat) dans une liste     
def displayVersionRocket():
    currentpath = "/" # chemin vers répertoire courant
    pathOfFileJson = SearchVersionFile.SearchJson(currentpath)
    listVersionJson = []

    for path in pathOfFileJson:
        if "Rocket.Chat" in path:
            with open(path, 'r') as file:
                fileVersion = file.read()
                listVersionJson += TakeVersionRocket(fileVersion)
    return listVersionJson