
**But**: Création d'une VM synchronisée à un serveur NTP externe, servant elle-même de serveur NTP à une deuxième VM, toutes deux sous Rocky Linux 8.

Pour plus de détails, voir l'article du [blog MicroLinux](https://blog.microlinux.fr/chrony-rocky-linux-8/) sur le sujet.

## Prérequis

- [Deux machines virtuelles basiques](https://github.com/RathGate/Linux-B2-Novak/blob/618100475c41369220b78136b76a24ef9fbaeed4/Cours/1.%20VM%20Rocky%20Linux%208.md) sous Rocky Linux 8
- Avoir chrony installé sur les deux machines (`dnf install -y chrony`)
- Modifier si besoin les [noms d'hôte des machines](https://github.com/RathGate/Linux-B2-Novak/blob/bc88dad68f8c236ab89c12916053b2ecb27a3a43/Divers/hostname.md):
  1. `hostnamectl` pour afficher le nom d'hôte actuel
  2. `hostnamectl set-hostname new-hostname` pour modifier le nom d'hôte
  3. `systemctl restart systemd-hostnamed` pour relancer le service ensuite

## Concernant Chrony:

**Fichier de configuration**: `/etc/chrony.conf`

- `chronyd` -> démon utilisé dans l'espace utilisateur
- `chronyc` -> outil en ligne de commande pour gérer `chronyd`
- `systemctl status chronyd` -> pour vérifier si le service fonctionne correctement
- `chronyc tracking` -> afficher le suivi de la synchronisation
- `chronyc sources` -> afficher les serveurs NTP auxquels la machine est connectée
- `chronyc sourcestats` -> afficher les statistiques pour les sources
- `systemctl enable chronyd --now`

## Mise en place de Chrony

**Note**: Cette mise en place est généraliste. Pour la mise en place de Chrony dans les deux VM de l'exercice, regarder aux deux points suivants.

### Configuration

- **Sauvegarder la configuration de base** (optionnel)
  `cp chrony.conf chrony.conf.orig`
- **Modifier les serveurs NTP utilisés**.
  `nano /etc/chrony.conf` et modifier les premières lignes (ici avec quatre serveurs distants situés en France):

![](https://iili.io/JoPwykQ.md.png)

### Mise en service

- **Activer au démarrage et lancer Chrony**
  `systemctl enable chronyd --now`
- **Vérifier le fonctionnement du service**
  `systemctl status chronyd`
- **Afficher la liste des serveurs auxquels la machine est connectée**
  `chronyc sources`

![enter image description here](https://i.postimg.cc/9f0rRNFp/Calque-1.png)

## 1. VM Client/Serveur NTP

**Prérequis**: Installer la VM en suivant intégralement le point précédent [Mise en place de Chrony](https://github.com/RathGate/Linux-B2-Novak/tree/main/TP/1.%20Atelier%20NTP#mise-en-place-de-chrony).

### Configuration supplémentaire en tant que serveur de temps

Dans `/etc/chrony.conf`, en plus d'avoir modifié les serveurs publics pour les quatre situés en France, il faut **décommenter les deux lignes suivantes**:

![enter image description here](https://i.postimg.cc/PqrW54wb/1.png)

La première permet d'autoriser l'accès au chrony de la machine à toutes celles présentes dans le même réseau, tandis que la deuxième permet d'afficher le serveur comme étant synchronisé avec une source.

### Ouverture du port NTP

Afin que les autres machines du réseau puissent accéder au serveur par le protocole UDP NTP, il faut autoriser l'accès externe au port 123:

- `firewall-cmd --permanent --add-service=ntp`
- `firewall-cmd --reload`

## 2. VM Client NTP

**Prérequis**: Aucun, la mise en place de Chrony interviendra un peu plus tard.

### Ajout du nom d'hôte aux hôtes connus

Si l'on souhaite transmettre à Chrony le nom d'hôte de la machine serveur et non son IP précise, il faut ajouter la liaison nom d'hôte/IP au fichier `/etc/hosts` de la machine Client.

- `ip a` dans le terminal de la VM Serveur pour récupérer son IP dans le réseau partagé:

![enter image description here](https://i.postimg.cc/fR0Lj0h4/Virtual-Box-server-chrony-26-11-2023-19-10-51.png)

- dans la VM client, ajouter les informations de la VM serveur au fichier `/etc/hosts`:

![enter image description here](https://i.postimg.cc/GpmbgBWh/1.png)

### Mise en place de Chrony

- Réaliser la mise en place complète de Chrony selon le point [Mise en place de Chrony](https://github.com/RathGate/Linux-B2-Novak/tree/main/TP/1.%20Atelier%20NTP#mise-en-place-de-chrony) plus haut, mais en mettant le nom d'hôte de la VM serveur au lieu des quatre serveurs NTP distants dans `/etc/chrony.conf`:

![enter image description here](https://i.postimg.cc/DZDLMt5j/1.png)

## 3. Vérification du fonctionnement

**VM serveur/client**:

![enter image description here](https://i.postimg.cc/6qncLWwL/Capture-d-cran-2023-11-26-192537.png)

Synchronisée avec succès avec le deuxième serveur distant de sa liste.

**VM client**:

![enter image description here](https://i.postimg.cc/vHXfRgPx/Capture-d-cran-2023-11-26-192639.png)

Synchronisée avec succès avec la VM serveur/client.
