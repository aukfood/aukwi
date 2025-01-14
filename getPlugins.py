import subprocess, pwd, displayUrl, pymysql, phpserialize, SearchUrl, os

listVersPlug = []
listNamePlug = []

# Fonction qui récupère nom + version des plugins dans un dictionnaire
def getPlug(listDbName, listUrl):
    plugDict = {}
    filtered_urls = [item for item in listUrl if any(substring in item for substring in listDbName)]
    for i in range(len(listDbName)):
        user = listDbName[i]
        plug_output = subprocess.getoutput(f'sudo -u {user} php8.2 /var/www/{filtered_urls[i]}/www/occ app:list').split('\n')
        if 'sudo:' in plug_output[0] or 'Console has to be executed' in plug_output[0] or 'Could not open' in plug_output[0] or 'Impossible d’écrire' in plug_output[0]:  # Si l'utilisateur ne fonctionne pas, essayer les utilisateurs possibles
            for user_info in pwd.getpwall():
                possible_user = user_info.pw_name
                plug_output = subprocess.getoutput(f'sudo -u {possible_user} php8.2 /var/www/{filtered_urls[i]}/www/occ app:list').split('\n')
                if 'sudo:' not in plug_output[0] and 'Console has to be executed' not in plug_output[0] and 'Could not open' not in plug_output[0] and 'Impossible d’écrire' not in plug_output[0]:
                    user = possible_user
                    break
        enabled_plugins = []
        disabled_plugins = []
        current_list = None
        for line in plug_output:
            if line.startswith('Enabled:'):
                current_list = enabled_plugins
            elif line.startswith('Disabled:'):
                current_list = disabled_plugins
            elif current_list is not None:
                plugin_info = line.split(':')
                if len(plugin_info) == 2:
                    plugin_name = plugin_info[0].strip().lstrip('-').lstrip()
                    plugin_version = plugin_info[1].strip()
                    current_list.append((plugin_name, plugin_version))
        plugDict[listDbName[i]] = {'enabled': enabled_plugins, 'disabled': disabled_plugins}
    return plugDict

# Fonction qui récupère les plugins WordPress
def getPlugWP(url):
    try:
        # Récupérer les informations de connexion à la base de données
        wpPath = SearchUrl.SearchConfWp(url)
        wpDir = os.path.dirname(wpPath)  # Retirer wp-config.php
        dbname, dbuser, dbpass = displayUrl.getDbCredentialsFromWpConfig(wpPath)
        connection = pymysql.connect(
            host='localhost',
            user=dbuser,
            password=dbpass,
            database=dbname
        )
        cursor = connection.cursor()

        # Étape 1 : Récupérer les plugins activés
        cursor.execute("SELECT option_value FROM wp_options WHERE option_name = 'active_plugins'")
        activePlugins = cursor.fetchall()
        activePlugins = [plugin.decode('utf-8') for plugin in phpserialize.loads(activePlugins[0][0].encode('utf-8')).values()]

        # Étape 2 : Récupérer les versions des plugins via _site_transient_update_plugins
        cursor.execute("SELECT option_value FROM wp_options WHERE option_name = '_site_transient_update_plugins'")
        updatePlugins = cursor.fetchone()
        connection.close()
    except:
        return {'enabled': [], 'disabled': []}

    plugin_versions = {}
    if updatePlugins:
        # Désérialiser les données de _site_transient_update_plugins avec object_hook
        updateData = phpserialize.loads(
            updatePlugins[0].encode('utf-8'),
            decode_strings=True,
            object_hook=lambda name, obj: {(key.decode() if isinstance(key, bytes) else key): value for key, value in obj.items()}
        )

        # Vérifier la liste des plugins dans "checked"
        checked_plugins = updateData.get('checked', {})
        for plugin_path, version in checked_plugins.items():
            plugin_name = plugin_path.split('/')[0]
            plugin_versions[plugin_name] = version
            
    # Récupérer les plugins inactifs
    inactivePlugins = []
    plugins_dir = os.path.join(wpDir, 'wp-content', 'plugins')
    for root, dirs, files in os.walk(plugins_dir):
        for file in files:
            if file.endswith('.php'):
                plugin_path = os.path.join(root, file)
                plugin_name = os.path.splitext(file)[0]
                if plugin_name not in [p.split('/')[0] for p in activePlugins]:
                    plugin_version = 'unknown'
                    with open(plugin_path, 'r') as f:
                        for line in f:
                            if 'Version:' in line:
                                plugin_version = line.split(':')[1].strip()
                                break
                    if plugin_version and plugin_version != 'unknown' and any(char.isdigit() for char in plugin_version):
                        inactivePlugins.append({'name': plugin_name, 'version': plugin_version})
    # Associer les versions aux plugins activés
    plugins = {
        'enabled': [
            {
                'name': plugin.split('/')[0],
                'version': plugin_versions.get(plugin.split('/')[0], 'unknown')
            }
            for plugin in activePlugins
        ],
        'disabled': inactivePlugins
    }
    return plugins

