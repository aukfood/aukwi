#!/usr/bin/env python3

import takeAppInDocker, SearchUrl, displayUrl, gestCsv, displayVers, SearchVersionFile, getPlugins

def main():
    # Création des fichiers d'inventaire
    gestCsv.createInventory()
    gestCsv.createInventoryJson()
    #listUrl = displayVers.displayVersionJson()
    #listDb = displayUrl.listDbName
    #print(listUrl)
  
if __name__ == "__main__":
    main()
