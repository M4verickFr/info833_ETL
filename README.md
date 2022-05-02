
# 🔆 INFO833 - ETL

Le but de ce projet est de réaliser un système de gestion d’ETL à grande échelle en Python. 

## 🛠 ETL simple avec Redis et parallélisme

### Présentation
Une ETL est un logiciel qui **extrait** des données de sources multiples, puis les **transforme** afin de pouvoir les **charger** dans une Data Warehouse.

### ETL simple - Un ensemble de tâches

Pour notre ensemble de tâches, nous avons décidé de réaliser les tâches suivantes : 
- T1 : retourne la tâche suivante et le chemin vers le fichier contenants divers APIs
- T2 : retourne la tâche suivante et la liste des APIs récupérer dans le fichier
- T3 : utilise l’api stocké sous le nom “IP” pour obtenir l’IP public

Le programme contient un tableau **task_queue** contenant les tâches à effectuer.

### ETL & Redis - Connexion avec Redis

Nous avons utilisé une instance de REDIS dans un docker :
```sh
docker run -d -p 6379:6379 --name redis-host redis
```
Puis exécuter le fichier *redis-test.py* pour vérifier la connexion avec le serveur redis
Et enfin vous pouvez utiliser notre programme en exécutant le fichier *main-redis.py*

Le programme est le même que **ETL simple** mais le tableau **task_queue** est maintenant stocké dans redis.

La donnée est stockées sous la forme *task_name:hash_name* où la première partie réfère au nom de la tâche a effectuer et la seconde partie réfère au nom d’une variable de hash dans REDIS qui contient le dictionnaire des paramètres nécessaire à l’exécution de la tache task_name. 

### ETL parallélisme - Implémentation du parallélisme

**👀 Pourquoi Python ne permet pas de faire du parallélisme au niveau thread ?**
> D’après ce que nous avons compris, le parallélisme au niveau thread est bloqué par le verrou d'interpréteur global (GIL).
Il s'agit d'un mutex qui  protège l'accès aux objets. Cela empêche de faire du parallélisme au niveau thread pour assurer la sécurité des threads. Car en python, les threads partagent la même mémoire. Avec plusieurs threads exécutés simultanément, nous ne connaissons pas l'ordre dans lequel les threads accèdent aux données partagées. 
Le GIL a été inventé parce que la gestion de la mémoire en Python n'est pas thread-safe. Avec un seul thread en cours d'exécution à la fois, Python s’assure qu'il n'y aura jamais de conditions de concurrence.

Le programme main test chaque seconde s'il y a une tache dans la task_queue, si une tache est disponible, il démarre un processus qui effectue la tache.
Si aucune tache n'est détéctée pendant 10s de suite, le programme se termine.

## 🛠 ETL avancé et implémentation d'un mapreducer

L'objectif est de refaire le projet [Map-Reduce Java](https://github.com/caullird/proj731_map-reducer) que nous avons effectué il y a quelques mois.

En fonction du nombre de mots dans le fichier, nous démmarrons un certain nombre de mapper, chaque mapper publie leurs résultats sur redis. Et le programme main est en écoute, quand deux resultats sont disponibles, un processus reducer est démarré, qui publie à son tour son résultat. 

Quand tous les reducers ont été executés, le dernier résultat reçu correspond au résultat final que nous écrivons dans le fichier result.json.

## 🏗️ **Developed with**

* [Python](https://www.python.org/)
* [Redis](https://redis.io/)
* [Docker](https://www.docker.com/)

## 💪 **Authors of this project**

* **PERROLLAZ Maverick** _alias_ [@M4verickFr](https://github.com/M4verickFr)
* **CAULLIREAU Dorian** _alias_ [@caullird](https://github.com/caullird)
