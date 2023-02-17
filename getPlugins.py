import subprocess, string, time, displayUrl, re

listVersPlug = []
listNamePlug = []
listDashPlus = []

#Fonction qui récupère nom + version des plugins dans une liste
def getPlug(listDbName, listUrl):

  for i in range(len(listDbName)):
    plug = subprocess.getoutput('sudo -u'+ listDbName[i]+ ' php8.1 /var/www/'+ listUrl[i] +'/www/occ app:list').split()
    plug = [x.split('\t')[0] for x in plug]

    plugNameList = []
    plugList = []
    for Name in plug:
      plugList.append(Name)
  
    return(plugList)

#Fonction qui va permettre de trier le nom + version des plugins pour récupérer que le nom 
def only_letters(input_str):
    return re.match("^[a-zA-Z:]+$", input_str)
    
#Fonction qui va permettre de récupérer que la version des plugins pour récupérer que la version
def only_numbers(input_str):
    return re.match(r'\b\d+\.\d+\b|\b\d+\b', input_str)

#Fonction qui va permettre de récupérer le nom des plugins dans une liste    
def listNamePlg(listPlug):

  listNamePlug = []
  for y in range(len(listPlug)):
         if listPlug[y] == "-":
           y = y + 1
         elif listPlug[y] == "Enabled:":
           y = y + 1
         elif listPlug[y] == "Disabled:":
           break
         elif only_letters(listPlug[y]):
           if ":" in listPlug[y]:
             new_text = listPlug[y].replace(":", "")
             listNamePlug.append(new_text)
  return listNamePlug

#Fonction qui va permettre de récupérer la version des plugins dans une liste
def listVersPlg(listPlug):

  listVersPlug = []
  for y in range(len(listPlug)):
         if listPlug[y] == "-":
           y = y + 1
         elif listPlug[y] == "Enabled:":
           y = y + 1
         elif listPlug[y] == "Disabled:":
           break
         elif only_numbers(listPlug[y]):     
           listVersPlug.append(listPlug[y])
  return listVersPlug