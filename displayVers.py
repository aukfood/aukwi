import os, sys, SearchVersionFile, pathlib

listCms = []
listCmsJson = []

#Fonction qui cherche dans un fichier si il contient les informations liées à la version des cms 
def TakeVersionCms(fileVersion):
    listVersionCms = []
    fileVersion = fileVersion.split('\n')
    for line in fileVersion:
        if line.startswith('$release  = '):
            start = line.index('$release  = ') + len('$release  = ')
            end = line.index('; ', start)
            version = line[start:end]
            cms = "Moodle"
            listCms.append(cms)
            listVersionCms.append(version)
        elif line.startswith('$wp_version = '):
            start = line.index('$wp_version =') + len('$wp_version = ')
            end = line.index(';', start)
            version = line[start:end]
            cms = "Wordpress"
            listCms.append(cms)
            listVersionCms.append(version)
        elif line.startswith('$OC_VersionString = \''):
            start = line.index('$OC_VersionString = \'') + len('$OC_VersionString = \'')
            end = line.index('\'', start)
            version = line[start:end]
            cms = "NextCloud"
            listCms.append(cms)
            listVersionCms.append(version)


    return listVersionCms

#Fonction qui cherche dans un fichier si il contient les informations liées à la version du cms
def TakeVersionCmsJson(fileVersion):
    listVersionCmsJson = []
    fileVersion = fileVersion.split('\n')
    for line in fileVersion:
      if line.startswith('  "version": "'):
        start = line.index('  "version": "') + len('  "version": "')
        end = line.index('"', start)
        version = line[start:end]
        cms = "PhpMyAdmin"
        listCmsJson.append(cms)
        listVersionCmsJson.append(version)

    return listVersionCmsJson

#récupération de la version des cms (Moodle, Wordpress, NextCloud) dans une liste 
def displayVersion():
    currentpath = "/" #chemin vers repertoire courant
    pathOfFileVers = SearchVersionFile.SearchVers(currentpath)
    listVersion = []

    for i in range(len(pathOfFileVers)):
      fileVersion = open(pathOfFileVers[i], 'r').read()
      listVersion += TakeVersionCms(fileVersion) 
               
    return listVersion
    
#récupération de la version du cms (PhpMyAdmin) dans une liste     
def displayVersionJson():
    currentpath = "/" #chemin vers repertoire courant
    pathOfFileJson = SearchVersionFile.SearchJson(currentpath)
    listVersionJson = []

    for y in range(len(pathOfFileJson)):
      if "myadmin" in pathOfFileJson[y]:
        fileVersion = open(pathOfFileJson[y], 'r').read()  
        listVersionJson += TakeVersionCmsJson(fileVersion)
 
               
    return listVersionJson