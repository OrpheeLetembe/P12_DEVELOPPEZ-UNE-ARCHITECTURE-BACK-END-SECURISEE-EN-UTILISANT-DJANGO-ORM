# P12_DEVELOPPEZ-UNE-ARCHITECTURE-BACK-END-SECURISEE-EN-UTILISANT-DJANGO-ORM

 # Description
  Epic Events est une entreprise de conseil et de gestion dans l'événementiel répondant aux besoins des start-up voulant organiser des fêtes. Suite au piratage du fournisseur de son CRM, elle décide d’élaborer un système CRM interne. 

Le système mis en place devra répondre aux exigences fonctionnelles suivants :
1-	Le système utilise Django et PostgreSQL.

2-	Le système prend en charge une page de connexion à laquelle les utilisateurs peuvent accéder.
-	Site d'administration Django configuré
-	La page de connexion du site d'administration Django est accessible
-	Les utilisateurs autorisés peuvent se connecter au site d'administration Django

3-	Il existe des modèles Django couvrant les domaines métier importants

4-	Les utilisateurs non administrateurs peuvent être associés à l'un des deux groupes déterminant les autorisations pour l'API
-	Tous les membres de l'équipe de gestion doivent avoir : 
   1. Créer, mettre à jour et supprimer des utilisateurs dans le système CRM.
   2. Afficher et modifier toutes les données dans le système CRM. 

5-	Il existe une API prenant en charge les opérations CRUD en fonction des modèles de base de données
-	Tous les membres de l'équipe de vente doivent pouvoir : 
   1. Ajouter de nouveaux clients dans le système CRM à mesure qu'ils obtiennent des prospects. 
   2  Actualiser les informations du client pour garantir leur exactitude. 
   3. Créer un contrat pour un nouvel événement potentiel. 
   4. Indiquer qu'un contrat ouvert est signé.  
   5. Créer un nouvel événement pour un contrat. 
 
-	Tous les membres de l'équipe de support doivent pouvoir : 
 1. Afficher et actualiser les informations relatives aux événements attribués.  
 2. Afficher les informations du client relatives aux événements attribués. 
 3. Actualiser les informations sur l'événement jusqu'à ce qu'il soit terminé. 

6-	Les endpoints  d'API doivent permettre aux utilisateurs de rechercher et de filtrer les informations


# Technologies utilisées :
-	Python 3.9.7
-	Django 4.0.4
-	Django rest framework 3.13.1
-	Django rest framework-simplejwt 5.2.0
-	PostgreSQL 14.3,

# Installation et exécution de l'application 

1	Cloner ce dépôt de code à l'aide de la commande ‘$ git clone clone https://github.com/OrpheeLetembe/P12_DEVELOPPEZ-UNE-ARCHITECTURE-BACK-END-SECURISEE-EN-UTILISANT-DJANGO-ORM.git

2	 Rendez-vous depuis un terminal à la racine du répertoire du projet 

3	Créer un environnement virtuel pour le projet avec la commande :

- `$ python -m venv env` sous windows 
- `$ python3 -m venv env` sous macos ou linux.

4	Activez l'environnement virtuel avec la commande

- `$ env\Scripts\activate` sous windows 
- `$ source env/bin/activate` sous macos ou linux.

5	Installez les dépendances du projet avec la commande `$ pip install -r requirements.txt`
6	 Démarrer le serveur avec $ python manage.py runserver

Les étapes 1 à 5 ne sont requises que pour l'installation initiale. Pour les lancements ultérieurs de l'application, il suffit d'exécuter l’étape 6 à partir du répertoire racine du projet.

Une fois que vous avez lancé le serveur, les utilisateurs autorisés peuvent se connecter à l’interface de gestion du CRM via l'url de base http://127.0.0.1:8000/admin.
L’API peut être interrogée à partir des points d'entrée commençant par l'url de base http://127.0.0.1:8000/api/


|Point de terminaison|Méthode HTTP|URI|
|-----------------|------------|--------------|
| Connexion de l'utilisateur	          |  POST  |/login/|
| Récupérer la liste de tous les clients |  GET|/clients/|
| Ajouter un client            |  POST|/clients/|
| Récupérer les détails d'un client via son id |  GET |/clients/{id}/|
| Mettre à jour les données d’un client             |  PUT |/clientts/{id}/|
| Créer un contrat pour un client |  POST|/ clients/{id}/contarcts/|
| Mette à jour les données d’un contrat |  PUT|/ clients/{id}/contracts/{id}|
| Récupérer le liste de tous les contrats|  GET|/contracts/|
| Récupérer les détail d’un contrat|  GET|/contracts/{id}/|
| Marquer qu’un contrat est signé|  Post|/clients/{id}/contracts/{id}/signed/
| Ajouter un évènement|  POST|/clients/{id}/contracts/{id}
| Récupérer la liste de tous les évènements|  GET|/events/
| Récupérer les détail d’un évènement|  GET|/events/{id}
| Mettre à jour un évènement|  PUT|/events/{id}
| Marquer un évènement comme terminer|  POST|/events/{id}
| Filtrer les clients, les contrats et les évènements|  POST|/filters









