# Smart GRH PFE (Application intelligente de GRH)

## 1. Contexte et problématique
## 2. Objectifs du projet
## 3. Périmètre (In/Out)
## 4. Acteurs et rôles
## 5. Modules fonctionnels
## 6. Automatisation (intelligence du système)
## 7. Architecture (vue globale)
## 8. Roadmap (planification)
## 9. Suivi Git (conventions de commits)
## 10. Documentation & UML
## 11. Comment exécuter le projet (à venir)
## 12. Licence (optionnel)
## 1. Contexte et problématique

Dans de nombreuses organisations, la gestion des ressources humaines repose encore sur des procédures manuelles ou des outils complexes et peu adaptés aux besoins réels des PME.

Les responsables RH font face à une charge administrative importante liée au traitement des demandes (congés, corrections de pointage, validations), au suivi du pointage et à l’évaluation de la performance.

Le manque d’automatisation entraîne des retards, des erreurs humaines et une absence de visibilité globale sur les indicateurs RH.

Ce projet vise donc à concevoir une application intelligente de gestion des ressources humaines permettant de centraliser, automatiser et simplifier les processus clés RH.
## 2. Objectifs du projet

Les objectifs principaux de cette application sont :

- Centraliser la gestion des employés au sein d’un système unique.
- Mettre en place un système structuré de gestion des demandes (congés, corrections, etc.).
- Automatiser les processus répétitifs afin de réduire la charge administrative des responsables RH.
- Améliorer la traçabilité et la transparence des décisions.
- Fournir des indicateurs et tableaux de bord pour faciliter la prise de décision.
- Intégrer des mécanismes d’alertes et de notifications automatiques.
## 3. Périmètre (In / Out)

### Fonctionnalités incluses (In Scope)

Le projet couvre les fonctionnalités suivantes :

- Gestion des employés (création, modification, consultation).
- Gestion des congés avec workflow de validation.
- Gestion du pointage (entrée, sortie, retards, absences).
- Système de demandes centralisé.
- Automatisation des règles métier (pré-validation, alertes, rappels).
- Évaluation de la performance basée sur des indicateurs objectifs.
- Tableau de bord RH avec statistiques principales.

### Fonctionnalités exclues (Out of Scope)

Les fonctionnalités suivantes ne sont pas incluses dans la version actuelle :

- Gestion complète de la paie (Payroll).
- Intégration avec des systèmes externes.
- Workflows complexes multi-niveaux avancés.
- Intelligence artificielle avancée prédictive.

Ces éléments pourront faire partie des perspectives d’amélioration futures.

## 4. Acteurs et rôles

Le système implique trois acteurs principaux :

### 👤 Employé
- Soumettre des demandes (congé, correction de pointage, etc.).
- Effectuer le pointage (entrée / sortie).
- Consulter l’état de ses demandes.
- Consulter ses indicateurs de performance.
- Recevoir des notifications.

### 🧑‍💼 Responsable RH
- Gérer les employés.
- Traiter et valider les demandes.
- Suivre le pointage (retards, absences).
- Évaluer la performance.
- Consulter les tableaux de bord.

### 🛠️ Administrateur
- Gérer les utilisateurs et les rôles.
- Paramétrer les types de demandes.
- Définir les règles d’automatisation.
- Superviser le système global.

## 5. Modules fonctionnels

L’application est structurée autour des modules fonctionnels suivants :

### 5.1 Module Gestion des employés
- Création et gestion des profils employés.
- Attribution des rôles (Employé, RH, Admin).
- Consultation des informations personnelles et professionnelles.

### 5.2 Module Gestion des demandes
- Soumission de demandes (congé, correction de pointage, etc.).
- Workflow de validation par le responsable RH.
- Suivi des statuts (en attente, approuvée, rejetée).
- Archivage et historique des actions.

### 5.3 Module Pointage
- Enregistrement des entrées et sorties.
- Calcul automatique des retards et absences.
- Suivi global du temps de travail.

### 5.4 Module Performance
- Calcul d’indicateurs basés sur la présence et la ponctualité.
- Attribution d’un score de performance.
- Évaluation qualitative par le responsable RH.

### 5.5 Module Automatisation
- Pré-validation automatique des demandes.
- Envoi de notifications et rappels.
- Détection des anomalies (retards fréquents, absences répétées).
- Mise à jour automatique des soldes.

## 6. Automatisation (intelligence du système)

L’aspect intelligent du système repose sur l’automatisation des règles métier et des processus RH.

Contrairement à un système classique purement manuel, cette application intègre des mécanismes automatiques permettant de :

- Vérifier automatiquement les conditions d’une demande (solde disponible, dates valides, absence de conflit).
- Calculer les retards et absences à partir des données de pointage.
- Mettre à jour automatiquement les soldes de congés après validation.
- Envoyer des notifications et rappels en cas de demandes en attente.
- Générer des alertes en cas d’anomalies (retards fréquents, absences répétées).

Cette automatisation vise à réduire les erreurs humaines, accélérer le traitement des demandes et améliorer l’efficacité globale du service RH.
## 7. Architecture (vue globale)

L’application suit une architecture en couches (3-tiers) :

- **Frontend** : interface utilisateur (Employé / RH / Admin).
- **Backend** : API et logique métier (règles RH, workflows, automatisation).
- **Base de données** : stockage des employés, demandes, pointage, performance et historique.

Les échanges entre le frontend et le backend se font via une API (REST).
### Technologies

- **Backend & Frontend** : Django (Python) avec templates (architecture MVC)
- **Base de données** : MySQL
- **Authentification & rôles** : Django Auth (Employé / RH / Admin)
- **Outils** : Git & GitHub


