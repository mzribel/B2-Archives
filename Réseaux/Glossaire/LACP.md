
# Définition

Le [LACP](https://fr.wikipedia.org/wiki/IEEE_802.3ad) (*Link Aggregation Control Protocol*) est un protocole de couche 2 du modèle OSI qui permet de regrouper plusieurs ports physiques en un port logique.

Il s'agit du protocole utilisé dans une agrégation de liens ([[LAG]]) dynamique.

## Répartition 

LACP permet un maximum de 16 ports dont 8 actifs.

Au niveau de chaque extrémité LACP il est possible de définir une politique de choix du port de sortie qui déterminera par quel port sortira une trame en fonction des arguments sélectionnables suivants : 
- les adresses MAC (source et/ou destination) ;
- les adresses IP (source et/ou destination) ;
- le port applicatif (destination).

<span style="background:rgba(240, 167, 216, 0.55)">Note -</span> Concernant les ports :
- Chaque flux réseau entre deux ordinateurs passera toujours par un seul port pour éviter les problèmes de réordonnancement à l'arrivée ;
- Ainsi, le débit nominal n'est pas toujours égal à la somme des débits de chaque port.

## Configuration 

Les modes possibles pour un port sont : 
- active : active le LACP inconditionnellement (la machine connectée doit supporter le LACP) ;
- passive : active le LACP seulement si détecté (généralement le mode par défaut).

___
# Bibliographie : 

- [NetGear](https://kb.netgear.com/fr/000051185/Qu-est-ce-que-l-agr%C3%A9gation-de-liens-et-le-LACP-et-comment-puis-je-les-utiliser-dans-mon-r%C3%A9seau?language=fr)
- [Dell](https://www.dell.com/support/kbdoc/fr-fr/000121681/comment-cr%C3%A9er-et-g%C3%A9rer-l-agr%C3%A9gation-de-liens-lag-sur-un-commutateur-dell-networking-s%C3%A9rie-x)