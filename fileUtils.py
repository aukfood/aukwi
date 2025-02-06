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