import subprocess

# Fonction pour récupérer tous les noms des OnlyOffice dans les dockers
def getNameOnlyOffice():
    of = subprocess.getoutput('docker ps -a --format \'{{.Names}}\' | grep onlyoffice').split('\n')
    of = [x.split('\t')[0] for x in of]
    return of

# Fonction pour récupérer le serveur des OnlyOffice récupérés avec getNameOnlyOffice
def getServOnlyOffice():
    nameList = getNameOnlyOffice()
    servList = []
    for name in nameList:
        serv = subprocess.getoutput(f'docker exec -it {name} hostname -f').strip()
        servList.append(serv)
    return servList

# Fonction pour récupérer la version des OnlyOffice récupérés avec getNameOnlyOffice
def getVersOnlyOffice():
    ofList = getNameOnlyOffice()
    for of in ofList:
        vers = subprocess.getoutput(f'docker exec -it {of} cat /var/lib/dpkg/status').split()
        vers = [x.split('\t')[0] for x in vers]

    versList = []
    for Name in vers:
        if Name == "Version:":
            version = vers.index(Name)+1
            versList.append(vers[version])
    return(versList)


# Fonction pour récupérer tous les noms des Collabora dans les dockers
def getNameCollabora():
    col = subprocess.getoutput('docker ps -a --format \'{{.Names}}\' | grep collabora').split('\n')
    col = [x.split('\t')[0] for x in col]
    return col

# Fonction pour récupérer la version des Collabora récupérés avec getNameCollabora
def getVersCollabora():
    ofList = getNameCollabora()
    for of in ofList:
      vers = subprocess.getoutput(f'docker exec -it {of} cat /var/lib/dpkg/status').split()
      vers = [x.split('\t')[0] for x in vers]

      versList = []
      for Name in vers:
        if Name == "Office":
          version = vers.index(Name)+1
          versList.append(vers[version])
          break
    
    return(versList)


# Fonction pour récupérer le serveur des Collabora récupérés avec getNameCollabora    
def getServCollabora():
    nameList = getNameCollabora()
    servList = []
    for name in nameList:
        serv = subprocess.getoutput(f'docker exec -it {name} hostname -f').strip()
        servList.append(serv)
    return servList