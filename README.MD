# S3APP3: Système répartis

## Pour la validation
- Vous devriez avoir réussi à faire fonctionner les 6 étapes de la
problématique.
- Vous serez questionnés sur ce que vous avez réalisé, en vous demandant d’en
expliquer le fonctionnement
- Vous aurez à réserver une plage horaire pour rencontrer le tuteur au cours
de la période réservée.

### Avec le formateur
- Présenter votre solution à l’une des six (6) étapes de la problématique
(déterminée par le tuteur)
- Expliquer comment elle fonctionne
- Répondre aux questions touchant les technologies sous-jacentes

## Pour les productions à remettre
Le rapport, nommé CIP1_CIP2.pdf, doit contenir les éléments suivants :
Identification de l’ensemble des membres de l’équipe (Prénom, nom et CIP)
Une description de la solution utilisée pour chacune des six étapes de la
problématique :
1. Exemples d’utilisation des commandes nouveau, retrait et liste
2. Fichier de configuration fonctionnel
3. Fichier yml utilisé pour docker-compose
4. Explication des problèmes inhérents à cette étape
5. Fichier yml utilisé pour docker-compose
6. Fichier yml utilisé pour l’orchestration avec kubernetes

Discussion de la structure, des avantages et des inconvénients de la version
ultime du système :
Quelles technologies Linux sous-jacentes ont été utilisées pour permettre
la mise en oeuvre de conteneurs ? Expliquez brièvement (en un paragraphe) ce
que chacune permet de faire :
- Identification des ressources
- Contrôle de l’accès aux ressources
- Gestion des accès aux fichiers utilisés :
-- Quels sont les pilotes utilisables pour la persistance du système de
fichiers à union ?
-- Quel pilote de persistence a été utilisé et pourquoi ?

Discussion de la configuration réseau permettant aux différents conteneurs
d’interagir
Discussion de la duplication mise en place pour les ressources :
- Quelles ressources doivent être dupliquées, et pourquoi ?
- Dans quel cas la duplication peut se faire sur une machine réelle unique,
dans quel cas elle doit être distribuée sur plusieurs machines réelles ?
