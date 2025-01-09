import subprocess, os, re, json

# Fonction pour récupérer tous les noms des containers Docker correspondant à un pattern
def getDockerNames(pattern):
    return subprocess.getoutput(f'docker ps -a --format \'{{{{.Names}}}}\' | grep {pattern}').split('\n')

# Fonction pour récupérer la version des containers Docker
def getDockerVersions(nameList, packageName):
    versions = []
    for name in nameList:
        status = subprocess.getoutput(f'docker exec -it {name} cat /var/lib/dpkg/status').split()
        try:
            packageIndex = status.index(packageName)
            status = status[packageIndex:]
            versionIndex = status.index("Version:") + 1
            versions.append(status[versionIndex])
        except ValueError:
            versions.append("Unknown")
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
    # Retourner uniquement les vhosts sous forme de liste
    return list(vhosts.values())

# Fonction pour récupérer tous les noms des OnlyOffice dans les dockers
def getNameOnlyOffice():
    return getDockerNames('onlyoffice')

# Fonction pour récupérer la version des OnlyOffice récupérés avec getNameOnlyOffice
def getVersOnlyOffice():
    return getDockerVersions(getNameOnlyOffice(), "onlyoffice-documentserver")

# Fonction pour récupérer tous les noms des Collabora dans les dockers
def getNameCollabora():
    return getDockerNames('collabora')

# Fonction pour récupérer la version des Collabora récupérés avec getNameCollabora
def getVersCollabora():
    return getDockerVersions(getNameCollabora(), "collaboraoffice")

# Fonction pour récupérer tous les noms des Calcom dans les dockers
def getNameCalcom():
    return getDockerNames('calcom')


# Fonction pour récupérer la version des Calcom récupérés avec getNameCalcom
def getVersCalcom():
    return getDockerVersions(getNameCalcom(), "calcom")