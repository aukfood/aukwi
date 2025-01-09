import csv, json, displayVers, displayUrl, getPlugins, takeAppInDocker, subprocess

listNameOfDock = takeAppInDocker.getNameOnlyOffice()
listNameCollabora = takeAppInDocker.getNameCollabora()
listNameCalcom = takeAppInDocker.getNameCalcom()
listUrl = displayUrl.displayUrl()
listDb = displayUrl.listDbName
yp = getPlugins.getPlug(listDb, listUrl)
listVersJson = displayVers.displayVersionJson()
servername = subprocess.getoutput('hostname -f').strip()
listVersions = displayVers.displayVersion()

# Fonction pour écrire les données dans un fichier CSV
def writeCsv(filename, header, rows):
    with open(filename, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(header)
        writer.writerows(rows)

# Fonction pour créer et remplir le fichier "inventory.csv"
def createInventory():
    header = ["Server Name", "Url", "Cms", "Plugin or not", "Version"]
    rows = []
    
    # Ajout des données pour OnlyOffice, Collabora et Calcom (Docker)
    if len(listNameOfDock) > 0 and listNameOfDock[0] != '':
        for i in range(len(listNameOfDock)):
            rows.append([servername, takeAppInDocker.getDockerUrls(listNameOfDock)[i], "OnlyOffice", "Not a plugin", takeAppInDocker.getVersOnlyOffice()[i]])
    
    if len(listNameCollabora) > 0 and listNameCollabora[0] != '':        
        for i in range(len(listNameCollabora)):
            rows.append([servername, takeAppInDocker.getDockerUrls(listNameCollabora)[i], "Collabora", "Not a plugin", takeAppInDocker.getVersCollabora()[i]])

    if len(listNameCalcom) > 0 and listNameCalcom[0] != '':
        for i in range(len(listNameCalcom)):
            rows.append([servername, takeAppInDocker.getDockerUrls(listNameCalcom)[i], "Calcom", "Not a plugin", takeAppInDocker.getVersCalcom()[i]])
    
    for i in range(len(listUrl)):
        version = listVersions[i]
        cms = displayVers.listCms[i]
        url = listUrl[i]
        serv = servername
        rows.append([serv, url, cms, "Not a plugin", version])
        if cms == "NextCloud":
            dbName = next((db for db in listDb if db in url), None)
            if dbName and dbName in yp:
                for status in ['enabled', 'disabled']:
                    for y in range(len(yp[dbName][status])):
                        rows.append([serv, url, yp[dbName][status][y][0], f"Plugin ({status})", yp[dbName][status][y][1]])

    for i in range(len(listVersJson)):
        rows.append([servername, displayUrl.displayUrlJson()[i], displayVers.listCmsJson[i], "Not a plugin", listVersJson[i]])

    writeCsv('inventory.csv', header, rows)

# Fonction pour créer et remplir le fichier "inventory.json"
def createInventoryJson():
    inventory = []

    if len(listNameOfDock) > 0 and listNameOfDock[0] != '':
        for i in range(len(listNameOfDock)):
            inventory.append({
                "Server Name": servername,
                "Url": takeAppInDocker.getDockerUrls(listNameOfDock)[i],
                "Cms": "OnlyOffice",
                "Plugin or not": "Not a plugin",
                "Version": takeAppInDocker.getVersOnlyOffice()[i]
            })

    if len(listNameCollabora) > 0 and listNameCollabora[0] != '':
        for i in range(len(listNameCollabora)):
            inventory.append({
                "Server Name": servername,
                "Url": takeAppInDocker.getDockerUrls(listNameCollabora)[i],
                "Cms": "Collabora",
                "Plugin or not": "Not a plugin",
                "Version": takeAppInDocker.getVersCollabora()[i]
            })

    if len(listNameCalcom) > 0 and listNameCalcom[0] != '':
        for i in range(len(listNameCalcom)):
            inventory.append({
                "Server Name": servername,
                "Url": takeAppInDocker.getDockerUrls(listNameCalcom)[i],
                "Cms": "Calcom",
                "Plugin or not": "Not a plugin",
                "Version": takeAppInDocker.getVersCalcom()[i]
            })

    for i in range(len(listUrl)):
        version = listVersions[i]
        cms = displayVers.listCms[i]
        url = listUrl[i]
        serv = servername
        inventory.append({
            "Server Name": serv,
            "Url": url,
            "Cms": cms,
            "Plugin or not": "Not a plugin",
            "Version": version
        })
        if cms == "NextCloud":
            dbName = next((db for db in listDb if db in url), None)
            if dbName and dbName in yp:
                for status in ['enabled', 'disabled']:
                    for y in range(len(yp[dbName][status])):
                        inventory.append({
                            "Server Name": serv,
                            "Url": url,
                            "Cms": yp[dbName][status][y][0],
                            "Plugin or not": f"Plugin ({status})",
                            "Version": yp[dbName][status][y][1]
                        })

    for i in range(len(listVersJson)):
        inventory.append({
            "Server Name": servername,
            "Url": displayUrl.displayUrlJson()[i],
            "Cms": displayVers.listCmsJson[i],
            "Plugin or not": "Not a plugin",
            "Version": listVersJson[i]
        })

    with open('inventory.json', 'w') as json_file:
        json.dump(inventory, json_file, indent=4)

