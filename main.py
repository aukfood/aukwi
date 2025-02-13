#!/usr/bin/env python3
import createFile


def main():
    """
    Fonction principale pour créer les fichiers d'inventaire.
    """
    # Création et envoi de l'inventaire
    glpi_url="https://dev-glpi.aukfood.net"
    createFile.createAndSend(glpi_url)

if __name__ == "__main__":
    main()
    
    
# qu'est ce qui ne fonctionne pas ?
# Version : docker[nextcloud?,rocket,calcom,matermost,]



# rocketchat (normal + container) /x
# mattermost (normal + container à venir) xx
# nextcloud (normal + container) /x
# calcom (container) x

# peertube (normal) /
# joomla (normal) /
# moodle (normal + container à venir) //
# passbolt (normal + container) //
# gitlab (normal + container) //
# collabora (normal + container) //
# matrix (normal) /
# limesurvey (normal) /
# drupal (normal) /
# onlyoffice (container) /
# phpmyadmin (normal) /
# dolibarr (normal) /