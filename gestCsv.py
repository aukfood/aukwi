import csv, os, fnmatch, displayVers, SearchVersionFile, displayUrl, getPlugins, subprocess, takeAppInDocker, displayVersRock, displayUrlRock

listNameOfDock = takeAppInDocker.getNameOnlyOffice()
listNameCollabora = takeAppInDocker.getNameCollabora()
listUrl = displayUrl.displayUrl()
listDb = displayUrl.listDbName
yp = getPlugins.getPlug(listDb, listUrl)
listVersJson = displayVers.displayVersionJson()
listVersRock = displayVersRock.displayVersionRocket()

#Création et remplissage du fichier "inventory.csv"
def createInventory():  
  header = ["Server Name", "Url", "Cms", "Plugin or not", "Version" ]

  with open('inventory.csv', "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(header)
    for i in range(len(listNameOfDock)):
      servOf = takeAppInDocker.getServOnlyOffice()[i]
      nameOf = listNameOfDock[i]
      versionOf = takeAppInDocker.getVersOnlyOffice()[i]
      writer.writerow([servOf, nameOf, "OnlyOffice", "Not a plugin", versionOf])
    for i in range(len(listUrl)):
      version = displayVers.displayVersion()[i]
      cms = displayVers.listCms[i]
      url = listUrl[i]
      serv = displayUrl.displayServ()[i]
      writer.writerow([serv, url, cms, "Not a plugin", version])
      if cms == "NextCloud":
        listNamePlug = getPlugins.listNamePlg(yp)
        for y in range(len(listNamePlug)):
          cmsP = listNamePlug[y]
          versionP = getPlugins.listVersPlg(yp)[y]
          writer.writerow([serv, url, cmsP, "Plugin", versionP])
    for i in range(len(listVersJson)):
      servJ = displayUrl.displayServJson()[i]
      urlJ = displayUrl.displayUrlJson()[i]
      cmsJ = displayVers.listCmsJson[i]
      versionJ = displayVers.displayVersionJson()[i]
      writer.writerow([servJ, urlJ, cmsJ, "Not a plugin", versionJ])
    for i in range(len(listNameCollabora)):
      servCo = takeAppInDocker.getServCollabora()[i]
      nameCo = listNameCollabora[i]
      versionCo = takeAppInDocker.getVersCollabora()[i]
      writer.writerow([servCo, nameCo, "Collabora", "Not a plugin", versionCo])
   # for i in range(len(listVersRock)):
    #  servR = displayUrlRock.displayServRocket()[i]
     # urlR = "salut"
      #cmsR = displayVersRock.listRocket[i]
      #versionR = listVersRock[i]
      #writer.writerow([servR, urlR, cmsR, "Not a plugin", versionR])  
      
