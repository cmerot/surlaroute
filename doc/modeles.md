# Modèles backend

## Annuaire

### Fiche Personne

Une fiche Personne représente une personne de la vie réelle avec bio, contact, fonction, etc.
à l'opposé d'une personne morale qui sera enregistrée en tant qu'organisation.

### Fiche Organisation

Une fiche Organisation représente un organisation réelle ou virtuelle. C'est un conteneur pour y attacher :

- une liste des activités de l'organisation (fiche Activité) et ainsi des informations supplémentaires liées à ces activités ;
- une liste de ses membres (fiches Personne et Organisation) ;
- des informations de contact.

Le **type** d'une organisation :

- externe : l'organisation n'est pas liée à l'éditeur ;
- interne : l'organisation est liée à l'éditeur, ses membres ont des privilèges supplémentaires. Exemple : Armodo et Slowfest.

### Fiche Activité

Une fiche Activité permet de décrire l'activité d'une organisation. Cela comprend :

- un nom et une description ;
- une liste des rôles possibles décrivant la ou les relations entre un membre et une organisation ;
- une liste des informations supplémentaires à lier à une Organisation.

	exemple: une organisation qui a comme activité "Restauration" ajoutera des champs sur la fiche de l'organisation pour savoir si c'est végétarien ou non.

```mermaid
classDiagram
    note for OrgActorAssoc "Membres de l'organisation"
    note for OrgActivity "Activités de l'organisation"
    note for Activity "Défini un schema de données pour l'org"
    Actor <|-- Org
    Actor <|-- Person
    Org --o Activity
    OrgActorAssoc --* Org
    OrgActorAssoc --* Actor
    OrgActivity --* Org
    OrgActivity --* Activity
    Actor --* Contact
    Contact --* AddressGeo

    class Actor {
    }
    class Org {
        +str name
        +OrgActorAssoc members
        +OrgActivity activities
        +bool is_member
        +JSONB data
    }
    class Activity {
        +ltree path
        +str title
        +JSONB schema
    }
    class Person {
        +str name
        +str role
        +bool is_individual
    }

    class OrgActorAssoc {
        +Org org
        +Actor member
        +JSONB data
    }
    class OrgActivity {
        +uuid org_id
        +uuid activity_id
    }
    class Contact {
        +str email_address
        +str phone_number
        +str website
        +AddressGeo address
    }
    class AddressGeo {
        +str street
        +str postal_code
        +str city
        +str country
        +administrative_area_1
        +administrative_area_2
        +GeoPoint geo_location
    }


```
## Tournée

Pour partager mon plan de tounée, j'ai besoin de :

- des lieux où je vais passer
- des événements ou je vais passer

Je vais saisir des étapes pour ma tournée

- un lieu (une organisation ?)
- une date
- une description

Si c'est je passe dans une salle de concert puis à un festival en 2 étapes :

- je créé ou sélectionne les 2 organisations

### Fiche Tournée

- propriétaire : utilisateur, donc une personne, et une organisation
- permissions : organisation / membres / autres
- acteurs avec role
- liste d'event

### Fiche Événement

- propriétaire : utilisateur, donc une personne, et une organisation
- permissions : organisation / membres / autres
- acteurs avec role
- lieu
- date debut
- date fin

```mermaid
classDiagram
    TourActorAssoc --* Tour
    TourActorAssoc --* Actor
    EventActorAssoc --* Event
    EventActorAssoc --* Actor
    Tour "1" --o "o..n" Event
    note for TourActorAssoc "Contacts de la tournée par fonction"
    note for EventActorAssoc "Contacts de l'événement par fonction"
    class Tour {
        str title
        str description
        +list[Event] events
        +TourActorAssoc actor_assocs
    }
    class Event {
        +str title
        +str description
        +Tour tour
        +DateTime start_datetime
        +DateTime end_datetime
        +AddressGeo address
        +EventActorAssoc actors
    }
    class TourActorAssoc {
        +Tour tour
        +Actor actor
        +JSONB data
    }
    class EventActorAssoc {
        +Event event
        +Actor actor
        +JSONB data
    }

```

## Permissions


### Présentation

Le système de permissions concerne les acteurs, tournées et événements. Cela permet de définir
qui peut lire ou modifier ces entités.

Ces entités ont chacune :

- un propriétaire : un utilisateur ;
- et un groupe propriétaire : une organisation.

Les permissions sont définies pour :

- les utilisateurs membres d'Armodo (User.is_member) en lecture/écriture
- les membres du groupe propriétaire en lecture/écriture
- les autres (utilisateur non membre et utilisateur non connecté)

#### Utilisateur

Un utilisateur est une personne qui a un compte sur le système, avec email et mot de passe.

Les **rôles** que peut exercer un utilisateur :

- superadmin : il peut faire tout ce qu'il est possible de faire ;
- membre : il est membre d'armodo

Les **statuts** d'un utilisateur :

- actif : il peut se connecter ;
- inactif : il ne peut pas se connecter (suite à la création d'un compte en attente de modération par exemple).

Un utilisateur peut être relié à une personne, elle même reliée à une organisation, permettant ainsi
de déduire les permissions liées au groupe propriétaire d'une entité.

#### Mise à jour des permissions

Seul le propriétaire d'une entité peut modifier son propriétaire et son groupe propriétaire.

### Diagramme

```mermaid
classDiagram
    note for User "Propriétaire de la ressource"
    note for Org "Groupe propriétaire de la ressource"
    note for Tour "Ressource"
    note for Event "Ressource"
    note for Actor "Ressource"
    note for Person "Personne correspondante à un utilisateur"
    Permissions <|-- Tour
    Permissions <|-- Event
    Permissions <|-- Actor
    Permissions --* User
    Permissions --* Org
    User --o Person
    class Permissions {
        +User owner
        +Org group_owner
        +bool group_read
        +bool group_write
        +bool member_read
        +bool member_write
        +bool other_read
    }
    class User {
        +str email
        +str password
        +bool is_superuser
        +bool is_member
        +bool is_active
        +Person person
    }
    class Person {
        +User user
    }
```
