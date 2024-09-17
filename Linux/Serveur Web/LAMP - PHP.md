
## Choix de la version

Rocky Linux fournit de base plusieurs versions de PHP depuis l'introduction des modules DNF. Il est intéressant de noter que les versions les plus récentes de PHP ne sont pas visibles par la commande suivante :
```shell
dnf module list php
# Last metadata expiration check: 1:59:06 ago on Mon 18 Dec 2023 12:54:21 AM CET.
# AppStream
#Name           Stream            Profiles                             Summary
# php            7.2 [d]           common [d], devel, minimal           PHP scripting language
# php            7.3               common [d], devel, minimal           PHP scripting language
# php            7.4               common [d], devel, minimal           PHP scripting language
# php            8.0               common [d], devel, minimal           PHP scripting language

# Hint: [d]efault, [e]nabled, [x]disabled, [i]nstalled
```

Par défaut, la version 7.2 est celle correspondant à Rocky Linux 8. Cela dit, PHP 7.4 étant d'un part bien supérieure à ses prédécesseurs (quelle idée de ne pas avoir introduit le typage strict plus tôt...) et annoncée comme supportée jusqu'à la fin de vie de RL8, c'est celle-ci qu'on utilisera ici.

```shell
dnf module -y reset php
dnf module -y enable php:7.4
```

## Installation

S'il est possible d'installer une foule de module php à la main, on va choisir ici d'utiliser le profil `common` pour s'épargner des souffrances :
```shell
dnf module -y install php:7.4/common
```
**Note** : Il n'est en réalité pas nécessaire de préciser `/common`, puisqu'il s'agit du profil utilisé par `[d]efault` !

Pour vérifier la version :
```php -v
# PHP 7.4.33 (cli) (built: Oct 31 2022 10:36:05) ( NTS )
# Copyright (c) The PHP Group
# Zend Engine v3.4.0, Copyright (c) Zend Technologies
```

Pour vérifier que l'interprétation du php fonctionne correctement, il est possible d'utiliser la console php et de taper du code directement à l'intérieur !
```shell
php -a
php > echo "hello world!";
# hello world!
php > exit
```

## Mise en service 

Pour que le tout fonctionne avec Apache, il faut redémarrer celui-ci :
```shell
systemctl restart httpd
```

Le service associé à php est `php-fpm`. S'il n'est pas activé, il faut l'activer manuellement dans la console :

```shell
systemctl enable --now php-fpm.service
# Created symlink /etc/systemd/system/multi-user.target.wants/php-fpm.service → /usr/lib/systemd/system/php-fpm.service.

systemctl status php-fpm.service
# ● php-fpm.service - The PHP FastCGI Process Manager
#    Loaded: loaded (/usr/lib/systemd/system/php-fpm.service; enabled; vendor preset: disabled)
#    Active: active (running) since Mon 2023-12-18 03:06:27 CET; 51s ago
# Main PID: 5279 (php-fpm)
#    Status: "Processes active: 0, idle: 5, Requests: 0, slow: 0, Traffic: 0req/sec"
#     Tasks: 6 (limit: 11064)
#    Memory: 9.6M
#    CGroup: /system.slice/php-fpm.service
#            ├─5279 php-fpm: master process (/etc/php-fpm.conf)
#            ├─5280 php-fpm: pool www
#            ├─5281 php-fpm: pool www
#            ├─5282 php-fpm: pool www
#            ├─5283 php-fpm: pool www
#            └─5284 php-fpm: pool www

# Dec 18 03:06:27 rathgate.lan systemd[1]: Starting The PHP FastCGI Process Manager...
# Dec 18 03:06:27 rathgate.lan systemd[1]: Started The PHP FastCGI Process Manager.
```

Pour vérifier que le tout fonctionne, on peut créer une page php bidon à la racine des fichiers du serveur Apache, ici `var/www//html/phpinfo.php`, qui contiendra :
```php
<?php
	phpinfo();
?>
```

Plus qu'à la charger, ici à l'adresse `http://rathgate.lan/phpinfo.php` :
![[linux_8.png]]

## Configuration initiale

Le fichier `/etc/php.ini` contient toute la configuration initiale de PHP. 

Il est possible d'y modifier tout un tas de paramètres, incluant notamment l'endroit où sont enregistrés les logs liés à PHP, le type d'erreurs journalisées, etc. Non vous ne rêvez pas, toute référence à des heures de tentatives de débug liées à `php-fpm` serait purement fortuite.

Au lieu de modifier directement le fichier `php.ini`, on peut le diviser en plusieurs sous-fichiers qui eux contiendront les modifications.

### Définition du fuseau horaire

Puisque beaucoup de serveurs web ont besoin de l'heure locale du serveur, on va la définir dans un fichier `/etc/php.d/date.ini` contenant les lignes suivantes :
```ini
[Date]
; Defines the default timezone used by the date functions
; http://php.net/date.timezones
date.timezone = Europe/Paris
```

Il faut recharger Apache et php-fpm pour voir les modifications sur la page précédente :
```shell
systemctl reload httpd php-fpm
```
![[linux_9.png]]

### Relier MariaDB à PHP

Pour utiliser MariaDB à l'intérieur de php, il faut installer le module correspondant :
```shell
dnf install -y php-mysqlnd
systemctl reload httpd php-fpm
```
![[linux_10.png]]

