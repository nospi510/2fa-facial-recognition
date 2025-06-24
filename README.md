# 🔐 Système d'Authentification à Double Facteur avec Reconnaissance Faciale

Ce projet implémente un système **2FA (authentification à double facteur)** sécurisé pour une application web, combinant :

- Mot de passe traditionnel 🔑
- Reconnaissance faciale biométrique 📸

Après connexion, l'utilisateur valide son identité via **capture faciale en temps réel avec webcam**.

---

## 🚀 Fonctionnalités

- **📝 Inscription** : Création d'un compte avec image faciale.
- **🔐 Connexion sécurisée** : Mot de passe + vérification faciale.
- **📊 Tableau de bord** : Accessible après authentification complète.
- **🚪 Déconnexion** : Sécurisée.
- **🗄️ Base de données** : Utilise MariaDB distante.
- **🎨 Interface** : Web simple avec Flask & CSS.

---

## 🛠️ Technologies Utilisées

| Côté | Outils |
|------|--------|
| **Back-end** | Flask 2.3.3, SQLAlchemy, MySQL Connector |
| **Reconnaissance faciale** | OpenCV, face_recognition |
| **Front-end** | HTML, CSS, JavaScript |
| **Base de données** | MariaDB (sur `192.168.1.42`) |
| **Environnement** | Python 3.9, virtualenv |

---

## ✅ Prérequis

- Python 3.9 (testé sur macOS)
- Webcam fonctionnelle
- Serveur MariaDB accessible à l’adresse `192.168.1.42`
- Compte MariaDB : `2fa_user`
- Git
- Homebrew (macOS uniquement pour `face_recognition`)

---

## ⚙️ Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/nospi510/2fa-facial-recognition.git
cd 2fa-facial-recognition
````

### 2. Créer un environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Installer les dépendances Python

```bash
pip install -r requirements.txt
```

> 💡 Sur macOS, si l'installation de `face_recognition` échoue :

```bash
brew install cmake libpng
```

---

## 🧱 Configuration de la base de données

### 1. Connexion à MariaDB

```bash
mysql -h 192.168.1.42 -u nick -p
```

### 2. Création de la base

```sql
CREATE DATABASE 2fa_db;
```

> ⚠️ Assurez-vous que le fichier `/etc/mysql/mariadb.conf.d/50-server.cnf` contient `bind-address = 0.0.0.0` si connexion distante.

---

## 🔐 Configuration de l’environnement

### 1. Créer le fichier `.env`

```bash
touch .env
```

### 2. Ajouter les variables suivantes :

```env
DB_HOST=192.168.1.42
DB_USER=2fa_user
DB_PASSWORD=secure_password
DB_NAME=2fa_db
SECRET_KEY=<clé_secrète_générée>
```

> 🔑 Générez une clé secrète avec :

```bash
python3 -c "import secrets; print(secrets.token_hex(16))"
```

---

## 📂 Créer les dossiers nécessaires

```bash
mkdir -p app/static/images
mkdir -p app/static/known_faces
chmod -R 755 app/static/images app/static/known_faces
```

---

## ▶️ Lancer l'application

```bash
python run.py
```

L'application sera accessible à :
👉 [http://localhost:5001](http://localhost:5001)

---

## 👥 Utilisation

### 🔐 Inscription

* Allez sur `/register`
* Entrez un identifiant, mot de passe et téléchargez une image faciale
* L’image est sauvegardée dans `app/static/known_faces`

### 🧾 Connexion

* Allez sur `/login`
* Entrez vos identifiants → Redirection vers `/2fa`

### 🎥 Vérification 2FA

* Sur `/2fa`, autorisez la webcam
* Cliquez sur **Capturer l’image**, puis sur **Vérifier**
* Si l’image est reconnue, redirection vers `/dashboard`

### 📊 Tableau de bord

* Affiche un message de bienvenue personnalisé
* Cliquez sur **Se déconnecter** pour quitter

---

## ✅ Tests Fonctionnels

Fichier : `test-results.txt`

### Scénarios couverts :

* ✔️ Inscription avec visage
* ✔️ Connexion correcte / incorrecte
* ✔️ 2FA succès / échec
* ✔️ Accès conditionné au dashboard
* ✔️ Déconnexion

**Exemple de test réussi** :

> **Test 8** : Vérifier le tableau de bord
> **Étapes** : Connexion + 2FA → Accès `/dashboard`
> **Résultat attendu** : `Bienvenue, [username]!`

---

## 🧠 Problèmes Connus

* ❌ Mauvais éclairage = échec reconnaissance
* ⚠️ Webcam requise + permissions navigateur
* 💻 Face recognition peut être lent selon la machine

---

## 🔮 Améliorations Futures

* 🔁 Verrouillage après plusieurs tentatives échouées
* 🔒 Chiffrement des images faciales
* 🧑‍🎨 UI améliorée avec Bootstrap ou autre framework

---

## 📁 Structure du Projet

```
2fa-facial-recognition/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/style.css
│   │   ├── js/camera.js
│   │   ├── images/
│   │   └── known_faces/
│   └── templates/
│       ├── login.html
│       ├── register.html
│       ├── 2fa.html
│       └── dashboard.html
├── .env
├── requirements.txt
├── run.py
└── test-results.txt
```

---

## 📧 Contact

Développé par **Nick Alix**
🔗 [nick@visiotech.me](https://visiotech.me)
