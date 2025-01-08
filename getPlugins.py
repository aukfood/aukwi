import subprocess, re

listVersPlug = []
listNamePlug = []

# Fonction qui récupère nom + version des plugins dans une liste
def getPlug(listDbName, listUrl):
    plugList = []
    for i in range(len(listDbName)):
        plug = subprocess.getoutput(f'sudo -u {listDbName[i]} php8.2 /var/www/{listUrl[i]}/www/occ app:list').split()
        plugList.extend(plug)
    return plugList

# Fonction qui va permettre de trier le nom + version des plugins pour récupérer que le nom 
def only_letters(input_str):
    return re.match("^[a-zA-Z:]+$", input_str)

# Fonction qui va permettre de récupérer que la version des plugins pour récupérer que la version
def only_numbers(input_str):
    return re.match(r'\b\d+\.\d+\b|\b\d+\b', input_str)

# Fonction qui va permettre de récupérer le nom des plugins dans une liste    
def listNamePlg(listPlug):
    listNamePlug = []
    for plug in listPlug:
        if only_letters(plug):
            listNamePlug.append(plug.replace(":", ""))
    return listNamePlug

# Fonction qui va permettre de récupérer la version des plugins dans une liste
def listVersPlg(listPlug):
    return [plug for plug in listPlug if only_numbers(plug)]