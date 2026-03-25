# 📖 Guide Utilisateur - Logiciel de Gestion de Bibliothèque

Bienvenue dans la documentation utilisateur de votre nouvelle application de gestion de livres. Ce guide va vous expliquer simplement comment vous connecter, naviguer, et rechercher des livres dans votre catalogue.

---

## 1. Démarrer l'application


1. Ouvrez le dossier Client sur votre ordinateur.
2. Lancez le fichier client.py
3. Attendez une seconde : la fenêtre de connexion apparaît à l'écran.

---

## 2. S'authentifier (Fenêtre de Connexion)

Afin de protéger les données du catalogue, tout le monde doit s'authentifier.

1. Tapez votre **Identifiant**.
2. Tapez votre **Mot de passe**.
3. Cliquez sur le bouton **Se connecter**.

*(En cas d'oubli ou pour tester l'application, voici deux comptes pré-configurés)* :
> **Profil Administrateur :** Identifiant : `admin` / Mot de passe : `admin`
> **Profil Employé :** Identifiant : `user` / Mot de passe : `user123`

Si les identifiants sont incorrects, un message d'erreur apparaîtra. S'ils sont corrects, la fenêtre principale s'ouvrira.

---

## 3. L'Écran Principal (Le Tableau de Bord)

C'est ici que se trouve le cœur de l'application. Dès l'ouverture de cette page, l'application contacte automatiquement la base de données et charge tous les livres dans le grand tableau central.

L'écran est décomposé en 3 parties claires :

### A. La Barre de Recherche (En haut)
Elle vous permet de trouver rapidement un livre au lieu de parcourir toute la liste à la main.
1. Cliquez dans la zone de texte à côté de *"Mot clé (titre)"*.
2. Tapez une partie du titre que vous cherchez (Exemple : "Harry"). *L'application n'est pas sensible aux majuscules/minuscules.*
3. Cliquez sur le bouton **Rechercher**. Le tableau se filtre immédiatement pour ne garder que les bons résultats !

### B. Le Bouton "Rafraîchir"
Si un ou une collègue vient de faire une rentrée de stock ou d'ajouter de nouveaux ouvrages via le système informatique, votre logiciel peut ne pas être à jour.
Un simple clic sur **Rafraîchir** relancera un appel réseau complet et vous affichera la toute dernière version de la base de données !

### C. Le Grand Tableau (Zone Centrale)
Ce tableau vous affiche les détails de chaque livre. Pour rendre la lecture confortable, il est trié par colonnes d'informations :
- **Id_Livre** : Le code unique du livre dans le système.
- **Titre** : Le nom de l'ouvrage.
- **Résumé** : Un texte introductif de l'histoire.
- **Prix** : Valeur de vente.
- **Date de parution** & Code **ISBN** (le code-barres international).
- **Stock** : Le nombre d'exemplaires encore présents en réserve de la boutique, à consulter d'urgence si un client vous demande une disponibilité !
- **Id_Editeur** : L'identifiant du fournisseur.

---

## 4. Fermer le Logiciel

Une fois votre journée terminée, ou votre recherche effectuée, il vous suffit de cliquer sur la petite croix `X` en haut à droite de la fenêtre principale. 

Le logiciel va de lui-même éteindre proprement le serveur interne de données et couper la liaison avec la base. Vous n'avez rien d'autre à faire !
