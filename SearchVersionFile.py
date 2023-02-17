import os, fnmatch, sys

listFileVersName = []
listFileJsonName = []

#Recherche du fichier version.php (o� se trouve la version des cms Moodle, Wordpress, Nextcloud) dans tous les dossiers � partir de la ra�ine du serveur
def SearchVers(currentpath):
  pattern = 'version.php'
  listPathVersion = []
  for path, dirs, files in os.walk(currentpath):
    for fname in fnmatch.filter(files, pattern):
      chemin = os.path.join(path, fname)
      listPathVersion.append(chemin)
      listFileVersName.append(fname)
            
  return listPathVersion

#Recherche du fichier package.json (o� se trouve la version du cmc PhpMyAdmin) dans tous les dossiers � partir de la ra�ine du serveur
def SearchJson(currentpath):
  listPathJson = []
  pattern = 'package.json'
  for path, dirs, files in os.walk(currentpath):
    for fname in fnmatch.filter(files, pattern):
      chemin = os.path.join(path, fname)
      listPathJson.append(chemin)
      listFileJsonName.append(fname)
            
  return listPathJson
