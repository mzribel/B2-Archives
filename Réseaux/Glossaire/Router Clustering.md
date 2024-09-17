
# Définition 

La redondance de routeurs (*router clustering*) est le fait de mettre plusieurs routeurs dans un même réseau pour que, si l'un tombe en panne, l'autre le remplace. Cela permet de ne pas avoir d'interruption dans l'acheminement du réseau et d'assurer la disponibilité de la passerelle par défaut dans un sous-réseau en dépit de la panne.

**Avantages :**
- haute disponibilité 
- *load balancing* (répartition de charge)
- redondance et *failover* 
- fiabilité accrue, scalabilité et performances également pour de grands réseaux

Deux protocoles existent : 
- [HSRP](https://fr.wikipedia.org/wiki/Hot_Standby_Router_Protocol) (*Hot Standby Router Protocol*) - protocole propriétaire Cisco sur les routeurs et commutateurs de niveau 3.
- [VRRP](https://fr.wikipedia.org/wiki/Virtual_Router_Redundancy_Protocol#:~:text=Virtual%20Router%20Redundancy%20Protocol%20(protocole,h%C3%B4tes%20d'un%20m%C3%AAme%20r%C3%A9seau.) (*Virtual Router Redundancy Protocol*) - équivalent configurable 

# Fonctionnement 

Les deux protocoles au-dessus fonctionnent en créant un ou plusieurs réseaux virtuels, communs à plusieurs routeurs réels. 
-> La passerelle par défaut devient indifférente : c'est celle qui est visée, et non une IP réelle d'un des routeurs.

- Dans un cluster de routeurs, on va créer un ou plusieurs réseaux virtuels, communs à plusieurs routeurs réels ; 
- les routeurs physiques du cluster sont appelés les *cluster members*. Ils partagent la même configuration et les mêmes informations de routage ; 
- pour chaque *cluster member*, une priorité est définie : le routeur ayant la priorité la plus élevée deviendra le routeur *actif*. Les autres routeurs restent en *stand-by* et écoutent les messages émis par le routeur actif ;
- Si deux routeurs ont la même priorité, l'adresse MAC définira le nouvel *actif* ;
- périodiquement, les routeurs du groupe échangent des messages pour assurer qu'ils sont toujours joignables. Si le routeur *actif* ne répond pas, le routeur en *stand-by* avec la priorité la plus élevée devient le routeur *actif*.

<span style="background:rgba(240, 167, 216, 0.55)">Note :</span> Le routeur actif ne doit pas révéler son adresse IP réelle aux hôtes qui l'utilisent avec son adresse IP virtuelle. En particulier, les messages [ICMP](https://fr.wikipedia.org/wiki/Internet_Control_Message_Protocol) redirect ne seront pas envoyés.

# Packet Tracer :

Soient deux routeurs (A et B) utilisant le protocole HSRP pour fournir une tolérance aux pannes. Le routeur A utilisera l'adresse IP 192.168.0.2 avec un masque de sous-réseau de 255.255.255.0 ; le routeur B utilisera l'adresse IP 192.168.0.3 avec le même masque de sous-réseau.

L'adresse IP virtuelle est 192.168.0.1. Elle sera configurée comme passerelle par défaut sur les équipements du sous-réseau.

**Routeur A :**
```text
interface fastethernet 0/0
ip address 192.168.0.2 255.255.255.0
standby 10 ip 192.168.0.1
standby 10 priority 110 
standby 10 preempt```
```

**Routeur B :**
```
interface fastethernet 0/0
ip address 192.168.0.3 255.255.255.0
standby 10 ip 192.168.0.1
standby 10 priority 90
standby 10 preempt
```