import re
import os
import fnmatch
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

def getDbCredentialsFromLimeSurveyConfig(path):
    """
    Extrait les informations de connexion à la base de données depuis le fichier config.php de LimeSurvey.
    """
    with open(path, 'r') as file:
        config = file.read()
        connection_string = re.search(r"'connectionString'\s*=>\s*'(.+?)'", config)
        dbuser = re.search(r"'username'\s*=>\s*'(.+?)'", config)
        dbpass = re.search(r"'password'\s*=>\s*'(.+?)'", config)
        table_prefix = re.search(r"'tablePrefix'\s*=>\s*'(.+?)'", config)
        
        if connection_string and dbuser and dbpass and table_prefix:
            connection_string = connection_string.group(1)
            dbname = re.search(r'dbname=([^;]+)', connection_string).group(1)
            dbhost = re.search(r'host=([^;]+)', connection_string).group(1)
            dbport = re.search(r'port=([^;]+)', connection_string).group(1)
            return dbname, dbuser.group(1), dbpass.group(1), dbhost, dbport, table_prefix.group(1)
        else:
            raise ValueError("Database credentials not found in config.php")

def searchConfigFiles(currentpath, pattern):
    """
    Recherche des fichiers correspondant à un pattern donné dans un répertoire et ses sous-répertoires.
    """
    listPath = []
    for path, dirs, files in os.walk(currentpath):
        for fname in fnmatch.filter(files, pattern):
            chemin = os.path.join(path, fname)
            listPath.append(chemin)
    return listPath

def getWebsiteConfig():
    """
    Recherche des configurations de sites web dans les répertoires des serveurs web
    """
    apache_configs = searchConfigFiles("/etc/apache2/sites-enabled/", '*.conf')
    nginx_configs = searchConfigFiles("/etc/nginx/sites-enabled/", '*.conf')
    sites = []
    for config in apache_configs + nginx_configs:
        print(config)
        with open(config, 'r') as file:
            content = file.read()
            url, path, port = None, None, None
            if "apache2" in config:
                url_match = re.search(r"ServerName\s+([\S]+)", content)
                path_match = re.search(r"DocumentRoot\s+([\S]+)", content)
                port_match = re.search(r"ProxyPass(?:Match)?\s+[^\s]+\s+['\"]?(?:http://|https://)?(?:localhost|(?:\d{1,3}\.){3}\d{1,3}):(\d+)", content)
            elif "nginx" in config:
                url_match = re.search(r"server_name\s+([\S]+);", content)
                path_match = re.search(r"root\s+([\S]+);", content)
                port_match = re.search(r"server\s+(?:localhost|(?:\d{1,3}\.){3}\d{1,3}):(\d+)", content)

            if url_match:
                url = url_match.group(1)
            if path_match:
                path = path_match.group(1)
            if port_match:
                port = port_match.group(1)
            if url and (port or path):
                sites.append({'url': url, 'path': path, 'port': port})
    return sites