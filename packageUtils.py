import os
import re
import subprocess

def getSitesPackages(configs):
    sites_info = []
    for config in configs:
        if config['port']:
            process = getProcessUsingPort(config['port'])
            if process:
                version = re.match(r'(\d+\.\d+(\.\d+)*)', os.popen(f"dpkg-query -f '${{Version}}' -W {process}").read()).group(1)
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
    Récupère le processus utilisant un port donné.
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
        if dpkg_result.returncode == 0:
            dpkg_output = dpkg_result.stdout.strip()
            package_name = dpkg_output.split(':')[0]
            return package_name
        return script_path

    except Exception as e:
        print(f"impossible de trouver le processus pour {port}", e)
        return None

def determineType(process):
    """
    Détermine le type du cms.
    """
    if process == "coolwsd":
        return "Collabora"
    elif process == "matrix-synapse-py3":
        return "Matrix"
    else:
        return process