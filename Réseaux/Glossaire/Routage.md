#routage

Le [routage](https://fr.wikipedia.org/wiki/Routage) est le processus de sélection du chemin dans un réseau. Un réseau informatique est composé de nombreuses machines, appelées _nœuds_, et de chemins ou de liaisons qui relient ces nœuds. La communication entre deux nœuds d'un réseau interconnecté peut s'effectuer par de nombreux chemins différents, déterminés par le routeur.

Une politique de routage cohérente doit être établie dans chaque [[Système Autonome]].

Le routage peut être réalisé par :
- Un routeur 
- Un [switch de niveau 3](https://community.fs.com/fr/article/layer-3-switch-vs-router-what-is-your-best-bet.html)
> Les machines qui s'échangent les messages sont appelés les *hôtes*.

Les **objectifs du routage** sont les suivants : 
- <u>acheminer les paquets</u> d'un réseau X à Y ;
- en cas de multipath, <u>inscrire la meilleure route dans la table de routage</u> selon un protocole aux critères choisis (route la plus rapide, la plus courte, la plus efficiente...) ;
- <u>détecter</u> dynamiquement les routes qui ne sont plus valides et les supprimer de la table ;
- <u>ajouter le plus rapidement possible des nouvelles routes</u> ou remplacer celles qui ont été perdues par la meilleure option alternative possible (*convergence*).

**Convergence** : rapidité avec laquelle le réseau s'adapte aux changements tels que l'ajout de nouveaux routeurs ou la défaillance d'un lien.
> Les protocoles dynamiques comme l'OSPF ont une meilleure convergence que les protocoles statiques.

# Cardinalités

En fonction du nombre de destinataires et de la manière de délivrer le message, on distingue : 
- l'[unicast](https://fr.wikipedia.org/wiki/Unicast) (vers une seule destination déterminée) ;
- l'[anycast](https://fr.wikipedia.org/wiki/Anycast) (vers n'importe quel membre d'un groupe, généralement le plus proche, par exemple en [[DNS]]) ;
- le [multicast](https://fr.wikipedia.org/wiki/Multicast) (ensemble des machines du même groupe) ;
- le [broadcast](https://fr.wikipedia.org/wiki/Broadcast_(informatique)) (vers tous les membres d'un réseau).

#### Spécificités du multicast

**Comparaison** :
- plus efficace que de l'*unicast* qui enverrait les paquets autant de fois qu'il n'y a de connexions (gaspillage de temps et de bande passante) ;
- plus spécifique que le *broadcast* puisque les paquets ne sont envoyés que là où ils sont requis ;

En *multicast*, chaque paquet n'est envoyé qu'une fois et sera routé vers toutes les machines du groupe de diffusion sans que le contenu soit dupliqué sur une quelconque ligne physique.

> Attention : Le *multicast* ne permet d'aucune façon le contrôle ou la participation au groupe par la source. L'identification ou l'authentification, si requises, doivent être gérés au niveau applicatif.

**Groupe multicast** : Un groupe multicast se compose d'un ensemble de machines. Il est entièrement <u>dynamique</u> (une station peut rejoindre ou quitter le groupe à tout moment), et ouvert (une <u>station</u> peut émettre un paquet dans un groupe sans en faire partie).

# Statique VS Dynamique

Dans la mesure où le routage est un <u>processus décentralisé</u>, chaque routeur maintient une liste des réseaux connus, chacun de ces réseaux étant associés à un ou plusieurs routeurs voisins à qui le message peut être passé ([table de routage](https://fr.wikipedia.org/wiki/Table_de_routage)).

On distingue trois <u>types de routes</u> dans une table de routage :
- **connexion directe** - le routeur utilise un protocole de niveau 2 (Ethernet, par exemple), pour acheminé les paquets vers un autre routeur directement connecté ;
- **routes statiques** - configurées en dur par l'administrateur réseau ; 
- **routes dynamiques** - similairement à un GPS, 

**Avantages** du routage statique :
- peut servir de mécanisme de backup ; 
- simple à configurer ;
- aucune ressource supplémentaire n'est nécessaire ; 
- plus sécurisé.
**Inconvénients** du routage statique : 
- chaque changement dans la topologie nécessite une intervention manuelle sur les routeurs de la topologie ;
- ne convient pas à la croissance des réseaux larges.

**Notes** :
- Il est possible d'utiliser des routes statiques à côté de routes dynamiques ; 
- les routes statiques sont souvent choisies pour des réseaux internes (sécurité et choix de la porte de sortie vers Internet s'il y en a plusieurs) ; 

# Critères de choix 

## Vecteur de distance VS états de lien

Les protocoles de routage interne (IGP) échangent des informations de routage à l'intérieur d'un système autonome par l'une des façons suivantes :

### Vecteur de distance

Les protocoles à **vecteur de distance** ne diffusent que leurs <u>meilleures routes</u> sur leurs interfaces. 
> Protocoles : RIP ou IGRP.

On parle de :
- connaissance "plate" de l'inter-réseau ;
- routage non-hiérarchique.

**Particularités** : 
- convergent lentement mais moins gourmands en ressources CPU / RAM ;
- route la plus courte en nombre de sauts.

### Etats de lien

Les protocoles à **états de lien** transmettent <u>la totalité des informations de routage</u> à tous les routeurs participants et établissent des tables de voisins directs.
> Protocoles : OSPF ou IS-IS.

On parle de : 
- routage hiérarchique

**Particularités** :
- plus efficaces mais plus gourmands en ressources CPU / RAM ;
- privilégie le coût (distance et efficacité).

### Hybride (EIGRP)

L'EIGPR, protocole propriétaire de CISCO, est à la fois un protocole à états de lien et à vecteur de distance. 

Il valorise d'autres éléments pour définir sa métrique, tels que la bande passante, le délai, la charge, la fiabilité...

## Métrique 

La métrique d'une route est la valeur de celle-ci en comparaison à d'autres routes, apprises par le même protocole de routage. Plus sa valeur est faible, meilleure est la route.

Chaque protocole dispose de sa méthode de valorisation : 
- RIP : nombre de sauts ;
- OSPF : coût numérique dépendant de la bande passante des liens franchis ;
- EIGRP : bande passante, délai, charge, fiabilité.

Si plusieurs chemins fournis par le même protocole de routage (ayant donc la même distance administrative) ont la même métrique, le routeur fera de la [répartition de charge](https://fr.wikipedia.org/wiki/R%C3%A9partition_de_charge) (*load balancing*) et divisera les paquets sur les routes concernées.

Si deux chemins ayant la même métrique ont une distance administrative différente, le chemin avec la <u>distance administrative la plus faible</u> sera préféré.

### Distance administrative 

La distance administrative est indique la préférence dans une table de routage pour des destinations apprises par un protocole de routage par rapport aux mêmes destinations apprises par un autre protocole de routage.

Plus la valeur est faible et plus le protocole est préféré.

Par défaut, une route EIGRP sera préférée à une route RIP; une route statique sera préférée à toute autre route dynamique.

| Méthode de routage | Distance administrative |
| ---- | ---- |
| Réseau connecté | 0 |
| Route statique | 1 |
| Ext-BGP | 20 |
| Int-EIGRP | 90 |
| OSPF | 110 |
| IS-IS | 115 |
| RIP | 120 |
| Int-BGP | 200 |
| Inconnu | 255 |

### Classful VS Classless

Les protocoles de routage peuvent être divisés en deux groupes basés sur la méthode d'adressage TCP/IP : 
- protocoles de routage par classe ;
- protocoles de routage sans classe.

Les classes correspondes aux classes IP auparavant utilisées : 

| **Classe** | **Plage** | **Masque** |
| ---- | ---- | ---- |
| A | 10.0.0.0 - 10.255.255.255 | 255.0.0.0 = /8 |
| B | 172.16.0.0 - 172.16.31.255 | 255.255.0.0 = /16 |
| C | 192.168.0.0 - 192.168.255.255 | 255.255.255.0 = /24 |

Un protocole de **routage par classe** :
- ne transmet pas le masque de sous-réseau dans ses mises à jour de routage ;
- exige que chaque interface réseau et chaque hôte utilisent le même masque de sous-réseau, gaspillant du précieux espace d'adressage ; 
- envoie régulièrement des modifications de routage à toutes les interfaces actives de chaque routeur, pouvant provoquer une congestion sur les liaisons WAN lentes.
> Exemples : RIPv1 et IGRP, tous deux obsolètes.

Un protocole de **routage sans classe** :
- intègre les informations de sous-réseau lors de l'échange de tables de routage ou de mises à jour ;
- permet l'utilisation de réseaux avec **différentes longueurs de masque** (VLSM) et la prise en charge du **routage interdomaine sans classe** (CIDR) ; 
- les routeurs n'échangent la totalité de table de routage qu'à l'initialisation. Une fois que le réseau a atteint la convergence complète, les mises à jour ne sont envoyées que lorsque la topologie change.

**Résumé** : 

| **As applied to** | **Classful** | **Classless** |
| ---- | ---- | ---- |
| Addresses | Addresses have 3 parts : network, subnet, host | Addresses have two parts : subnet or prefix, and host |
| Routing protocols | Routing protocol doesn't advertise masks no support VLSM | Routing protocol does advertise masks and support VLSM |
| Routing (forwarding) | IP-forwarding process is restricted in how it uses the default route | IP-forwarding process has no restrictions on using the default route |
| Examples | RIPv1, IGRP | RIPv2, EIGRP, OSPF |
# Bibliographie 

- [*Protocoles de routage : Définition, fonctionnements et mise en place*](https://www.devuniversity.com/blog/protocoles-de-routage-definition-fonctionnements-et-mis-en-place#:~:text=De%20m%C3%AAme%2C%20la%20convergence%20du,rapide%20que%20les%20protocoles%20statiques.), DevUniversity (2023).
- [*Multicast - Définition*](https://www.techno-science.net/definition/3782.html), Techno-Science.net.
- [*Synthèse sur les protocoles de routage dynamique*](https://cisco.goffinet.org/ccna/routage/synthese-routage-dynamique/), cisco.goffinet.org.
- [*Quels sont les protocoles de routage avec classe et sans classe*](https://forum.huawei.com/enterprise/fr/que-sont-les-protocoles-de-routage-avec-classe-et-sans-classe/thread/667495126521495552-667481000260808704), Huawei (2022).