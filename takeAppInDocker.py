import subprocess, string, time

#Fonction pour r�cup�rer tous les noms des OnlyOffice dans les dockers
def getNameOnlyOffice():
    of = subprocess.getoutput('docker ps -a --format \'{{.Names}}\' | grep onlyoffice').split('\n')
    of = [x.split('\t')[0] for x in of]

    ofList = []
    for Name in of:
        ofList.append(Name)


    return (ofList)

#Fonction pour r�cup�rer le serveur des OnlyOffice r�cup�r�s avec getNameOnlyOffice
def getServOnlyOffice():
    nameList = getNameOnlyOffice()
    for i in range(len(nameList)):
      serv = subprocess.getoutput('docker exec -it '+ nameList[i] +' hostname -f').split('\n')
      serv = [x.split('\t')[0] for x in serv]

    servList = []
    for Name in serv:
        servList.append(Name)


    return (servList)

#Fonction pour r�cup�rer la version des OnlyOffice r�cup�r�s avec getNameOnlyOffice
def getVersOnlyOffice():
    
    ofList = getNameOnlyOffice()
    for i in range(len(ofList)):
      vers = subprocess.getoutput('docker exec -it '+ofList[i]+' grep Version /var/log/onlyoffice/documentserver/docservice/out.log |tail -n 1').split()
      vers = [x.split('\t')[0] for x in vers]

    versList = []
    for Name in vers:
      if Name == "Version:":
        version = vers.index(Name)+1
        versList.append(vers[version])
  
    return(versList)

#Fonction pour r�cup�rer tous les noms des Collabora dans les dockers
def getNameCollabora():
    col = subprocess.getoutput('docker ps -a --format \'{{.Names}}\' | grep collabora').split('\n')
    col = [x.split('\t')[0] for x in col]

    colList = []
    for Name in col:
        colList.append(Name)
  
    return (colList)
    
#Fonction pour r�cup�rer la version des Collabora r�cup�r�s avec getNameCollabora
def getVersCollabora():
    
    ofList = getNameCollabora()
    for i in range(len(ofList)):
      vers = subprocess.getoutput('docker exec -it '+ofList[i]+' cat /var/lib/dpkg/status').split()
      vers = [x.split('\t')[0] for x in vers]

      versList = []
      for Name in vers:
        if Name == "Office":
          version = vers.index(Name)+1
          versList.append(vers[version])
          break
    
    return(versList)

#Fonction pour r�cup�rer le serveur des Collabora r�cup�r�s avec getNameCollabora    
def getServCollabora():
    
  nameList = getNameCollabora()
  for i in range(len(nameList)):
    serv = subprocess.getoutput('docker exec -it '+ nameList[i] +' hostname -f').split('\n')
    serv = [x.split('\t')[0] for x in serv]

    servList = []
    for Name in serv:
      servList.append(Name)


  return (servList)