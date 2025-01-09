import subprocess, re, pwd

listVersPlug = []
listNamePlug = []

# Fonction qui récupère nom + version des plugins dans un dictionnaire
def getPlug(listDbName, listUrl):
    plugDict = {}
    filtered_urls = [item for item in listUrl if any(substring in item for substring in listDbName)]
    for i in range(len(listDbName)):
        user = listDbName[i]
        plug_output = subprocess.getoutput(f'sudo -u {user} php8.2 /var/www/{filtered_urls[i]}/www/occ app:list').split('\n')
        print(plug_output)
        if 'sudo:' in plug_output[0] or 'Console has to be executed' in plug_output[0] or 'Could not open' in plug_output[0] or 'Impossible d’écrire' in plug_output[0]:  # Si l'utilisateur ne fonctionne pas, essayer les utilisateurs possibles
            print("erreur dbname sudo")
            for user_info in pwd.getpwall():
                possible_user = user_info.pw_name
                print("essaye", possible_user)
                plug_output = subprocess.getoutput(f'sudo -u {possible_user} php8.2 /var/www/{filtered_urls[i]}/www/occ app:list').split('\n')
                print(plug_output)
                if 'sudo:' not in plug_output[0] and 'Console has to be executed' not in plug_output[0] and 'Could not open' not in plug_output[0] and 'Impossible d’écrire' not in plug_output[0]:
                    user = possible_user
                    print('trouvé! :', user)
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
                    plugin_name = plugin_info[0].strip().lstrip('-')
                    plugin_version = plugin_info[1].strip()
                    current_list.append((plugin_name, plugin_version))
        plugDict[listDbName[i]] = {'enabled': enabled_plugins, 'disabled': disabled_plugins}
    return plugDict