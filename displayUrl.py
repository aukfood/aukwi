import os, sys, SearchUrl, subprocess

listDbName = []

#Fonction qui cherche dans un fichier si il contient les informations liées à l'url des cms (Wordpress, Moodle, NextCloud)
def TakeUrlCms(fileConfig):
    listUrlCms = []
    fileConfig = fileConfig.split('\n')
    for line in fileConfig:
        if line.startswith('    0 => '):
            start = line.index('    0 => ') + len('    0 => ')
            end = line.index(',', start)
            url = line[start:end]
            listUrlCms.append(url)
        if line.startswith('    0 => \''):
            start = line.index('    0 => \'') + len('    0 => \'')
            end = line.index('.', start)
            dbname = line[start:end]
            listDbName.append(dbname)

    return listUrlCms

#Fonction qui cherche dans un fichier si il contient les informations liées à l'url du cms (PhpMyAdmin)     
def TakeUrlCmsJson(fileConfig):
    listUrlCmsJson = []
    fileConfig = fileConfig.split('\n')
    for line in fileConfig:
        if line.startswith('  ServerName '):
          start = line.index('  ServerName ') + len('  ServerName ')
          end = line.index('ovh', start)+3
          url = line[start:end]
          listUrlCmsJson.append(url)      

    return listUrlCmsJson

#Fonction qui crée une condition pour trier les fichiers contenant les url
def trueOrNot(fileConfig):
    fileConfig = fileConfig.split('\n')
    yesOrNo = False
    for line in fileConfig:
        if line.startswith('    0 => '):
            start = line.index('    0 => ') + len('    0 => ')
            end = line.index(',', start)
            url = line[start:end]
            yesOrNo = True
        if line.startswith('    0 => \''):
            start = line.index('    0 => \'') + len('    0 => \'')
            end = line.index('.', start)
            dbname = line[start:end]
            yesOrNo = True

    return yesOrNo

#Fonction qui crée une condition pour trier les fichiers contenant les url
def trueOrNotJson(fileConfig):
    fileConfig = fileConfig.split('\n')
    yesOrNo = False
    for line in fileConfig:
        if line.startswith('  ServerName '):
            start = line.index('  ServerName ') + len('  ServerName ')
            end = line.index('ovh', start)+3
            url = line[start:end]
            yesOrNo = True

    return yesOrNo

#récupération des url des cms (Moodle, Wordpress, NextCloud) dans une liste
def displayServ():
    currentpath = "/" #chemin vers repertoire courant
    pathOfFileConf = SearchUrl.SearchConf(currentpath)
    servList = []

    for i in range(len(pathOfFileConf)):
            fileConfig = open(pathOfFileConf[i], 'r').read()
            if (trueOrNot(fileConfig) == True):
                serv = subprocess.getoutput('sudo '+ pathOfFileConf[i] +' | hostname -f').split('\n')
                serv = [x.split('\t')[0] for x in serv]

                for Name in serv:
                  servList.append(Name)
                  break
    return servList

#récupération des url du cms (PhpMyAdmin) dans une liste 
def displayServJson():
    currentpath = "/" #chemin vers repertoire courant
    pathOfFileConf = SearchUrl.SearchConfJson(currentpath)
    servListJson = []

    for i in range(len(pathOfFileConf)):
        fileConfig = open(pathOfFileConf[i], 'r').read()
        if (trueOrNotJson(fileConfig) == True):
          serv = subprocess.getoutput('sudo '+ pathOfFileConf[i] +' | hostname -f').split('\n')
          serv = [x.split('\t')[0] for x in serv]

    for Name in serv:
      servListJson.append(Name)
      break
    return servListJson
    
def displayUrl():
  currentpath = "/" #chemin vers repertoire courant
  pathOfFileConf = SearchUrl.SearchConf(currentpath)
  listUrl = []

  for i in range(len(pathOfFileConf)):
    fileConfig = open(pathOfFileConf[i], 'r').read()
    listUrl += TakeUrlCms(fileConfig)
  return listUrl
   
def displayUrlJson():
  currentpath = "/" #chemin vers repertoire courant
  pathOfFileConfJson = SearchUrl.SearchConfJson(currentpath)
  listUrlJson = []

  for y in range(len(pathOfFileConfJson)):
    if "myadmin" in pathOfFileConfJson[y]:
      fileConfig = open(pathOfFileConfJson[y], 'r').read()
      listUrlJson += TakeUrlCmsJson(fileConfig)             
  return listUrlJson