import csv, json, displayVers, displayUrl, getPlugins, takeAppInDocker, subprocess

Dockers = takeAppInDocker.getAllDockers()
listUrl = displayUrl.displayUrl()
listDb = displayUrl.listDbName
yp = getPlugins.getPlug(listDb, listUrl)
listVersJson = displayVers.displayVersionJson()
servername = subprocess.getoutput('hostname -f').strip()
listVersions = displayVers.displayVersion()

# Fonction pour écrire les données dans un fichier CSV
def writeCsv(filename, header, rows):
    """
    Écrit les données dans un fichier CSV.
    """
    with open(filename, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(header)
        writer.writerows(rows)

# Fonction pour créer et remplir le fichier "inventory.csv"
def createInventory():
    """
    Crée et remplit le fichier inventory.csv avec les informations des CMS et plugins.
    """
    header = ["Server Name", "Url", "Cms", "Plugin or not", "Version"]
    rows = []
    
    # Ajout des données pour tous les dockers
    for docker in Dockers:
        rows.append([servername, docker['url'], docker['cms'], "Not a plugin", docker['version']])
    
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
        elif cms == "Wordpress":
            plugins = getPlugins.getPlugWP(url)
            for status in plugins.keys():
                for y in range(len(plugins[status])):
                    rows.append([serv, url, plugins[status][y]['name'], f"Plugin ({status})",  plugins[status][y]['version']])

    for i in range(len(listVersJson)):
        rows.append([servername, displayUrl.displayUrlJson()[i], displayVers.listCmsJson[i], "Not a plugin", listVersJson[i]])

    writeCsv('inventory.csv', header, rows)

# Fonction pour créer et remplir le fichier "inventory.json"
def createInventoryJson():
    """
    Crée et remplit le fichier inventory.json avec les informations des CMS et plugins.
    """
    inventory = []

    # Ajout des données pour tous les dockers
    for docker in Dockers:
        inventory.append({
            "Server Name": servername,
            "Url": docker['url'],
            "Cms": docker['cms'],
            "Plugin or not": "Not a plugin",
            "Version": docker['version']
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
        elif cms == "Wordpress":
            plugins = getPlugins.getPlugWP(url)
            for status in plugins.keys():
                for y in range(len(plugins[status])):
                    inventory.append({
                        "Server Name": serv,
                        "Url": url,
                        "Cms": plugins[status][y]['name'],
                        "Plugin or not": f"Plugin ({status})",
                        "Version": plugins[status][y]['version']
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

