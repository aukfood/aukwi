import subprocess, os, re, json

# Fonction pour récupérer tous les noms des containers Docker correspondant à un pattern
def getDockerNames():
    docker_names = subprocess.getoutput(f'docker ps -a --format \'{{{{.Names}}}}\'').split('\n')
    docker_info = {}
    for name in docker_names:
        try:
            # Récupérer les informations du conteneur
            output = subprocess.getoutput(f'docker inspect {name}')
            container_info = json.loads(output)
            
            # Extraire l'image utilisée par le conteneur
            docker_image = container_info[0].get("Config", {}).get("Image", "unknown")
            
            # Déterminer le type de Docker à partir de l'image
            docker_type = docker_image.split('/')[0].split('.')[0]
            
            docker_info[name] = docker_type
        except Exception as e:
            print(f"Erreur lors de l'inspection du conteneur {name} : {str(e)}")
            docker_info[name] = "Unknown"
    return docker_info

# Fonction pour récupérer la version des containers Docker
def getDockerVersions(nameList):
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
                versions[name]=status[version_index]
            else:
                versions[name]="Unknown"
        except ValueError:
            versions[name]="Unknown"
    return versions

# Fonction pour récupérer les URLs des applications Docker
def getDockerUrls(container_names, apache_config_path="/etc/apache2/sites-enabled"):
    vhosts = {}  # Dictionnaire pour stocker les correspondances conteneur -> vhost

    # Étape 1 : Inspecter les conteneurs Docker
    container_ports = {}
    for container in container_names:
        try:
            # Récupérer les informations du conteneur
            output = subprocess.getoutput(f'docker inspect {container}')
            container_info = json.loads(output)
            
            # Extraire les ports exposés
            ports = container_info[0].get("NetworkSettings", {}).get("Ports", {})
            for port, mappings in ports.items():
                if mappings:  # Si le port est mappé
                    container_ports[container] = mappings[0]['HostPort']
            if container not in container_ports:
                container_ports[container] = "Unknown"
        except Exception as e:
            print(f"Erreur lors de l'inspection du conteneur {container} : {str(e)}")
    # Étape 2 : Associer les ports aux vhosts Apache
    for root, dirs, files in os.walk(apache_config_path):
        for file in files:
            if file.endswith(".conf"):  # Analyser uniquement les fichiers .conf
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    
                    # Extraire les ServerName
                    server_names = re.findall(r"ServerName\s+([^\s]+)", content)
                    
                    # Extraire les ports dans ProxyPass, même avec du texte avant ou après
                    proxy_passes = re.findall(r"ProxyPass.*https?://127\.0\.0\.1:(\d+)", content)
                    
                    # Associer les vhosts aux conteneurs en fonction des ports
                    for server_name in server_names:
                        for container, port in container_ports.items():
                            if port == "Unknown":
                                vhosts[container] = "Unknown"
                            elif port in proxy_passes:  # Si le port du conteneur correspond
                                vhosts[container] = server_name
    return vhosts

def getAllDockers():    
    # Récupérer les noms des containers
    docker_names = getDockerNames()
    # Récupérer les versions des containers
    docker_versions = getDockerVersions(docker_names)
    
    # Récupérer les URLs des containers
    docker_urls = getDockerUrls(list(docker_names.keys()))

    # Combiner les informations dans une liste de dictionnaires
    dockers_info = []
    for name,type in docker_names.items():
        dockers_info.append({
            "name": name,
            "cms": type,
            "version": docker_versions[name],
            "url": docker_urls[name]
        })
    # print(dockers_info)
    return dockers_info