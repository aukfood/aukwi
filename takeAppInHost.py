import re
import os
import pymysql
import phpserialize
import fnmatch

def getAllSites():
    """
    Récupère toutes les informations sur les sites, y compris les URLs, types, versions et plugins.
    """
    urls = getUrls()
    sites_info = []

    for url, path in urls.items():
        cms_type = determineCmsType(path)
        version = getCmsVersion(path, cms_type)
        plugins = getPlugins(path, cms_type)
        # if url!="Unknown" and cms_type!="Unknown":
        sites_info.append({
                'url': url,
                'type': cms_type,
                'version': version,
                'plugins': plugins
            })
    return sites_info

def getUrls():
    """
    Récupère les URLs des sites.
    """
    currentpath = "/etc/apache2/sites-enabled/" # chemin vers répertoire d'apache
    apache_configs =  searchConfigFiles(currentpath, '*.conf')
    url_path = {}
    for config in apache_configs:
        with open(config, 'r') as file:
            for line in file:
                if "ServerName" in line:
                    url = line.split()[1]
                elif "DocumentRoot" in line:
                    url_path[url] = line.split()[1]
    return url_path

def determineCmsType(path):
    """
    Détermine le type de CMS (Wordpress, Moodle, NextCloud, etc.) à partir des fichiers de configuration spécifiques.
    """
    if os.path.isfile(os.path.join(path, 'wp-config.php')):
        return "Wordpress"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'moodle' in open(os.path.join(path, 'config.php')).read():
        return "Moodle"
    elif os.path.isfile(os.path.join(path, 'version.php')) and 'OC_Version' in open(os.path.join(path, 'version.php')).read():
        return "NextCloud"
    elif os.path.isfile(os.path.join(path, 'package.json')) and 'phpmyadmin' in open(os.path.join(path, 'package.json')).read():
        return "PhpMyAdmin"
    elif os.path.isfile(os.path.join(path, 'index.php')) and 'JOOMLA' in open(os.path.join(path, 'index.php')).read():
        return "Joomla"
    elif os.path.isfile(os.path.join(path, 'settings.php')) and 'Drupal' in open(os.path.join(path, 'settings.php')).read():
        return "Drupal"
    elif os.path.isfile(os.path.join(path, 'htdocs')) and 'dolibarr' in open(os.path.join(path, 'htdocs')).read():
        return "Dolibarr"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'PeerTube' in open(os.path.join(path, 'config.php')).read():
        return "PeerTube"
    elif os.path.isfile(os.path.join(path, 'application/config/config.php')) and 'lime' in open(os.path.join(path, 'application/config/config.php')).read():
        return "LimeSurvey"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'gitlab' in open(os.path.join(path, 'config.php')).read():
        return "GitLab"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'rocketchat' in open(os.path.join(path, 'config.php')).read():
        return "RocketChat"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'passbolt' in open(os.path.join(path, 'config.php')).read():
        return "Passbolt"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'matrix' in open(os.path.join(path, 'config.php')).read():
        return "Matrix"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'mattermost' in open(os.path.join(path, 'config.php')).read():
        return "Mattermost"
    return "Unknown"

def getCmsVersion(path, cms_type):
    """
    Récupère la version du CMS installé à partir des fichiers de version.
    """
    if cms_type == "Wordpress":
        version_file = os.path.join(path, 'wp-includes/version.php')
        with open(version_file, 'r') as file:
            content = file.read()
            version = re.search(r"\$wp_version\s*=\s*'(.+?)';", content)
            if version:
                return version.group(1)
    elif cms_type == "Moodle":
        version_file = os.path.join(path, 'version.php')
        with open(version_file, 'r') as file:
            for line in file:
                if line.startswith('$release'):
                    version = re.search(r'(\d+\.\d+\.\d+)', line)
                    if version:
                        return version.group(1)
    elif cms_type == "NextCloud":
        version_file = os.path.join(path, 'version.php')
        with open(version_file, 'r') as file:
            for line in file:
                if line.startswith('$OC_VersionString'):
                    return line.split('=')[1].strip().strip(';').strip("'")
    elif cms_type == "PhpMyAdmin":
        version_file = os.path.join(path, 'package.json')
        with open(version_file, 'r') as file:
            content = file.read()
            version = re.search(r'"version":\s*"(.+?)"', content)
            if version:
                return version.group(1)
    elif cms_type == "Joomla":
        version_file = os.path.join(path, 'administrator/manifests/files/joomla.xml')
        with open(version_file, 'r') as file:
            content = file.read()
            version = re.search(r'<version>(.*?)</version>', content)
            if version:
                return version.group(1)
    elif cms_type == "LimeSurvey":
        version_file = os.path.join(path, 'application/config/version.php')
        with open(version_file, 'r') as file:
            content = file.read()
            version = re.search(r"\$config\['versionnumber'\]\s*=\s*'(.+?)';", content)
            if version:
                return version.group(1)
    elif cms_type == "Drupal":
        version_file = os.path.join(path, 'package.json')
        with open(version_file, 'r') as file:
            content = file.read()
            version = re.search(r'"version":\s*"(.+?)"', content)
            if version:
                return version.group(1)
    # Ajoutez des conditions similaires pour les autres CMS
    return "Unknown"

def getPlugins(path, cms_type):
    """
    Récupère les plugins installés pour un CMS donné.
    """
    plugins = {'enabled': [], 'disabled': []}
    if cms_type == "Wordpress":
        wp_config_path = os.path.join(path, 'wp-config.php')
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
                        if re.search(r'\d', plugin_version):
                            plugins['disabled'].append({'name': plugin_name, 'version': plugin_version})
        connection.close()
    elif cms_type == "NextCloud":
        apps_dir = os.path.join(path, 'apps')
        for root, dirs, files in os.walk(apps_dir):
            for dir in dirs:
                app_info_path = os.path.join(root, dir, 'appinfo', 'info.xml')
                if os.path.isfile(app_info_path):
                    with open(app_info_path, 'r') as f:
                        content = f.read()
                        app_name = re.search(r'<id>(.*?)</id>', content).group(1)
                        app_version = re.search(r'<version>(.*?)</version>', content).group(1)
                        plugins['enabled'].append({'name': app_name, 'version': app_version})
    elif cms_type == "PhpMyAdmin":
        composer_lock_file = os.path.join(path, 'composer.lock')
        with open(composer_lock_file, 'r') as file:
            content = file.read()
            packages = re.findall(r'"name":\s*"([^"]+)",\s*"version":\s*"([^"]+)"', content)
            for package in packages:
                plugins['enabled'].append({'name': package[0], 'version': package[1]})
    elif cms_type == "LimeSurvey":
        config_path = os.path.join(path, 'application/config/config.php')
        dbname, dbuser, dbpass, dbhost, dbport, table_prefix = getDbCredentialsFromLimeSurveyConfig(config_path)
        connection = pymysql.connect(
            host=dbhost,
            port=int(dbport),
            user=dbuser,
            password=dbpass,
            database=dbname
        )
        cursor = connection.cursor()
        cursor.execute(f"SELECT name, version, active FROM {table_prefix}plugins")
        plugins_data = cursor.fetchall()
        for plugin in plugins_data:
            plugin_info = {'name': plugin[0], 'version': plugin[1]}
            if plugin[2] == 1:
                plugins['enabled'].append(plugin_info)
            else:
                plugins['disabled'].append(plugin_info)
        connection.close()
    return plugins

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

print(getAllSites())