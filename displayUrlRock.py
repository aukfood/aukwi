import os, sys, SearchUrl, subprocess

#Fonction qui cherche dans un fichier si il contient les informations liées à l'url du cms (PhpMyAdmin)     
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

#Fonction qui crée une condition pour trier les fichiers contenant les url
def trueOrNotRock(fileConfig):
    fileConfig = fileConfig.split('\n')
    yesOrNo = False
    for line in fileConfig:
        if line.startswith('    "semver": "'):
            start = line.index('    "semver": "') + len('    "semver": "')
            end = line.index('"', start)
            url = line[start:end]
            yesOrNo = True

    return yesOrNo

#récupération des url du cms (PhpMyAdmin) dans une liste 
def displayServRocket():
  currentpath = "/" #chemin vers repertoire courant
  pathOfFileConf = SearchUrl.SearchConfJson(currentpath)
  servListRock = []

  for i in range(len(pathOfFileConf)):
    fileConfig = open(pathOfFileConf[i], 'r').read()
    if (trueOrNotRock(fileConfig) == True):
      serve = subprocess.getoutput('sudo '+ pathOfFileConf[i] +' | hostname -f').split('\n')
      serve = [x.split('\t')[0] for x in serv]

  for Name in serve:
    servListRock.append(Name)
    break
  return servListRock
    
def displayUrlRock():
  currentpath = "/" #chemin vers repertoire courant
  pathOfFileConfJson = SearchUrl.SearchConfJson(currentpath)
  listUrlRock = []

  for y in range(len(pathOfFileConfJson)):
    if "Rocket.Chat" in pathOfFileConfJson[y]:
      fileConfig = open(pathOfFileConfJson[y], 'r').read()
      listUrlRock += TakeUrlRocket(fileConfig)             
  return listUrlRock