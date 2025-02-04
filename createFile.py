import json
import displayVers
import displayUrl
import getPlugins
import takeAppInDocker
import subprocess
import re

def createAndSend(glpi_url):
    """
    Crée l'inventaire JSON en local, ajoute les sites en tant que logiciels, et l'envoie à GLPI.
    """

    def print_progress(step, total_steps):
        progress = (step / total_steps) * 100
        print(f"\rProgression: {progress:.2f}% [{'#' * int(progress // 2)}{' ' * (50 - int(progress // 2))}]", end="", flush=True)

    total_steps = 4
    current_step = 0

    # Préparation des données
    print_progress(current_step, total_steps)
    Dockers = takeAppInDocker.getAllDockers()
    current_step += 1
    print_progress(current_step, total_steps)
    sites_info = displayUrl.getAllSites()
    current_step += 1
    print_progress(current_step, total_steps)
    listVersJson = displayVers.displayVersionJson()
    listVersions = displayVers.displayVersion()
    current_step += 1

    # # Étape 1 : Générer l'inventaire local au format JSON
    # print_progress(current_step, total_steps)
    # subprocess.getoutput("glpi-inventory --json > inventory.json")
    # current_step += 1

    # # Étape 2 : Modifier le fichier JSON pour ajouter les sites en tant que logiciels
    # print_progress(current_step, total_steps)
    # with open("inventory.json", "r") as file:
    #     inventory = json.load(file)
    # inventory["content"]["softwares"] = []

    # # Ajouter les sites en tant que logiciels
    # for docker in Dockers:
    #     new_software = {
    #         "arch": "all",
    #         "name": docker['url'],
    #         "publisher": "AukFood",
    #         "version": docker['version'],
    #         "system_category": docker['cms']
    #     }
    #     inventory["content"]["softwares"].append(new_software)

    # for site in sites_info:
    #     new_software = {
    #         "arch": "all",
    #         "name": site['url'],
    #         "publisher": "AukFood",
    #         "version": site['version'],
    #         "system_category": site['type']
    #     }
    #     inventory["content"]["softwares"].append(new_software)
    #     for status in site['plugins'].keys():
    #         for plugin in site['plugins'][status]:
    #             new_software = {
    #                 "arch": "all",
    #                 "name": plugin['name'],
    #                 "publisher": "AukFood",
    #                 "version": plugin['version'],
    #                 "system_category": f"Plugin ({status})"
    #             }
    #             inventory["content"]["softwares"].append(new_software)

    # for i in range(len(listVersJson)):
    #     new_software = {
    #         "arch": "all",
    #         "name": displayUrl.displayUrlJson()[i],
    #         "publisher": "AukFood",
    #         "version": listVersJson[i],
    #         "system_category": displayVers.listCmsJson[i]
    #     }
    #     inventory["content"]["softwares"].append(new_software)

    # # Spécifier l'entité (client)
    # with open("/etc/ansible/facts.d/client-server.fact", "r") as facts:
    #     for line in facts:
    #         if line.startswith('client'):
    #             client = line.split('=')[1].strip()
    #             break
    # if not client:
    #     client = "Clients"

    # # Enregistrer le fichier JSON modifié
    # print_progress(current_step, total_steps)
    # with open("inventory.json", "w") as file:
    #     json.dump(inventory, file, indent=4)
    # current_step += 1

    # # Étape 3 : Soumettre l'inventaire mis à jour à GLPI
    # print_progress(current_step, total_steps)
    # print("\n")
    # subprocess.run(["glpi-agent", "--force", f"--server={glpi_url}", f"--tag={re.sub(r'[^A-Za-z0-9]', '', client)}"])

    # print("\nInventaire terminé et envoyé à GLPI.")
    
    print(sites_info)