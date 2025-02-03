#!/usr/bin/env python3
import createFile
# from dotenv import load_dotenv
# import os

def main():
    """
    Fonction principale pour créer les fichiers d'inventaire.
    """
    # Création et envoi de l'inventaire
    glpi_url="https://dev-glpi.aukfood.net"
    createFile.createAndSend(glpi_url)

if __name__ == "__main__":
    main()