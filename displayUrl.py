import SearchUrl, pymysql, re, os

listDbName = []

# Fonction qui cherche dans un fichier si il contient les informations liées à l'url des cms (Wordpress, Moodle, NextCloud)
def TakeUrlCms(fileConfig):
    """
    Extrait l'URL des CMS (Wordpress, Moodle, NextCloud) à partir d'un fichier de configuration.
    """
    listUrlCms = []
    fileConfig = fileConfig.split('\n')
    for line in fileConfig:
        try:
            if line.startswith('    0 => '):
                start = line.index('    0 => ') + len('    0 => ')
                end = line.index(',', start)
                url = line[start:end].strip("'")  # Supprimer les apostrophes
                if '.' in url:
                    listUrlCms.append(url)
            if line.startswith('    0 => \''):
                start = line.index('    0 => \'') + len('    0 => \'')
                if '.' in line[start:]:
                    end = line.index('.', start)
                    dbname = line[start:end]
                    listDbName.append(dbname)
        except:
            continue
    return listUrlCms

# Fonction pour extraire les informations de connexion à la base de données depuis wp-config.php
def getDbCredentialsFromWpConfig(path):
    """
    Extrait les informations de connexion à la base de données depuis le fichier wp-config.php.
    """
    with open(path, 'r') as file:
        config = file.read()
        dbname = re.search(r"define\(\s*['\"]DB_NAME['\"]\s*,\s*['\"](.+?)['\"]\s*\);", config)
        dbuser = re.search(r"define\(\s*['\"]DB_USER['\"]\s*,\s*['\"](.+?)['\"]\s*\);", config)
        dbpass = re.search(r"define\(\s*['\"]DB_PASSWORD['\"]\s*,\s*['\"](.+?)['\"]\s*\);", config)
        if dbname and dbuser and dbpass:
            return dbname.group(1), dbuser.group(1), dbpass.group(1)
        else:
            raise ValueError("Database credentials not found in wp-config.php")

# Fonction pour récupérer l'URL d'un site WordPress depuis la base de données
def getWordPressUrl(path):
    """
    Récupère l'URL d'un site WordPress depuis la base de données.
    """
    try:
        wp_config_path = findWpConfigPath(path)
        dbname, dbuser, dbpass = getDbCredentialsFromWpConfig(wp_config_path)
        connection = pymysql.connect(
            host='localhost',
            user=dbuser,
            password=dbpass,
            database=dbname
        )
        cursor = connection.cursor()
        cursor.execute("SELECT option_value FROM wp_options WHERE option_name = 'siteurl'")
        url = cursor.fetchone()[0]
        connection.close()
        # Supprimer les préfixes http:// ou https://
        url = re.sub(r'^https?://', '', url)
        return url
    except:
        return "Unknown"

# Fonction pour trouver le fichier wp-config.php en remontant dans les répertoires
def findWpConfigPath(path):
    """
    Trouve le fichier wp-config.php en remontant dans les répertoires.
    """
    while path != '/':
        wp_config_path = os.path.join(path, 'wp-config.php')
        if os.path.isfile(wp_config_path):
            return wp_config_path
        path = os.path.dirname(path)
    raise FileNotFoundError("wp-config.php not found")

# Fonction qui cherche dans un fichier si il contient les informations liées à l'url du cms (PhpMyAdmin)     
def TakeUrlCmsJson(fileConfig):
    """
    Extrait l'URL de PhpMyAdmin à partir d'un fichier de configuration JSON.
    """
    listUrlCmsJson = []
    fileConfig = fileConfig.split('\n')
    for line in fileConfig:
        if line.startswith('  ServerName '):
            start = line.index('  ServerName ') + len('  ServerName ')
            end = line.find(' ', start)  # Trouver la fin de l'URL
            if end == -1:  # Si aucun espace trouvé, prendre toute la ligne
                end = len(line)
            url = line[start:end].strip("'")  # Supprimer les apostrophes
            listUrlCmsJson.append(url)
    return listUrlCmsJson

# Fonction qui crée une condition pour trier les fichiers contenant les url
def trueOrNot(fileConfig):
    """
    Vérifie si un fichier de configuration contient des informations liées à l'URL des CMS.
    """
    fileConfig = fileConfig.split('\n')
    for line in fileConfig:
        if line.startswith('    0 => '):
            return True
        if line.startswith('    0 => \''):
            return True
    return False

# Fonction qui crée une condition pour trier les fichiers contenant les url
def trueOrNotJson(fileConfig):
    """
    Vérifie si un fichier de configuration JSON contient des informations liées à l'URL des CMS.
    """
    fileConfig = fileConfig.split('\n')
    for line in fileConfig:
        if line.startswith('  ServerName '):
            return True
    return False

def displayUrl():
    """
    Affiche les URLs des CMS (Wordpress, Moodle, NextCloud) en parcourant les fichiers de configuration.
    """
    currentpath = "/" # chemin vers répertoire courant
    pathOfFileConf = SearchUrl.SearchConf(currentpath)
    listUrl = []

    for path in pathOfFileConf:
        with open(path, 'r') as file:
            fileConfig = file.read()
            if 'wp' in path or 'wordpress' in path:
                url = getWordPressUrl(path)
                listUrl.append(url)  # Ajouter l'URL en tant qu'élément unique
            else:
                listUrl += TakeUrlCms(fileConfig)
    return listUrl

def displayUrlJson():
    """
    Affiche les URLs de PhpMyAdmin en parcourant les fichiers de configuration JSON.
    """
    currentpath = "/" # chemin vers répertoire courant
    pathOfFileConfJson = SearchUrl.SearchConfJson(currentpath)
    listUrlJson = []

    for path in pathOfFileConfJson:
        if "myadmin" in path:
            with open(path, 'r') as file:
                fileConfig = file.read()
                listUrlJson += TakeUrlCmsJson(fileConfig)
    return listUrlJson