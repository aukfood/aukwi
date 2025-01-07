import subprocess

# Fonction pour récupérer tous les noms des containers Docker correspondant à un pattern
def getDockerNames(pattern):
    return subprocess.getoutput(f'docker ps -a --format \'{{{{.Names}}}}\' | grep {pattern}').split('\n')

# Fonction pour récupérer le serveur des containers Docker
def getDockerServers(nameList):
    return [subprocess.getoutput(f'docker exec -it {name} hostname -f').strip() for name in nameList]

# Fonction pour récupérer la version des containers Docker
def getDockerVersions(nameList, versionKey):
    versions = []
    for name in nameList:
        status = subprocess.getoutput(f'docker exec -it {name} cat /var/lib/dpkg/status').split()
        try:
            versionIndex = status.index(versionKey) + 1
            versions.append(status[versionIndex])
        except ValueError:
            versions.append("Unknown")
    return versions

# Fonction pour récupérer tous les noms des OnlyOffice dans les dockers
def getNameOnlyOffice():
    return getDockerNames('onlyoffice')

# Fonction pour récupérer le serveur des OnlyOffice récupérés avec getNameOnlyOffice
def getServOnlyOffice():
    return getDockerServers(getNameOnlyOffice())

# Fonction pour récupérer la version des OnlyOffice récupérés avec getNameOnlyOffice
def getVersOnlyOffice():
    return getDockerVersions(getNameOnlyOffice(), "Version:")

# Fonction pour récupérer tous les noms des Collabora dans les dockers
def getNameCollabora():
    return getDockerNames('collabora')

# Fonction pour récupérer la version des Collabora récupérés avec getNameCollabora
def getVersCollabora():
    return getDockerVersions(getNameCollabora(), "Office")

# Fonction pour récupérer le serveur des Collabora récupérés avec getNameCollabora    
def getServCollabora():
    return getDockerServers(getNameCollabora())

# Fonction pour récupérer tous les noms des Calcom dans les dockers
def getNameCalcom():
    return getDockerNames('calcom')

# Fonction pour récupérer le serveur des Calcom récupérés avec getNameCalcom
def getServCalcom():
    return getDockerServers(getNameCalcom())

# Fonction pour récupérer la version des Calcom récupérés avec getNameCalcom
def getVersCalcom():
    return getDockerVersions(getNameCalcom(), "Version:")