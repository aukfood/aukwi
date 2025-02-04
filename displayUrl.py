import SearchUrl
import pymysql
import re
import os
import phpserialize  # Ajout de l'importation

listDbName = []

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

# Fonction pour déterminer le type de CMS à partir de l'URL ou des fichiers
def determineCmsType(path):
    """
    Détermine le type de CMS (Wordpress, Moodle, NextCloud, etc.) à partir de l'URL ou des fichiers.
    """
    if os.path.isfile(os.path.join(path, 'wp-config.php')):
        return "Wordpress"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'moodle' in path:
        return "Moodle"
    elif os.path.isfile(os.path.join(path, 'version.php')) and 'nextcloud' in path:
        return "NextCloud"
    elif os.path.isfile(os.path.join(path, 'config.inc.php')) and 'phpmyadmin' in path:
        return "PhpMyAdmin"
    elif os.path.isfile(os.path.join(path, 'configuration.php')) and 'joomla' in path:
        return "Joomla"
    elif os.path.isfile(os.path.join(path, 'settings.php')) and 'drupal' in path:
        return "Drupal"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'dolibarr' in path:
        return "Dolibarr"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'peertube' in path:
        return "PeerTube"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'limesurvey' in path:
        return "LimeSurvey"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'gitlab' in path:
        return "GitLab"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'rocketchat' in path:
        return "RocketChat"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'passbolt' in path:
        return "Passbolt"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'matrix' in path:
        return "Matrix"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'mattermost' in path:
        return "Mattermost"
    return "Unknown"

# Fonction pour récupérer la version du CMS installé
def getCmsVersion(path, cms_type):
    """
    Récupère la version du CMS installé à partir des fichiers de version.
    """
    if cms_type == "Wordpress":
        wp_config_path = findWpConfigPath(path)
        with open(wp_config_path, 'r') as file:
            config = file.read()
            version = re.search(r"define\(\s*['\"]WP_VERSION['\"]\s*,\s*['\"](.+?)['\"]\s*\);", config)
            if version:
                return version.group(1)
    elif cms_type == "Moodle":
        version_file = os.path.join(path, 'version.php')
        with open(version_file, 'r') as file:
            for line in file:
                if line.startswith('$release'):
                    return line.split('=')[1].strip().strip(';').strip("'")
    elif cms_type == "NextCloud":
        version_file = os.path.join(path, 'version.php')
        with open(version_file, 'r') as file:
            for line in file:
                if line.startswith('$OC_VersionString'):
                    return line.split('=')[1].strip().strip(';').strip("'")
    elif cms_type == "PhpMyAdmin":
        version_file = os.path.join(path, 'config.inc.php')
        with open(version_file, 'r') as file:
            for line in file:
                if line.startswith('$cfg[''Version'']'):
                    return line.split('=')[1].strip().strip(';').strip("'")
    # Ajoutez des conditions similaires pour les autres CMS
    return "Unknown"

# Fonction pour récupérer les plugins installés
def getPlugins(path, cms_type):
    """
    Récupère les plugins installés pour un CMS donné.
    """
    plugins = {'enabled': [], 'disabled': []}
    if cms_type == "Wordpress":
        wp_config_path = findWpConfigPath(path)
        dbname, dbuser, dbpass = getDbCredentialsFromWpConfig(wp_config_path)
        connection = pymysql.connect(
            host='localhost',
            user=dbuser,
            password=dbpass,
            database=dbname
        )
        cursor = connection.cursor()
        cursor.execute("SELECT option_value FROM wp_options WHERE option_name = 'active_plugins'")
        active_plugins = cursor.fetchone()[0]
        active_plugins = [plugin.decode('utf-8') for plugin in phpserialize.loads(active_plugins.encode('utf-8')).values()]
        cursor.execute("SELECT option_value FROM wp_options WHERE option_name = '_site_transient_update_plugins'")
        update_plugins = cursor.fetchone()[0]
        update_plugins = phpserialize.loads(
            update_plugins.encode('utf-8'),
            decode_strings=True,
            object_hook=lambda name, obj: {(key.decode() if isinstance(key, bytes) else key): value for key, value in obj.items()}
        )
        for plugin in active_plugins:
            plugin_name = plugin.split('/')[0]
            plugin_version = update_plugins['checked'].get(plugin, 'unknown')
            plugins['enabled'].append({'name': plugin_name, 'version': plugin_version})
        plugins_dir = os.path.join(path, 'wp-content', 'plugins')
        for root, dirs, files in os.walk(plugins_dir):
            for file in files:
                if file.endswith('.php'):
                    plugin_path = os.path.join(root, file)
                    plugin_name = os.path.splitext(file)[0]
                    if plugin_name not in [p['name'] for p in plugins['enabled']]:
                        plugin_version = 'unknown'
                        with open(plugin_path, 'r') as f:
                            for line in f:
                                if 'Version:' in line:
                                    plugin_version = line.split(':')[1].strip()
                                    break
                        plugins['disabled'].append({'name': plugin_name, 'version': plugin_version})
        connection.close()
    # Ajoutez des conditions similaires pour les autres CMS
    return plugins

def getAllSites():
    """
    Récupère toutes les informations sur les sites, y compris les URLs, types, versions et plugins.
    """
    currentpath = "/etc/apache2/sites-enabled/" # chemin vers répertoire courant
    apache_configs = SearchUrl.searchApacheConfigs(currentpath)
    sites_info = []

    for config_path in apache_configs:
        with open(config_path, 'r') as file:
            for line in file:
                if "DocumentRoot" in line:
                    path = line.split()[1]
                    cms_type = determineCmsType(path)
                    version = getCmsVersion(path, cms_type)
                    plugins = getPlugins(path, cms_type)
                    url = getWordPressUrl(path) if cms_type == "Wordpress" else path
                    sites_info.append({
                        'url': url,
                        'type': cms_type,
                        'version': version,
                        'plugins': plugins
                    })
    return sites_info