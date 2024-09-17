# ADRESSAGE : routeur `INTERNET`

```
no ip domain-lookup

interface gig0/0
ip address 189.122.88.1 255.255.255.252
no shutdown
exit
interface gig4/0
ip address 189.122.88.5 255.255.255.252
no shutdown
exit
interface gig1/0
ip address 58.95.208.1 255.255.255.252
no shutdown
exit
interface gig2/0
ip address 122.190.101.1 255.255.255.252
no shutdown
exit
interface gig3/0
ip address 19.61.142.1 255.255.255.252
no shutdown
exit

do wr mem
```

# OSPF : routeur `INTERNET`

```
router ospf 100
network 189.122.88.0 255.255.255.252 area 100
network 189.122.88.4 255.255.255.252 area 100
network 58.95.208.0 255.255.255.252 area 100
network 122.190.101.0 255.255.255.252 area 100
network 19.61.142.0 255.255.255.252 area 100
exit

do wr mem
```