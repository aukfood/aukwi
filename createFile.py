import json
import displayVers
import displayUrl
import getPlugins
import takeAppInDocker
import subprocess
import re

def createAndSend():
    """
    Crée l'inventaire JSON en local, ajoute les sites en tant que logiciels, et l'envoie à GLPI.
    """

    def print_progress(step, total_steps):
        progress = (step / total_steps) * 100
        print(f"\rProgression: {progress:.2f}% [{'#' * int(progress // 2)}{' ' * (50 - int(progress // 2))}]", end="", flush=True)

    total_steps = 6
    current_step = 0

    # Préparation des données
    print_progress(current_step, total_steps)
    Dockers = takeAppInDocker.getAllDockers()
    current_step += 1
    print_progress(current_step, total_steps)
    listUrl = displayUrl.displayUrl()
    current_step += 1
    print_progress(current_step, total_steps)
    listDb = displayUrl.listDbName
    yp = getPlugins.getPlug(listDb, listUrl)
    current_step += 1
    print_progress(current_step, total_steps)
    listVersJson = displayVers.displayVersionJson()
    listVersions = displayVers.displayVersion()
    current_step += 1

    # Étape 1 : Générer l'inventaire local au format JSON
    print_progress(current_step, total_steps)
    subprocess.getoutput("glpi-inventory --json > inventory.json")
    current_step += 1

    # Étape 2 : Modifier le fichier JSON pour ajouter les sites en tant que logiciels
    print_progress(current_step, total_steps)
    with open("inventory.json", "r") as file:
        inventory = json.load(file)
    inventory["content"]["softwares"]= []

    # Ajouter les sites en tant que logiciels
    for docker in Dockers:
        new_software = {
            "arch": "all",
            "name": docker['url'],
            "publisher": "AukFood",
            "version": docker['version'],
            "system_category": docker['cms']
        }
        inventory["content"]["softwares"].append(new_software)

    for i in range(len(listUrl)):
        version = listVersions[i]
        cms = displayVers.listCms[i]
        url = listUrl[i]
        new_software = {
            "arch": "all",
            "name": url,
            "publisher": "AukFood",
            "version": version,
            "system_category": cms
        }
        inventory["content"]["softwares"].append(new_software)
        if cms == "NextCloud":
            dbName = next((db for db in listDb if db in url), None)
            if dbName and dbName in yp:
                for status in ['enabled', 'disabled']:
                    for y in range(len(yp[dbName][status])):
                        new_software = {
                            "arch": "all",
                            "name": yp[dbName][status][y][0],
                            "publisher": "AukFood",
                            "version": yp[dbName][status][y][1],
                            "system_category": f"Plugin ({status})"
                        }
                        inventory["content"]["softwares"].append(new_software)
        elif cms == "Wordpress":
            plugins = getPlugins.getPlugWP(url)
            for status in plugins.keys():
                for y in range(len(plugins[status])):
                    new_software = {
                        "arch": "all",
                        "name": plugins[status][y]['name'],
                        "publisher": "AukFood",
                        "version": plugins[status][y]['version'],
                        "system_category": f"Plugin ({status})"
                    }
                    inventory["content"]["softwares"].append(new_software)

    for i in range(len(listVersJson)):
        new_software = {
            "arch": "all",
            "name": displayUrl.displayUrlJson()[i],
            "publisher": "AukFood",
            "version": listVersJson[i],
            "system_category": displayVers.listCmsJson[i]
        }
        inventory["content"]["softwares"].append(new_software)

    # Spécifier l'entité (client)
    with open("/etc/ansible/facts.d/client-server.fact", "r") as facts:
        for line in facts:
            if line.startswith('client'):
                client = line.split('=')[1].strip()
                break
    if not client:
        client ="Clients"

    # Enregistrer le fichier JSON modifié
    print_progress(current_step, total_steps)
    with open("inventory.json", "w") as file:
        json.dump(inventory, file, indent=4)
    current_step += 1

    # Étape 3 : Soumettre l'inventaire mis à jour à GLPI
    print_progress(current_step, total_steps)
    print("\n")
    subprocess.run(["glpi-agent", "--force", f"--tag={re.sub(r'[^A-Za-z0-9]', '', client)}"])

    print("\nInventaire terminé et envoyé à GLPI.")