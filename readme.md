# Application de Gestion de Livres - API REST & Client Lourd

Ce projet a été réalisé dans le cadre du **BTS SIO** (Services Informatiques aux Organisations) - Option SLAM. 
Il s'agit d'une architecture de type **client-serveur** permettant de consulter et gérer un catalogue de livres.

## Fonctionnalités
- **API REST (Back-end) :** Développée avec le framework **FastAPI**, elle assure le traitement des données (Consultation, Ajout, Suppression des livres). L'API est connectée à une base de données **SQL Server** grâce à l'ORM **SQLAlchemy** et sécurise l'accès à certaines de ses routes par Header HTTP. L'API est hébergée en local sur le port `8001`.
- **Client Lourd (Front-end) :** Développé en **Python (Tkinter)**, il offre une interface graphique fluide permettant aux utilisateurs de s'authentifier par login, de visualiser les livres disponibles, et d'effectuer des recherches interactives par mots-clés.
- **Confort d'utilisation :** Le client gère lui-même le lancement en tâche de fond du serveur de l'API afin de simplifier l'exécution du projet.

## Pré-requis
- **Python 3.8+** installé sur votre machine.
- Serveur **SQL Server** actif avec une base de données configurée.
- Pilotes ODBC installés (exemple : `ODBC Driver 17 for SQL Server`).

## Installation

1. **Cloner ou décompresser le projet** dans le répertoire de votre choix.
2. **Initialiser l'environnement virtuel (Optionnel mais recommandé) :**
   ```bash
   python -m venv venv
   # Activation sous Windows :
   venv\Scripts\activate
   ```
3. **Installer les dépendances requises :**
   ```bash
   pip install -r requirements.txt
   ```
4. **Base de données :**
   Assurez-vous que les identifiants de connexion dans `database.py` (ou le `.env`) correspondent à votre instance SQL Server. Au démarrage, SQLAlchemy créera automatiquement les tables nécessaires si elles n'existent pas. *Note : La vue SQL (V_Livres) doit potentiellement être créée dans SQL Server au préalable.*

## Exécution du projet

Le lancement de l'application est automatisé. Il suffit de démarrer le client lourd qui se chargera d'initialiser lui-même le serveur API.

1. **Ouvrir un terminal** dans le répertoire racine du projet.
2. **Exécuter le client :**
   ```bash
   python Client/client.py
   ```
> *L'API est alors propulsée via `uvicorn` sur l'adresse `http://127.0.0.1:8001` et se fermera seule à la fermeture de la fenêtre graphique Tkinter.*

## Accès & Authentification

**1. Connexion au client graphique Tkinter :**
Pour vous connecter à l'interface de visualisation, vous pouvez utiliser l'un des comptes locaux configurés :
- Identifiant : `admin` / Mot de passe : `admin`
- Identifiant : `user` / Mot de passe : `user123`

**2. Requêtes directes vers l'API (ex: via Postman) :**
Si vous souhaitez interroger l'API manuellement :
- **URL complète :** `http://127.0.0.1:8001`
- **Documentation interactive Swagger :** [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)
- **Sécurité :** L'accès aux points de terminaison protégés requiert l'autorisation explicite dans le header HTTP : `x-api-key: tp-secret-key`.

## Structure du Répertoire
- `main.py` : Point d'entrée de l'API FastAPI (déclarations des routes et du serveur métier).
- `models.py` / `schemas.py` : Entités structurelles SQLAlchemy et schémas de validation Pydantic.
- `crud.py` / `database.py` : Logique applicative SQL et paramétrage des instances de base de données.
- `Client/client.py` : Application fenêtrée du client lourd, exploitant `tkinter` et `requests`.
- `APISIO.txt` : Documentation textuelle recensant toutes les routes (endpoints) disponibles sur l'API.
