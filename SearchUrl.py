import os, fnmatch, sys

listFileConfName = []
listFileConfJson = []

#Fonction qui cherche le fichier config.php où se trouve l'url de certain cms
def SearchConf(currentpath):
  listPathConfig = []
  pattern = 'config.php'
  for path, dirs, files in os.walk(currentpath):
    for fname in fnmatch.filter(files, pattern):
      chemin = os.path.join(path, fname)
      listPathConfig.append(chemin)
      listFileConfName.append(fname)
  return listPathConfig

#Fonction qui cherche le fichier apache.conf où se trouve l'url de certain cms
def SearchConfJson(currentpath):
  listPathConfJson = []
  pattern = 'apache.conf'
  for path, dirs, files in os.walk(currentpath):
    for fname in fnmatch.filter(files, pattern):
      chemin = os.path.join(path, fname)
      listPathConfJson.append(chemin)
      listFileConfJson.append(fname)
  return listPathConfJson