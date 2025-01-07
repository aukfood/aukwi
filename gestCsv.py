import csv, json, displayVers, displayUrl, getPlugins, takeAppInDocker

listNameOfDock = takeAppInDocker.getNameOnlyOffice()
listNameCollabora = takeAppInDocker.getNameCollabora()
listNameCalcom = takeAppInDocker.getNameCalcom()
listUrl = displayUrl.displayUrl()
listDb = displayUrl.listDbName
yp = getPlugins.getPlug(listDb, listUrl)
listVersJson = displayVers.displayVersionJson()

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

    for i in range(len(listNameOfDock)):
        rows.append([takeAppInDocker.getServOnlyOffice()[i], listNameOfDock[i], "OnlyOffice", "Not a plugin", takeAppInDocker.getVersOnlyOffice()[i]])

    for i in range(len(listUrl)):
        version = displayVers.displayVersion()[i]
        cms = displayVers.listCms[i]
        url = listUrl[i]
        serv = displayUrl.displayServ()[i]
        rows.append([serv, url, cms, "Not a plugin", version])
        if cms == "NextCloud":
            listNamePlug = getPlugins.listNamePlg(yp)
            for y in range(len(listNamePlug)):
                rows.append([serv, url, listNamePlug[y], "Plugin", getPlugins.listVersPlg(yp)[y]])

    for i in range(len(listVersJson)):
        rows.append([displayUrl.displayServJson()[i], displayUrl.displayUrlJson()[i], displayVers.listCmsJson[i], "Not a plugin", listVersJson[i]])

    for i in range(len(listNameCollabora)):
        rows.append([takeAppInDocker.getServCollabora()[i], listNameCollabora[i], "Collabora", "Not a plugin", takeAppInDocker.getVersCollabora()[i]])

    for i in range(len(listNameCalcom)):
        rows.append([takeAppInDocker.getServCalcom()[i], listNameCalcom[i], "Calcom", "Not a plugin", takeAppInDocker.getVersCalcom()[i]])

    writeCsv('inventory.csv', header, rows)

# Fonction pour créer et remplir le fichier "inventory.json"
def createInventoryJson():
    inventory = []

    for i in range(len(listNameOfDock)):
        inventory.append({
            "Server Name": takeAppInDocker.getServOnlyOffice()[i],
            "Url": listNameOfDock[i],
            "Cms": "OnlyOffice",
            "Plugin or not": "Not a plugin",
            "Version": takeAppInDocker.getVersOnlyOffice()[i]
        })

    for i in range(len(listUrl)):
        version = displayVers.displayVersion()[i]
        cms = displayVers.listCms[i]
        url = listUrl[i]
        serv = displayUrl.displayServ()[i]
        inventory.append({
            "Server Name": serv,
            "Url": url,
            "Cms": cms,
            "Plugin or not": "Not a plugin",
            "Version": version
        })
        if cms == "NextCloud":
            listNamePlug = getPlugins.listNamePlg(yp)
            for y in range(len(listNamePlug)):
                inventory.append({
                    "Server Name": serv,
                    "Url": url,
                    "Cms": listNamePlug[y],
                    "Plugin or not": "Plugin",
                    "Version": getPlugins.listVersPlg(yp)[y]
                })

    for i in range(len(listVersJson)):
        inventory.append({
            "Server Name": displayUrl.displayServJson()[i],
            "Url": displayUrl.displayUrlJson()[i],
            "Cms": displayVers.listCmsJson[i],
            "Plugin or not": "Not a plugin",
            "Version": listVersJson[i]
        })

    for i in range(len(listNameCollabora)):
        inventory.append({
            "Server Name": takeAppInDocker.getServCollabora()[i],
            "Url": listNameCollabora[i],
            "Cms": "Collabora",
            "Plugin or not": "Not a plugin",
            "Version": takeAppInDocker.getVersCollabora()[i]
        })

    for i in range(len(listNameCalcom)):
        inventory.append({
            "Server Name": takeAppInDocker.getServCalcom()[i],
            "Url": listNameCalcom[i],
            "Cms": "Calcom",
            "Plugin or not": "Not a plugin",
            "Version": takeAppInDocker.getVersCalcom()[i]
        })

    with open('inventory.json', 'w') as json_file:
        json.dump(inventory, json_file, indent=4)

