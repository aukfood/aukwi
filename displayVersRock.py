import os, sys, SearchVersionFile, pathlib 

listRocket = []


#Fonction qui cherche dans un fichier si il contient les informations liées à la version de rocket
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

    
#récupération de la version du cms (RocketChat) dans une liste     
def displayVersionRocket():
    currentpath = "/" #chemin vers repertoire courant
    pathOfFileJson = SearchVersionFile.SearchJson(currentpath)
    listVersionJson = []

    for y in range(len(pathOfFileJson)):
      if "Rocket.Chat" in pathOfFileJson[y]:
        fileVersion = open(pathOfFileJson[y], 'r').read()  
        listVersionJson += TakeVersionRocket(fileVersion)
 
               
    return listVersionJson