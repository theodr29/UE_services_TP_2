# UE-AD-A1-MIXTE

## Ce qui a été fait :

TP Vert :
- Implémentation du service Movie en GraphQL
- Adaptation du Service User pour faire appel au service Movie via GraphQL
- Implémentation du service Times en gRPC
- Implémentation du service Booking en gRPC
- Adaptation du Service Booking pour faire appel au Service Times via gRPC
- Adapation du Service User pour faire appel au Service Booking via gRPC

TP Rouge :
- Non implémenté

## Utilisation :

### Prérequis :

Avoir une version de Docker fonctionnelle avec docker-compose

### Comment lancer :

Télécharger l'archive de code sur votre machine, ouvrez un terminal dans le dossier source du code :

```bash
$ docker-compose up --build
```

Vous pouvez ensuite utiliser un navigateur internet ou Postman pour utiliser l'application