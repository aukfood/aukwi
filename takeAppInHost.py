import SearchUrl

def getAllSites():
    """
    Récupère toutes les informations sur les sites, y compris les URLs, types, versions et plugins.
    """
    urls = getUrls()
    versions = getVersions(urls)
    plugins = getPlugins(urls)
    
    sites_info = []
    for url, version, plugins in zip(urls, versions, plugins):
        sites_info.append({
            'url': url,
            'type': getSiteType(url),
            'version': version,
            'plugins': plugins
        })
    return sites_info

def getUrls():
    """
    Récupère les URLs des sites.
    """
    currentpath = "/etc/apache2/sites-enabled/" # chemin vers répertoire courant
    apache_configs = SearchUrl.searchApacheConfigs(currentpath)
    url_path = {}
    for config in apache_configs:
        with open(config, 'r') as file:
            for line in file:
                if "ServerName" in line:
                    url = line.split()[1]
                elif "DocumentRoot" in line:
                    url_path[url] = line.split()[1]
    return url_path

def getVersions(url_path):
    """
    Récupère les versions des sites à partir des chemins des dossiers de documentations.
    """
    versions = {}
    for url, path in url_path.items():
        
    return versions