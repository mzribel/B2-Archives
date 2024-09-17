#routage

Un système autonome (AS, pour *Autonomous System*) est un ensemble de réseaux IP sous le contrôle d'une seule et même entité, typiquement un fournisseur d'accès à Internet ou une plus grande organisation qui possède des connexions redondantes avec le reste du réseau Internet, et dont la politique de [[Routage]] est cohérente.

> Il s'agit surtout d'une notion administrative et non technique.

La notion de système autonome s'**oppose** à celle de <u>réseau public</u> comme l'Internet, où les différentes entités indépendantes **peuvent prendre des décisions contradictoires**.

# Protocoles 

**Types de protocoles **:
- système autonome => routage <u>interne</u> en BGP interne ([[OSPF]] par exemple) ;
- entre systèmes autonomes => routage <u>externe</u> en BGP externe (eBGP).

# Fonctionnement 

Chaque AS est généralement sous le contrôle d'un FAI ou d'une organisation unique.

Chaque AS est différencié par un numéro de 16 ou 32 bits appelé *Autonomous System Number* (ASN), affecté par les [Registres Internet Régionaux](https://fr.wikipedia.org/wiki/Registre_Internet_r%C3%A9gional) (RIR) qui affectent également les adresses IP.

En général, l'ASN n'apparaît pas dans les protocoles de routage internes (IGP) puisque par définition, ceux-ci sont limités à un seul AS.
> Certains protocoles (EIGRP) sont configurés pour n'établir d'adjacence qu'avec les routeurs qui annoncent le même AS.


____
# Bibliographie 
- [*Qu'est-ce qu'un système autonome ?*](https://www.cloudflare.com/fr-fr/learning/network-layer/what-is-an-autonomous-system/), Cloudflare
- [*Autonomous System - Définition*](https://www.techno-science.net/definition/3888.html), Techno-Science.net. 