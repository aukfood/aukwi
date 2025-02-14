#!/usr/bin/env python3
import createFile
import os
from dotenv import load_dotenv


def main():
    """
    Fonction principale pour créer les fichiers d'inventaire.
    """
    # Chargement des variables d'environnement
    load_dotenv()
    
    # Récupération de l'URL GLPI depuis les variables d'environnement
    glpi_url = os.getenv('GLPI_URL')
    config_path = os.getenv('CONFIG_PATH')
    
    # Création et envoi de l'inventaire
    createFile.createAndSend(glpi_url, config_path)

if __name__ == "__main__":
    main()