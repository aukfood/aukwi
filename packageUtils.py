import os
import re
import subprocess

def getSitesPackages(configs):
    """
    Récupère les informations des sites installés via des paquets système.
    
    Args:
        configs: Liste des configurations de sites contenant les ports et URLs
        
    Returns:
        Liste de dictionnaires contenant les informations des sites (url, type, version, plugins)
    """
    sites_info = []
    for config in configs:
        if config['port']:
            process = getProcessUsingPort(config['port'])
            if process:
                version = re.match(r'(\d+\.\d+(\.\d+)*)', os.popen(f"dpkg-query -f '${{Version}}' -W {process} 2>/dev/null").read())
                version = version.group(1) if version else searchVersion(process)
                type = determineType(process)
                sites_info.append({
                    'url': config['url'],
                    'type': type,
                    'version': version,
                    'plugins': {}
                })
    return sites_info

def getProcessUsingPort(port):
    """
    Récupère le nom du processus/paquet qui utilise un port donné.
    
    Args:
        port: Numéro du port à vérifier
        
    Returns:
        Nom du paquet ou None si non trouvé/erreur
    """
    try:
        # Utiliser lsof pour obtenir le PID du processus utilisant le port
        lsof_result = subprocess.run(['lsof', '-i', f':{port}'], capture_output=True, text=True)
        lsof_output = lsof_result.stdout.strip().split('\n')
        pid = lsof_output[1].split()[1]
        
        # si le processus est docker alors il ne faut pas le traiter
        if 'docker' in lsof_output[1].split()[0]:
            return None
        
        # trouver le chemin du processus
        ps_result = subprocess.run(['ps', '-p', pid, '-o', 'args'], capture_output=True, text=True)
        ps_output = ps_result.stdout.strip()
        script_path = ps_output.split()[1]

        # Utiliser dpkg pour obtenir le nom du paquet
        dpkg_result = subprocess.run(['dpkg', '-S', script_path], capture_output=True, text=True)
        dpkg_output = dpkg_result.stdout.strip()
        package_name = dpkg_output.split(':')[0]

        return package_name if package_name else script_path.split('/')[-1]

    except Exception as e:
        print(f"impossible de trouver le processus pour {port}", e)
        return None

def determineType(process):
    """
    Détermine le type de CMS basé sur le nom du processus.
    
    Args:
        process: Nom du processus
        
    Returns:
        Type de CMS identifié ou le nom du processus si non reconnu
    """
    if process == "coolwsd":
        return "collabora"
    elif process == "matrix-synapse-py3":
        return "matrix"
    else:
        return process
    
def searchVersion(process):
    """
    Recherche la version du CMS en utilisant systemctl et les fichiers de configuration.
    
    Args:
        process: Nom du processus
        
    Returns:
        Version trouvée ou "Unknown" si non trouvée
    """
    try:
        # Utiliser systemctl pour obtenir le répertoire de travail du paquet
        systemctl_result = subprocess.run(['systemctl', 'show', process], capture_output=True, text=True)
        systemctl_output = systemctl_result.stdout.strip().split('\n')
        for line in systemctl_output:
            if line.startswith('WorkingDirectory='):
                working_directory = line.split('=')[1].strip()
                break
        if process == "mattermost":
            version_output = subprocess.getoutput(f'{working_directory}/bin/mattermost version')
            if version_output:
                # Parcourir les lignes pour trouver celle qui commence par "Version:"
                for line in version_output.split('\n'):
                    if line.startswith('Version:'):
                        return line.split('Version:')[1].strip()
        else:
            version_file = os.path.join(working_directory, 'package.json')
            with open(version_file, 'r') as file:
                content = file.read()
                version = re.search(r'"version":\s*"(.+?)"', content)
                if version:
                    return version.group(1)
        return "Unknown"
    except Exception as e:
        print(f"impossible de trouver le répertoire de travail pour {process}", e)
        return "Unknown"