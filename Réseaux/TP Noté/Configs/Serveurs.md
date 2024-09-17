# VLAN SERVEURS : switch `switch_dc`

```
vlan 50
name ADMIN
exit
vlan 100
name PRODUCTION
exit

interface fa0/1
switchport mode trunk
no shutdown
exit
interface fa0/5
switchport mode trunk
no shutdown
exit

interface fa0/2
switchport mode access
switchport access vlan 50
no shutdown
exit
interface fa0/10
switchport mode access
switchport access vlan 50
no shutdown
exit
interface fa0/3
switchport mode access
switchport access vlan 50
no shutdown
exit
interface fa0/11
switchport mode access
switchport access vlan 50
no shutdown
exit
interface fa0/4
switchport mode access
switchport access vlan 100
no shutdown
exit
interface fa0/12
switchport mode access
switchport access vlan 100
no shutdown
exit
interface fa0/24
switchport mode access
switchport access vlan 50
no shutdown
exit

interface range fa0/6-9
shutdown
exit
interface range fa0/13-23
shutdown
exit
interface range gig0/1
shutdown
exit
interface range gig0/2
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
ip address 10.0.50.253 255.255.255.0
exit
ip default-gateway 10.0.50.254

ip domain-name ynov.fr
crypto key generate rsa
2048

access-list 10 permit 10.0.50.0 0.0.0.255
line vty 0 4
access-class 10 in
exit

do wr mem
```

# VLAN AIX : routeur `router_dc`

```
no ip domain-lookup

interface fa1/0
no shutdown
exit
interface gig0/0
ip address 189.122.88.2 255.255.255.252
no shutdown
exit

interface fa1/0.50
encapsulation dot1Q 50
ip address 10.0.50.252 255.255.255.0
standby 50 ip 10.0.50.254
standby 50 priority 105
standby 50 preempt
exit

interface fa1/0.100
encapsulation dot1Q 100
ip address 10.0.100.252 255.255.255.0
standby 100 ip 10.0.100.254
standby 100 priority 105
standby 100 preempt
exit

do wr mem
```

# VLAN AIX : routeur `router_dc2` (failover)

```
no ip domain-lookup

interface fa1/0
no shutdown
exit
interface gig0/0
ip address 189.122.88.6 255.255.255.252
no shutdown
exit

interface fa1/0.50
encapsulation dot1Q 50
ip address 10.0.50.253 255.255.255.0
standby 50 ip 10.0.50.254
exit
interface fa1/0.100
encapsulation dot1Q 100
ip address 10.0.100.253 255.255.255.0
standby 100 ip 10.0.100.254
exit

do wr mem
```


# OSPF SERVEURS : routeur `router_dc`

```
router ospf 100
network 189.122.88.0 255.255.255.252 area 100
network 10.0.50.0 255.255.255.0 area 100
network 10.0.100.0 255.255.255.0 area 100
exit

do wr mem
```
# OSPF SERVEURS : routeur `router_dc2`

```
router ospf 100
network 189.122.88.4 255.255.255.252 area 100
network 10.0.50.0 255.255.255.0 area 100
network 10.0.100.0 255.255.255.0 area 100
exit

do wr mem
```



# Périphériques :

#### DHCP :
10.0.50.250
#### DNS :
10.0.50.252
#### WEB :
10.0.100.1

