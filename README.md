Système d'Authentification à Double Facteur avec Reconnaissance Faciale

Ce projet implémente un système d'authentification à double facteur (2FA) sécurisé pour une application web dans le cadre d'un examen IA Appliquée, combinant une authentification par mot de passe et une vérification biométrique par reconnaissance faciale. Après la saisie d'un nom d'utilisateur et d'un mot de passe, l'utilisateur doit confirmer son identité via une capture faciale en temps réel à l'aide d'une webcam.
Fonctionnalités

Inscription : Création d'un compte avec nom d'utilisateur, mot de passe et une image faciale de référence.
Connexion : Authentification par mot de passe suivie d'une vérification 2FA par reconnaissance faciale.
Tableau de bord : Espace sécurisé accessible après authentification réussie, affichant un message personnalisé.
Déconnexion : Suppression sécurisée de la session utilisateur.
Base de données : Gestion des utilisateurs avec MariaDB, hébergée sur un serveur distant.
Interface utilisateur : Interface web simple et esthétique avec Flask et CSS.

Technologies Utilisées

Back-end : Flask 2.3.3, SQLAlchemy, MySQL Connector
Reconnaissance faciale : OpenCV, face_recognition
Front-end : HTML, CSS, JavaScript
Base de données : MariaDB (hébergée sur 192.168.1.42)
Environnement : Python 3.9, virtualenv

Prérequis

Python 3.9 installé sur votre machine (testé sur macOS).
Accès à une webcam pour la reconnaissance faciale.
Serveur MariaDB configuré sur 192.168.1.42 avec une base de données 2fa_db.
Compte utilisateur MariaDB avec les privilèges nécessaires (2fa_user avec mot de passe).
Git installé pour cloner le dépôt.
Homebrew (sur macOS) pour installer les dépendances de face_recognition (optionnel).

Installation

Cloner le dépôt :
git clone https://github.com/nospi510/2fa-facial-recognition.git
cd 2fa-facial-recognition


Créer et activer un environnement virtuel :
python3 -m venv .venv
source .venv/bin/activate


Installer les dépendances Python :
pip install -r requirements.txt

Si face_recognition échoue à s'installer, installez d'abord les dépendances nécessaires sur macOS :
brew install cmake libpng


Configurer le serveur MariaDB :

Connectez-vous au serveur MariaDB sur 192.168.1.42 : mysql -h 192.168.1.42 -u nick -p


Créez la base de données  :

CREATE DATABASE 2fa_db;


Assurez-vous que MariaDB accepte les connexions distantes (modifiez bind-address dans /etc/mysql/mariadb.conf.d/50-server.cnf si nécessaire).


Configurer les variables d'environnement :

Créez un fichier .env à la racine du projet :touch .env


Ajoutez les informations suivantes dans .env :DB_HOST=192.168.1.42
DB_USER=2fa_user
DB_PASSWORD=secure_password
DB_NAME=2fa_db
SECRET_KEY=votre_clé_secrète


Générez une clé secrète avec :python3 -c "import secrets; print(secrets.token_hex(16))"




Créer les dossiers nécessaires :
mkdir -p app/static/{images,known_faces}
chmod -R 755 app/static/{images,known_faces}


Lancer l'application :
python run.py

Accédez à l'application via http://localhost:5001.


Structure du Projet
2fa-facial-recognition/
├── app/
│   ├── __init__.py          # Initialisation de l'application Flask
│   ├── config.py            # Configuration (base de données, clés)
│   ├── models.py            # Modèle SQLAlchemy pour les utilisateurs
│   ├── routes.py            # Routes Flask (inscription, connexion, 2FA, dashboard)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Styles CSS
│   │   ├── js/
│   │   │   └── camera.js    # Gestion de la webcam
│   │   ├── images/          # Images temporaires pour 2FA
│   │   └── known_faces/     # Images faciales de référence
│   └── templates/
│       ├── login.html       # Page de connexion
│       ├── register.html    # Page d'inscription
│       ├── 2fa.html         # Page de vérification 2FA
│       └── dashboard.html   # Page du tableau de bord
├── .env                     # Variables d'environnement
├── requirements.txt         # Dépendances Python
├── run.py                   # Script de démarrage
├── test-results.txt         # Résultats des tests fonctionnels

Utilisation

Inscription :

Accédez à /register.
Saisissez un nom d'utilisateur, un mot de passe, et téléchargez une image faciale claire.
L'image est sauvegardée dans app/static/known_faces.


Connexion :

Accédez à /login.
Entrez vos identifiants.
Si corrects, vous serez redirigé vers la page 2FA.


Vérification 2FA :

Sur /2fa, utilisez la webcam pour capturer une image.
Cliquez sur "Capturer l’image", puis sur "Vérifier".
Si la reconnaissance faciale réussit, vous serez redirigé vers le tableau de bord.


Tableau de bord :

Sur /dashboard, consultez votre espace sécurisé.
Cliquez sur "Se déconnecter" pour quitter.



Tests Fonctionnels
Les tests sont documentés dans test-results.txt. Pour exécuter les tests :

Lancez l'application (python run.py).
Testez les scénarios suivants :
Affichage des pages (inscription, connexion, 2FA, dashboard).
Inscription avec une image valide.
Connexion avec des identifiants corrects/incorrects.
Vérification 2FA avec un visage correspondant/non correspondant.
Accès au tableau de bord après authentification réussie.
Déconnexion.



Exemple de test :

Test 8 : Vérifier le tableau de bord
Étape : Se connecter, passer 2FA, accéder à /dashboard.
Résultat attendu : Page affichée avec "Bienvenue, [username] !".



Problèmes Connus

La reconnaissance faciale peut échouer dans des conditions d'éclairage très médiocres.
Nécessite une webcam fonctionnelle et des permissions d'accès dans le navigateur.
Les performances dépendent de la puissance de calcul pour face_recognition.

Améliorations Futures

Ajouter un verrouillage temporaire après plusieurs tentatives 2FA échouées.
Chiffrer les images faciales pour plus de sécurité.
Intégrer un framework front-end (par exemple, Bootstrap) pour une meilleure UI.


