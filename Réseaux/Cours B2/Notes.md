VLAN = séparation
éléments réseau de niveau 3?

### Routage

- switch de niveau 3 = switch avec un routeur intégré

notions de base:

> objectifs:

    - acheminer des paquets d'un réseau X à Y
    - en cas de multipath, inscrire la meilleure route dans la table de routage (meilleure route peut être la plus rapide, la plus courte, la plus efficiente dépendant du protocole)
    - détecter les routes qui ne sont plus valides et les supprimer de la table de routage
    - ajouter le plus rapidement possible de nouvelles routes ou remplacer le plus rapidement les routes perdues par la meilleure route actuellement disponible (détecter et ajouter = la convergence, temps de mise à jour = temps de convergence)

> unicast, broadcast, anycast, broadcast

    - unicast = PC A envoie à PC B, envoi vers un seul membre déjà connu
    - multicast = PC A envoie à plusieurs PC ciblés dans le même domaine de provision
    - anycast = PC A envoie au premier PC qui répond (broadcast into unicast)
    - broadcast = PC A envoie à tous les PC

> routage intérieur VS extérieur

    - attention faux-amis!
    - en routage on parle de système autonome = réseau ou ensemble de réseaux interconnectés à internet
    - routage intérieur = routage qui a lieu au sein de ce système autonome
    - routage extérieur = routage qui va permettre de relier les systèmes autonomes entre eux (les FAI font les deux)
    - les protocoles, commandes, équipements sont différents

> routage statique VS dynamique

    - exemple du GPS (choix de la route ou route optimisée et récupérée automatiquement)
    - statique utilisé en entreprise encore assez souvent (parce qu'elles veulent garder la main sur les zones de passage de flux)
    - dynamique utilisé par exemple par les box de maison

> protocole à vecteur de distance VS à état de lien

    - vecteur de distance = route la plus courte
    - état de lien = distance, efficacité

> classful VS classless
> convergence
> métrique

    - utilisée sur les protocoles à vecteur de distance (combien de saut à effectuer pour atteindre la destination)

> distance administrative

    - rattachée au protocole à état de lien (formule de calcul qui prend en compte la vitesse, la latence, le débit, etc.). Le routeur calcule et attribue une note, déterminante pour choisir la route finale (plus petite note = plus petite distance administrative = privilégiée)

Protocoles de routages

> Internes

    - A vecteur de distance
        - RIP v2 (standard) / RIPng = Routing information protocol
        - IGRP = Interior Gateway Protocol, version CISCO de RIP
    - A état de lien
        - OSPF = Open Shortest Path First
        basé sur l'algorithme de Dijsktra qui consiste à calculer toutes les routes possibles et choisir la plus optimale
    - Hybride (CISCO)
        - EIGRP = Enhanced Interior Gateway Routing Protocols (métrique la plus courte et l'état le plus efficient)
        Sait également gérer des routes de secours

> Externes

    - A vecteur de chemin (va traverser toutes les routes possibles puis détermine quelle est la plus efficace)
        - BGP = Border Gateway Protocol (côté FAI de manière générale)
        (fonctionne en TCP, à chaque envoi il reçoit un acknowledge, couche application d'OSI au lieu de la couche réseau)

> Notes:

    - Possible d'utiliser des routes dynamiques à côté de routes statiques (priorisation)
    - Souvent on met des routes statiques pour des réseaux internes. Ca peut arriver si on a deux sorties sur internet d'un réseau
    - ACL en sécurité des routeurs?
    - FA O/1 ou FA 0/0 = interfaces physiques
    - Interface VLAN sur l'interface physique nom FA 0/0.100 si elle couvre la VLAN 100

    - Maintenant le routage est géré par des UTM (gestion centralisée de la menace / unified thread management) qui allient pare-feu et routeur
    - Les routeurs seuls sont de plus en plus délaissés


### VLAN

Objectif : des sous-interfaces pour ne pas avoir à créer de VLAN par dizaines sur un seul routeur

Sous-interfaces VLAN dans les interfaces :
- Nombre illimité 
- Configurables comme une interface physique réelle (adresse IP, sous-réseau, VLAN) 
- La communication entre VLAN passe par le routeur en simulation, par UTM en entreprise ou par des switches de niveau 3. 
- Avantages : capables de faire du routage basique et routage inter-VLAN, mais pas de choix d'OSPF etc. Egalement moins chers qu'un routeur. 
- Inconvénient : pas de granularité (= pas de règle pour filtrer les accès inter-VLAN)

Différence LAN / VLAN :
- vlan a un identifiant, area jusqu'à 4096

interface physique (lan) et sous-interface virtuelle (vlan)

