# VLAN LYON : switch `switch_lyon`

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
name COMMERCE
exit
vlan 115
name JURIDIQUE
exit

interface fa0/1
switchport mode trunk
no shutdown
exit
interface fa0/2
switchport mode access
switchport voice vlan 100
switchport access vlan 110
no shutdown
exit
interface fa0/3
switchport mode access
switchport voice vlan 100
switchport access vlan 115
no shutdown
exit
interface fa0/4
switchport mode access 
switchport access vlan 105
no shutdown
exit
interface fa0/24
switchport mode access
switchport access vlan 50
no shutdown
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

ip ssh version 2

interface vlan 50
ip address 10.69.50.253 255.255.255.0
exit
ip default-gateway 10.69.50.254

username admin password admin
ip domain-name ynov.fr
crypto key generate rsa
2048

access-list 10 permit 10.69.50.0 0.0.0.255
line vty 0 5
no transport input
transport input ssh
access-class 10 in
exit

do wr mem
```

# VLAN LYON : routeur `router_lyon`

```
no ip domain-lookup

interface fa1/0
no shutdown
exit
interface gig0/0
ip address 122.190.101.2 255.255.255.252
no shutdown
exit

interface fa1/0.50
encapsulation dot1Q 50
ip address 10.69.50.254 255.255.255.0
exit
interface fa1/0.100
encapsulation dot1Q 100
ip address 10.69.100.254 255.255.255.0
exit
interface fa1/0.105
encapsulation dot1Q 105
ip address 10.69.105.254 255.255.255.0
exit
interface fa1/0.110
encapsulation dot1Q 110
ip address 10.69.110.254 255.255.255.0
exit
interface fa1/0.115
encapsulation dot1Q 115
ip address 10.69.115.254 255.255.255.0
exit
do wr mem
```

# OSPF LYON : routeur `router_lyon`

```
router ospf 100
network 122.190.101.0 255.255.255.252 area 100
network 10.69.50.0 255.255.255.0 area 100
network 10.69.100.0 255.255.255.0 area 100
network 10.69.105.0 255.255.255.0 area 100
network 10.69.110.0 255.255.255.0 area 100
network 10.69.115.0 255.255.255.0 area 100
exit
do wr mem
```

# Périphériques :

#### PC 3 :
10.69.110.1
#### PC 4 :
10.69.115.1
#### Printer_LYON
10.69.105.1

