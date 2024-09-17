
### Configuration basique d'un routeur

![[reseau_1.png]]

Dans le CLI de `Router` :

```
Router>en
Router#conf t

Router(config)#interface gig9/0
Router(config-if)#ip address 192.168.1.254 255.255.255.0
Router(config-if)#no shutdown
Router(config-if)#exit

Router(config)#do wr mem
```

Dans les paramètres de `PC`, onglet `Config` :
- Dans `global/settings`, entrer `192.168.1.254` en `IPV4 / Default Gateway`
- Dans `interface/FastEthernet0` :
	- entrer `192.168.1.1` en `IPv4 Address`
	- entrer `255.255.255.0` en `Subnet Mask`


### Route statique 

Dans le CLI d'un routeur :
```
ip route [base IP] [base subnet] [IP saut 1] [IP saut 2]...
```

Pour retirer une configuration de route ou d'IP :
```
no ip route [commande inverse]
```

Pour afficher les routes, dynamiques et statiques :
```
Router(config)#do sh ip route
```

### Routage par OSPF

![[reseau_2.png]]

Dans le CLI de `Router1` dans cet exemple :
```
Router>en
Router#conf t

Router(config)#router ospf [area]
Router(config-router)#network 192.168.0.0 255.255.255.252 area [area]
Router(config-router)#network 192.168.0.4 255.255.255.252 area [area]
Router(config-router)#network 192.168.2.0 255.255.255.0 area [area]
Router(config-router)#exit

Router(config)#do wr mem
```

Explication : 
- Doivent être mentionnés avec `network` les adresses de tous les réseaux où se trouve le routeur.
- Ici on vise le routeur central, connecté :
	- à `Router0` sur le réseau `192.168.0.0/30`
	- à `Router2` sur le réseau `192.168.0.4/30`
	- à `PC1` *via* `Switch1` sur le réseau `192.168.2.0/24`
- Pour qu'une connexion via OSPF s'affiche avec `do sh ip route`, il faut que l'OSPF soit correctement configuré sur les deux réseaux à connecter. Dans l'exemple, il faudra configurer `Router0` et `Router2` de la même façon.

**Note** : Si `Switch1`, situé sous `Router1`, possédait des `VLAN`, il faudrait alors fallu toutes les renseigner.


### Création de VLAN sur un switch

![[reseau_3.png]]

#### 1. Définir les VLAN

Dans le CLI de `Switch` :
```
Switch>
Switch>en
Switch#conf t

Switch(config)#vlan 100
Switch(config-vlan)#name PC
Switch(config-vlan)#exit

Switch(config)#vlan 200
Switch(config-vlan)#name IMPRIMANTES
Switch(config-vlan)#exit

Switch(config)#vlan 500
Switch(config-vlan)#name SERVEURS
Switch(config-vlan)#exit

Switch(config)#do wr mem
```

#### 2. Relier les VLAN aux interfaces du switch

Toujours dans le CLI de `Switch` :
```
Switch>
Switch>en
Switch#conf t

Switch(config)#interface fa0/2
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 100
Switch(config-if)#exit

Switch(config)#interface fa0/3
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 200
Switch(config-if)#exit

Switch(config)#interface fa0/1
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 500
Switch(config-if)#exit

Switch(config)#do wr mem
```

**Note** : Pour un VLAN ne contenant QUE des téléphones :
```
Switch(config)#interface fa0/1
Switch(config-if)#switchport mode access
Switch(config-if)#switchport voice vlan 100
Switch(config-if)#exit
```

#### 3. Configurer l'interface reliée au routeur :

A la suite des commandes précédentes :
```
Switch(config)#interface gig0/1 [menant au routeur]
Switch(config-if)#switchport mode trunk
Switch(config-if)#exit
```

#### 2. Relier les VLAN au routeur

Ici, on va diviser l'interface du routeur sous la forme `interface fa0/1.100` pour le VLAN 100 par exemple.

Dans un premier temps, on s'assure que `Routeur` n'a aucune forme d'adresse IP actuellement assignée à l'interface cible :

![[reseau_4.png]]

Ensuite, dans le CLI de `Routeur` :
```
Router>en
Router#conf t

Router(config)#interface gig9/0.100
Router(config-subif)#encapsulation dot1Q 100
Router(config-subif)#ip address 192.168.1.254 255.255.255.0
Router(config-subif)#exit

Router(config)#interface gig9/0.200
Router(config-subif)#encapsulation dot1Q 200
Router(config-subif)#ip address 192.168.2.254 255.255.255.0
Router(config-subif)#exit

Router(config)#interface gig9/0.500
Router(config-subif)#encapsulation dot1Q 500
Router(config-subif)#ip address 192.168.5.254 255.255.255.0
Router(config-subif)#exit

Router(config)#do wr mem
```

**Notes** :
	- L'adresse IP que l'on renseigne n'est pas celle du réseau, mais celle de la passerelle du VLAN que l'on attribuera au routeur !

### Mise en place d'un serveur DHCP

- Adresse du VLAN concerné :         192.168.111.0 / 24
- ID du VLAN : 100
- Passerelle du VLAN concerné :      192.168.254
- Adresse du serveur DHCP :            192.168.101.1 / 24
- Passerelle du serveur DHCP :         192.168.101.254
   
Désactiver tous les services hors DHCPv4, puis dans la config DHCP :
![[reseau_5.png]]
**Note** : Un DNS est nécessaire, même si aucun n'est défini sur le serveur. On peut mettre l'adresse de la passerelle ou celle du serveur DHCP s'il fait aussi office de DNS.

Dans le routeur : 
```
Router>en
Router#conf t

Router(config)#interface gig9/0.100 [vlan concerné]
Router(config-subif)#ip helper-address 192.168.101.1 [adresse du DHCP]
```
