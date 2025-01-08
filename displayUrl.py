import SearchUrl, subprocess

listDbName = []

# Fonction qui cherche dans un fichier si il contient les informations liées à l'url des cms (Wordpress, Moodle, NextCloud)
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
            if '.' in line[start:]:
                end = line.index('.', start)
                dbname = line[start:end]
                listDbName.append(dbname)
    return listUrlCms

# Fonction qui cherche dans un fichier si il contient les informations liées à l'url du cms (PhpMyAdmin)     
def TakeUrlCmsJson(fileConfig):
    listUrlCmsJson = []
    fileConfig = fileConfig.split('\n')
    for line in fileConfig:
        if line.startswith('  ServerName '):
            start = line.index('  ServerName ') + len('  ServerName ')
            end = line.index('ovh', start) + 3
            url = line[start:end]
            listUrlCmsJson.append(url)
    return listUrlCmsJson

# Fonction qui crée une condition pour trier les fichiers contenant les url
def trueOrNot(fileConfig):
    fileConfig = fileConfig.split('\n')
    for line in fileConfig:
        if line.startswith('    0 => '):
            return True
        if line.startswith('    0 => \''):
            return True
    return False

# Fonction qui crée une condition pour trier les fichiers contenant les url
def trueOrNotJson(fileConfig):
    fileConfig = fileConfig.split('\n')
    for line in fileConfig:
        if line.startswith('  ServerName '):
            return True
    return False

# Récupération des url des cms (Moodle, Wordpress, NextCloud) dans une liste
# def displayServ():
#     currentpath = "/" # chemin vers répertoire courant
#     pathOfFileConf = SearchUrl.SearchConf(currentpath)
#     servList = []

#     for path in pathOfFileConf:
#         with open(path, 'r') as file:
#             fileConfig = file.read()
#             if trueOrNot(fileConfig):
#                 serv = subprocess.getoutput(f'sudo {path} | hostname -f').split('\n')
#                 serv = [x.split('\t')[0] for x in serv]
#                 servList.extend(serv)
#     return servList

# Récupération des url du cms (PhpMyAdmin) dans une liste 
# def displayServJson():
#     currentpath = "/" # chemin vers répertoire courant
#     pathOfFileConf = SearchUrl.SearchConfJson(currentpath)
#     servListJson = []

#     for path in pathOfFileConf:
#         with open(path, 'r') as file:
#             fileConfig = file.read()
#             if trueOrNotJson(fileConfig):
#                 serv = subprocess.getoutput(f'sudo {path} | hostname -f').split('\n')
#                 serv = [x.split('\t')[0] for x in serv]
#                 servListJson.extend(serv)
#     return servListJson

def displayUrl():
    currentpath = "/" # chemin vers répertoire courant
    pathOfFileConf = SearchUrl.SearchConf(currentpath)
    listUrl = []

    for path in pathOfFileConf:
        with open(path, 'r') as file:
            fileConfig = file.read()
            listUrl += TakeUrlCms(fileConfig)
    return listUrl

def displayUrlJson():
    currentpath = "/" # chemin vers répertoire courant
    pathOfFileConfJson = SearchUrl.SearchConfJson(currentpath)
    listUrlJson = []

    for path in pathOfFileConfJson:
        if "myadmin" in path:
            with open(path, 'r') as file:
                fileConfig = file.read()
                listUrlJson += TakeUrlCmsJson(fileConfig)
    return listUrlJson