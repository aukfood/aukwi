import subprocess
import json

def getAllDockers(configs):
    """
    Récupère toutes les informations sur les conteneurs Docker, y compris les noms, versions et URLs.
    """
    # Récupérer les noms des containers
    docker_names = getDockerNames()
    # Récupérer les versions des containers
    docker_versions = getDockerVersions(docker_names)
    
    # Récupérer les URLs des containers
    docker_urls = getDockerUrls(list(docker_names.keys()), configs)

    # Combiner les informations dans une liste de dictionnaires
    dockers_info = []
    for name, type in docker_names.items():
        if type != "Unknown" and docker_urls[name] != "Unknown":
            dockers_info.append({
                    "name": name,
                    "type": type,
                    "version": docker_versions[name],
                    "url": docker_urls[name]
                })
    return dockers_info

# Fonction pour récupérer tous les noms des containers Docker correspondant à un pattern
def getDockerNames():
    """
    Récupère les noms des conteneurs Docker et détermine leur type à partir de l'image et du nom du conteneur.
    """
    docker_names = subprocess.getoutput('docker ps -a --format \'{{.Names}}\'').split('\n')
    docker_info = {}
    for name in docker_names:
        try:
            # Récupérer les informations du conteneur
            output = subprocess.getoutput(f'docker inspect {name}')
            container_info = json.loads(output)
            
            # Extraire l'image utilisée par le conteneur
            docker_image = container_info[0].get("Config", {}).get("Image", "unknown")
            
            # Retirer "docker" des chaînes de caractères
            docker_image = docker_image.replace("docker", "")
            
            # Déterminer le type de Docker à partir de l'image et du nom du conteneur
            image_parts = docker_image.replace('.', '/').split('/')
            name_parts = name.replace("docker", "").split('_')
            
            common_word = next((word for word in image_parts if any(word in part for part in name_parts)), None)
            if common_word:
                docker_type = common_word
            else:
                docker_type = image_parts[0] if image_parts else name_parts[0]
            
            docker_info[name] = docker_type
            if docker_info[name] == "":
                docker_info[name] = "Unknown"
        except Exception as e:
            print(f"Erreur lors de l'inspection du conteneur {name} : {str(e)}")
    return docker_info

# Fonction pour récupérer la version des containers Docker
def getDockerVersions(nameList):
    """
    Récupère les versions des conteneurs Docker en lisant le fichier de statut des paquets.
    """
    versions = {}
    for name, type in nameList.items():
        status = subprocess.getoutput(f'docker exec -it {name} cat /var/lib/dpkg/status').split()
        try:
            # Trouver le package correspondant dans le status
            package_name = next((pkg for pkg in status if type in pkg), None)
            if package_name:
                package_index = status.index(package_name)
                status = status[package_index:]
                version_index = status.index("Version:") + 1
                versions[name] = status[version_index]
            else:
                versions[name] = "Unknown"
        except (ValueError, IndexError):
            versions[name] = "Unknown"
    return versions

# Fonction pour récupérer les URLs des applications Docker
def getDockerUrls(container_names, configs):
    """
    Récupère les URLs des applications Docker en associant les ports des conteneurs aux vhosts Apache.
    """
    vhosts = {}  # Dictionnaire pour stocker les correspondances conteneur -> vhost

    # Étape 1 : Inspecter les conteneurs Docker
    container_ports = {}
    for container in container_names:
        vhosts[container] = "Unknown"
        try:
            # Récupérer les informations du conteneur
            output = subprocess.getoutput(f'docker inspect {container}')
            container_info = json.loads(output)
            
            # Extraire les ports exposés
            ports = container_info[0].get("NetworkSettings", {}).get("Ports", {})
            container_ports[container] = []
            for port, mappings in ports.items():
                if mappings:  # Si le port est mappé
                    for mapping in mappings:
                        if mapping['HostPort'] not in container_ports[container]:
                            container_ports[container].append(mapping['HostPort'])
        except Exception as e:
            print(f"Erreur lors de l'inspection du conteneur {container} : {str(e)}")
    
    # Étape 2 : Associer les ports aux vhosts
    for config in configs:
        if config['port']:  
            for container, ports in container_ports.items():
                if config['port'] in ports:
                    vhosts[container] = config['url']
    return vhosts


import fileUtils
print(getAllDockers(fileUtils.getWebsiteConfig()))