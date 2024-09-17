
# Définition

L'[agrégation de liens](https://fr.wikipedia.org/wiki/Agr%C3%A9gation_de_liens) (*Link Aggregation Group*) permet de combiner plusieurs liaisons Ethernet en une seule liaison logique entre deux périphériques en réseau.

**Autres noms** : 
- Liaison Ethernet
- Regroupement Ethernet
- Liaison solidaire
- Regroupement de liaisons
- Regroupement de liens
- Liaison du contrôleur d'interface réseau (NIC)
- Regroupement de cartes réseau
- Agrégation de ports
- Canalisation de port
- Agrégation de ports

**But** : Accroître le débit au-delà des limites d'un seul lien, et éventuellement de faire en sorte que les autres ports prennent le relai si un lien tombe en panne (redondance / *failover*).

____
# Fonctionnement 

### Couches OSI

Le LAG peut être mis en place sur les trois couches inférieures du modèle OSI, par exemple :
- **Couche 1** - Agrégation de liens CPL sur le réseau électrique ou sur un réseau sans-fil, regroupement des plages de fréquences en une seule, plus étendue 
- **Couche 2** - Agrégation de liens Ethernet ou agrégation de liens longue distance PPP avec *multilink PPP*
- **Couche 3** - Envoi de paquets IP en les transmettant tour à tour sur des routes différentes

## Connexions

Les combinaisons les plus courantes impliquent la connexion :
- d'un switch vers un autre switch 
- d'un switch vers un serveur 
- d'un switch vers un NAS
- d'un switch à un point d'accès multiport

<span style="background:rgba(240, 167, 216, 0.5)">Note :</span> Les switches non-manageables ne prennent pas en charge l'agrégation de liens.

Il est également possible d'inclure un LAG dans un réseau local virtuel (VLAN), de configurer plusieurs LAG sur le même switch ou d'ajouter plus de deux liaisons Ethernet au même LAG.

### Types de LAG

Il existe deux types de LAG : 
- statique, où les paramètres sont définis manuellement ;
- dynamique, utilisant le protocole LACP pour négocier les paramètres entre les deux périphériques connectés.

___
# Bibliographie

- [NetGear](https://kb.netgear.com/fr/000051185/Qu-est-ce-que-l-agr%C3%A9gation-de-liens-et-le-LACP-et-comment-puis-je-les-utiliser-dans-mon-r%C3%A9seau?language=fr)
- [Dell](https://www.dell.com/support/kbdoc/fr-fr/000121681/comment-cr%C3%A9er-et-g%C3%A9rer-l-agr%C3%A9gation-de-liens-lag-sur-un-commutateur-dell-networking-s%C3%A9rie-x)