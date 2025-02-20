import subprocess
import json
import re

def getDockerFromPort(port):
    """
    Récupère les informations d'un conteneur Docker à partir d'un port.
    """
    try:
        # Trouver le conteneur qui utilise ce port
        cmd = f"docker ps --format '{{{{.Names}}}}' --filter publish={port}"
        container_name = subprocess.getoutput(cmd).strip()
        
        if not container_name:
            return None
            
        # Récupérer les informations du conteneur
        output = subprocess.getoutput(f'docker inspect {container_name}')
        container_info = json.loads(output)
        
        # Extraire l'image utilisée par le conteneur
        docker_image = container_info[0].get("Config", {}).get("Image", "unknown")
        docker_image = docker_image.replace("docker", "")
        
        # Déterminer le type de Docker
        image_parts = docker_image.replace('.', '/').split('/')
        name_parts = container_name.replace("docker", "").split('_')
        
        common_word = next((word for word in image_parts if any(word in part for part in name_parts)), None)
        docker_type = common_word if common_word else image_parts[0] if image_parts else name_parts[0]
        
        docker_type = docker_type.lower() if docker_type else "Unknown"
            
        return {"name": container_name, "type": docker_type}
    except Exception as e:
        print(f"Erreur lors de la recherche du conteneur pour le port {port}: {str(e)}")
        return None

def getDockerVersion(container_name, docker_type, port):
    """
    Récupère la version d'un conteneur Docker selon son type.
    """
    try:
        if "cal" in docker_type:
            version_output = subprocess.getoutput(f'docker exec {container_name} npm pkg get version --workspace=@calcom/web')
            if version_output:
                version_json = json.loads(version_output)
                return version_json["@calcom/web"]
                
        elif "mattermost" in docker_type:
            version_output = subprocess.getoutput(f'docker exec {container_name} mattermost version')
            if version_output:
                return version_output.split('\n')[0].split('Version:')[1].strip()
                
        elif "nextcloud" in docker_type:
            container_name = container_name.replace('-apache', '')
            main_container = subprocess.getoutput(f'docker ps --format "{{{{.Names}}}}" | grep "{container_name}" | grep "nextcloud-aio-nextcloud$"')
            if main_container:
                version_output = subprocess.getoutput(f'docker exec -u 33 {main_container} php occ status --output=json')
                if version_output:
                    version_json = json.loads(version_output)
                    return version_json.get('version', 'Unknown')

        elif "rocket" in docker_type:
            try:
                version_output = subprocess.getoutput(f'curl -s http://localhost:{port}/api/info')
                version_json = json.loads(version_output)
                return version_json.get('version', 'Unknown')
            except Exception as e:
                print(f"Erreur lors de la récupération de la version Rocket.Chat: {str(e)}")
                return "Unknown"

        else:
            # Récupérer le contenu du fichier status
            status = subprocess.getoutput(f'docker exec {container_name} cat /var/lib/dpkg/status')
            # Rechercher le bloc correspondant au package avec des préfixes et suffixes possibles
            package_block = re.search(f'Package: .*?[-.a-z]*{docker_type.lower()}[-.a-z]*.*?Version: ([\d.-]+(?:ce|ee)?\.?\d*)', status, re.DOTALL | re.IGNORECASE)
            if package_block:
                return package_block.group(1)
                
    except Exception as e:
        print(f"Erreur lors de la récupération de la version pour {container_name}: {str(e)}")
    
    return "Unknown"

def getAllDockers(configs):
    """
    Récupère les informations des conteneurs Docker à partir des configurations de sites.
    """
    dockers_info = []
    
    for config in configs:
        if config.get('port'):
            docker_info = getDockerFromPort(config['port'])
            if docker_info:
                version = getDockerVersion(docker_info['name'], docker_info['type'], config['port'])
                dockers_info.append({
                    "name": docker_info['name'],
                    "type": f"{docker_info['type']} (Docker)",
                    "version": version,
                    "url": config['url']
                })
    
    return dockers_info