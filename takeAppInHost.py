import re
import os
import pymysql
import phpserialize
import packageUtils
import fileUtils

def getAllSites(configs):
    """
    Récupère toutes les informations sur les sites, y compris les URLs, types, versions et plugins.
    """
    sites_info = []

    for config in configs:
        if config['path']:
            cms_type = determineCmsType(config['path'])
            version = getCmsVersion(config['path'], cms_type)
            plugins = getPlugins(config['path'], cms_type)
            #if config['url']!="Unknown" and cms_type!="Unknown":
            sites_info.append({
                    'url': config['url'],
                    'type': cms_type,
                    'version': version,
                    'plugins': plugins
                })
    sites_info += packageUtils.getSitesPackages(configs)
    return sites_info

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
    elif os.path.isfile(os.path.join(path, 'composer.json')) and 'drupal' in open(os.path.join(path, 'composer.json')).read():
        return "Drupal"
    elif os.path.isfile(os.path.join(path, 'conf/conf.php')) and 'dolibarr' in open(os.path.join(path, 'conf/conf.php')).read():
        return "Dolibarr"
    elif os.path.isfile(os.path.join(path, 'application/config/config.php')) and 'lime' in open(os.path.join(path, 'application/config/config.php')).read():
        return "LimeSurvey"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'gitlab' in open(os.path.join(path, 'config.php')).read():
        return "GitLab"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'rocketchat' in open(os.path.join(path, 'config.php')).read():
        return "RocketChat"
    elif os.path.isfile(os.path.join(path, 'index.php')) and 'passbolt' in open(os.path.join(path, 'index.php')).read():
        return "Passbolt"
    elif os.path.isfile(os.path.join(path, 'config.php')) and 'mattermost' in open(os.path.join(path, 'config.php')).read():
        return "Mattermost"
    elif os.path.isfile(os.path.join(path, 'package.json')) and 'peertube' in open(os.path.join(path, 'package.json')).read():
        return "Peertube"
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
    elif cms_type in ["PhpMyAdmin", "Peertube"]:
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
        version_file = os.path.join(path, 'composer.lock')
        with open(version_file, 'r') as file:
            content = file.read()
            version = re.search(r'"name":\s*"drupal/core",\s*"version":\s*"(.+?)"', content)
            if version:
                return version.group(1)
    elif cms_type == "Dolibarr":
        version_file = os.path.join(path, 'filefunc.inc.php')
        with open(version_file, 'r') as file:
            content = file.read()
            version = re.search(r"define\('DOL_VERSION',\s*'(.+?)'\);", content)
            if version:
                return version.group(1)
    elif cms_type == "Passbolt":
        # Remove 'webroot' from the path and add 'bin/cake'
        base_path = path.replace('/webroot', '')
        command = f"{base_path}/bin/cake passbolt version"
        try:
            output = os.popen(command).read()
            version = re.search(r"Passbolt (?:CE|EE) (\d+\.\d+\.\d+)", output)
            if version:
                return version.group(1)
        except Exception:
            return "Unknown"
    # Ajoutez des conditions similaires pour les autres CMS
    return "Unknown"

def getPlugins(path, cms_type):
    """
    Récupère les plugins installés pour un CMS donné.
    """
    plugins = {'enabled': [], 'disabled': []}
    if cms_type == "Wordpress":
        wp_config_path = os.path.join(path, 'wp-config.php')
        dbname, dbuser, dbpass = fileUtils.getDbCredentialsFromWpConfig(wp_config_path)
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
        dbname, dbuser, dbpass, dbhost, dbport, table_prefix = fileUtils.getDbCredentialsFromLimeSurveyConfig(config_path)
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
    elif cms_type == "Drupal":
        modules_dir = os.path.join(path, 'modules')
        themes_dir = os.path.join(path, 'themes')
        plugins = {'module': [], 'theme': []}
        for plugins_dir in [modules_dir, themes_dir]:
            for root, dirs, files in os.walk(plugins_dir):
                for file in files:
                    if file.endswith('.info.yml'):
                        plugin_path = os.path.join(root, file)
                        with open(plugin_path, 'r') as f:
                            content = f.read()
                            plugin_name = re.search(r'name:\s*(.+)', content).group(1)
                            plugin_version = re.search(r'version:\s*\'(.+?)\'', content).group(1)
                            type = re.search(r'type:\s*(.+)', content).group(1)
                            plugins[type].append({'name': plugin_name, 'version': plugin_version})
                        # Stop descending into subdirectories once a .info.yml file is found
                        dirs[:] = []
    elif cms_type == "Dolibarr":
        custom_dir = os.path.join(path, 'custom')
        core_modules_dir = os.path.join(path, 'core/modules')
        plugins = {'custom': [], 'core': []}
        for plugins_dir in [custom_dir, core_modules_dir]:
            status = 'custom' if 'custom' in plugins_dir else 'core'
            for root, dirs, files in os.walk(plugins_dir):
                for file in files:
                    if file.endswith('.class.php'):
                        plugin_path = os.path.join(root, file)
                        with open(plugin_path, 'r') as f:
                            content = f.read()
                            class_name = re.search(r'class\s+mod(\w+)\s+extends', content)
                            plugin_version = re.search(r'\$this->version\s*=\s*\'(.+?)\'', content)
                            if class_name and plugin_version:
                                plugin_name = class_name.group(1)
                                plugin_info = {'name': plugin_name, 'version': plugin_version.group(1)}
                                plugins[status].append(plugin_info)
    elif cms_type == "Moodle":
        mod_dir = os.path.join(path, 'mod')
        for root, dirs, files in os.walk(mod_dir):
            for file in files:
                if file == 'version.php':
                    plugin_path = os.path.join(root, file)
                    plugin_name = os.path.basename(os.path.dirname(plugin_path))
                    with open(plugin_path, 'r') as f:
                        content = f.read()
                        plugin_version = re.search(r'\$plugin->version\s*=\s*(\d+);', content).group(1)
                        plugins['enabled'].append({'name': plugin_name, 'version': plugin_version})
    elif cms_type == "Joomla":
        plugins_dir = os.path.join(path, 'plugins')
        for root, dirs, files in os.walk(plugins_dir):
            for file in files:
                if file.endswith('.xml'):
                    plugin_path = os.path.join(root, file)
                    with open(plugin_path, 'r') as f:
                        content = f.read()
                        plugin_name_match = re.search(r'<name>(.*?)</name>', content)
                        plugin_version_match = re.search(r'<version>(.*?)</version>', content)
                        if plugin_name_match and plugin_version_match:
                            plugin_name = plugin_name_match.group(1).split('_')[1]
                            plugin_version = plugin_version_match.group(1)  
                            plugins['enabled'].append({'name': plugin_name, 'version': plugin_version})
        plugins['enabled'] = [dict(t) for t in {tuple(d.items()) for d in plugins['enabled']}]
    return plugins