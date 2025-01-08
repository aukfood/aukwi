import subprocess

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

# Fonction pour récupérer le vhost des containers Docker
def getDockerVhosts(nameList):
    vhosts = []
    for name in nameList:
        vhosts.append("unknown")
    return vhosts

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