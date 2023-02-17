import os, fnmatch, sys

listFileVersName = []
listFileJsonName = []

#Recherche du fichier version.php (où se trouve la version des cms Moodle, Wordpress, Nextcloud) dans tous les dossiers à partir de la raçine du serveur
def SearchVers(currentpath):
  pattern = 'version.php'
  listPathVersion = []
  for path, dirs, files in os.walk(currentpath):
    for fname in fnmatch.filter(files, pattern):
      chemin = os.path.join(path, fname)
      listPathVersion.append(chemin)
      listFileVersName.append(fname)
            
  return listPathVersion

#Recherche du fichier package.json (où se trouve la version du cmc PhpMyAdmin) dans tous les dossiers à partir de la raçine du serveur
def SearchJson(currentpath):
  listPathJson = []
  pattern = 'package.json'
  for path, dirs, files in os.walk(currentpath):
    for fname in fnmatch.filter(files, pattern):
      chemin = os.path.join(path, fname)
      listPathJson.append(chemin)
      listFileJsonName.append(fname)
            
  return listPathJson
