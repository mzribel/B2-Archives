# VLAN PARIS : switch `switch_paris`

```
vlan 50
name ADMIN
exit
vlan 100
name TELEPHONES
exit
vlan 105
name IMPRIMANTES
exit
vlan 110
name DIRECTION
exit
vlan 115
name COMPTABILITE
exit
vlan 120
name RH
exit

interface fa0/1
switchport mode trunk
no shutdown
exit
interface fa0/2
switchport mode access
switchport voice vlan 100
switchport access vlan 110
exit
interface fa0/3
switchport mode access
switchport voice vlan 100
switchport access vlan 115
exit
interface fa0/4
switchport mode access
switchport voice vlan 100
switchport access vlan 120
exit
interface fa0/5
switchport mode access 
switchport access vlan 105
exit
interface fa0/24
switchport mode access
switchport access vlan 50
exit
interface range fa0/6-23
shutdown
exit
do wr mem
```

### SSH

```
en
conf t

aaa new-model
aaa auth
aaa authentication login LOCAL_AUTH local
line console 0
login authentication LOCAL_AUTH
line vty 0 5 
login authentication LOCAL_AUTH
username admin password admin
service password-encryption
enable password level 15 admin

ip domain-name ynov.fr
crypto key generate rsa
2048
ip ssh version 2

interface vlan 50
ip address 10.75.50.253 255.255.255.0
exit
ip default-gateway 10.75.50.254

access-list 10 permit 10.75.50.0 0.0.0.255
line vty 0 5
no transport input
transport input ssh
access-class 10 in
exit

do wr mem
```

# VLAN PARIS : routeur `router_paris`

```
no ip domain-lookup

interface fa1/0
no shutdown
exit

interface gig0/0
ip address 58.95.208.2 255.255.255.252
no shutdown
exit

interface fa1/0.50
encapsulation dot1Q 50
ip address 10.75.50.254 255.255.255.0
exit
interface fa1/0.100
encapsulation dot1Q 100
ip address 10.75.100.254 255.255.255.0
exit
interface fa1/0.105
encapsulation dot1Q 105
ip address 10.75.105.254 255.255.255.0
exit
interface fa1/0.110
encapsulation dot1Q 110
ip address 10.75.110.254 255.255.255.0
exit
interface fa1/0.115
encapsulation dot1Q 115
ip address 10.75.115.254 255.255.255.0
exit
interface fa1/0.120
encapsulation dot1Q 120
ip address 10.75.120.254 255.255.255.0
exit
do wr mem
```

# OSPF PARIS : routeur `router_paris`

```
router ospf 100
network 58.95.208.0 255.255.255.252 area 100
network 10.75.50.0 255.255.255.0 area 100
network 10.75.100.0 255.255.255.0 area 100
network 10.75.105.0 255.255.255.0 area 100
network 10.75.110.0 255.255.255.0 area 100
network 10.75.115.0 255.255.255.0 area 100
network 10.75.120.0 255.255.255.0 area 100
exit
do wr mem
```

# Périphériques :

#### PC 5 :
10.75.110.1
#### PC 6 :
10.75.115.1
#### PC 7 :
10.75.120.1
#### Printer_PARIS
10.75.105.1
