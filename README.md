# Inventaire GLPI

Ce projet permet de générer et d'envoyer automatiquement un inventaire des applications web (CMS et conteneurs Docker) vers GLPI.

## Fonctionnalités

- Détection automatique des sites web (Apache et Nginx)
- Support pour plusieurs CMS :
  - WordPress
  - Moodle
  - NextCloud
  - Joomla
  - Drupal
  - et plus encore...
- Ajout de l'inventaire dans une entité en fonction d'un fichier de configuration (voir mise en place)
- Détection des conteneurs Docker
- Inventaire des plugins et versions
- Barre de progression pendant l'exécution

## Prérequis

- Python 3.6+
- GLPI Agent installé sur le système
- Accès root pour certaines opérations

## Installation

1. Cloner le repository :

2. Installer les dépendances :
   ```bash
   pip install python-dotenv pymysql phpserialize
   ```
   ou
   ```bash
   apt install python3-dotenv python3-pymysql python3-phpserialize
   ```

3. Configurer les variables d'environnement :
   ```bash
   cp .env.example .env
   # Éditer le fichier .env avec vos paramètres
   ```

4. Installer l'agent GLPI : **attention note importante**
   Installer l'agent GLPI sans préciser d'url lors de l'installation pour éviter qu'il efface les inventaires existants.

## Utilisation

Exécuter le script principal (avec privilèges root):
```bash
sudo python3 main.py
```

## Structure du projet

- `main.py` : Point d'entrée du programme
- `createFile.py` : Gestion de la création et de l'envoi de l'inventaire
- `takeAppInHost.py` : Détection des applications installées sur l'hôte
- `takeAppInDocker.py` : Détection des applications dans Docker
- `fileUtils.py` : Utilitaires de gestion des fichiers
- `packageUtils.py` : Utilitaires de gestion des paquets

## Dépendances système requises

- glpi-agent
- docker (pour la détection des conteneurs)
- apache2/nginx (pour la détection des sites web)

## Mise en place de l'ajout dans une entité en fonction d'un fichier de configuration

- Spécifier le chemin du fichier
- Ajouter le nom de l'entité dans le fichier de configuration comme suit : 
```
client = Nom de L'entité
```
Attention, le script va retirer espaces et caractères spéciaux pour le nom de l'entité

- créer la règle d'association à une entité dans GLPI avec le nom de l'entité sans espaces et caractères spéciaux


