nanox
Les hôtes virtuels permettent de servir plusieurs site web sur le port 80 d'un serveur sous Apache. Ils sont particulièrement utiles pour optimiser les ressources d'un serveur web : ne mettre qu'un seul site par machine serait un potentiel gaspillage phénoménal !

**But** : Cet article a pour but de diviser notre serveur Apache en deux sites web distincts, qui seront :
- `http://documentation.rathgate.lan` qui contiendra la documentation auparavant contenue à la racine du dossier `www/html`.
- `http://example.rathgate.lan` contiendra un joli [site statique](https://github.com/cloudacademy/static-website-example) trouvé sur GitHub, réalisé par HTML UP5.
- `http://rathgate.lan` contiendra la page placeholder de Apache légèrement modifiée; elle sera remplacée plus tard pour l'installation WordPress !

Les fichiers des sites seront respectivement placés aux endroits suivants :
- `/var/www/documentation/html`
- `/var/www/example/html`
- `/var/www/default/html`

## Création des dossiers

### 1. Documentation 

Dans un premier temps, on va modifier le site actuel dans son dossier final, c'est-à-dire `/var/www/documentation/html` , puis changer les permissions pour que `root` ne soit plus le propriétaire du dossier :
``` shell
cd /var/www
mdkir -v documentation
ls
# documentation  html
mv -v html/ documentation/
chown -R rathgate:rathgate documentation/
```

### 2. Example

Ensuite, on va créer les dossiers mentionnés plus tôt `/var/www/example/html`, récupérer les fichiers du dépôt de HTML UP5, les placer correctement et modifier les permissions :
```shell
cd /var/www/
mkdir -pv example/html
# mkdir: created directory 'example'
# mkdir: created directory 'example/html'
cd example/

git clone https://github.com/cloudacademy/static-website-example
ls
# html  static-website-example
mv static-website-example/* html/
rm -r static-website-example/
# rm: descend into directory 'static-website-example/'? y
# rm: descend into directory 'static-website-example/.git'?
ls html/
# assets  error  images  index.html  LICENSE.MD  README.MD

chown -R rathgate:rathgate /var/www/example
```

### 3. Default

Enfin, on va créer l'arborescence du dernier site, et récupérer la page par défaut de Apache :

```shell
cd /var/www/
mkdir -pv default/html
# mkdir: created directory 'default'
# mkdir: created directory 'default/html'

cp -v /usr/share/testpage/index.html default/html/
# '/usr/share/testpage/index.html' -> 'default/html/index.html'
chown -R rathgate:rathgate /var/www/default/
```

Pour être sûr qu'il n'y a pas d'erreur avec le dossier et qu'il ne s'agit pas réellement de la page par défaut qui s'affiche, on va légèrement modifier le contenu de `/var/www/default/html/index.html`, à un endroit bien visible :
```html
... 
 <body>
    <h1>wow is that <strong>A RATHTEST ???</strong></h1>

    <div class='row'>
      <div class='col-sm-12 col-md-6 col-md-6 '></div>
          <p class="summary">This page is used to test the proper operation of
            an HTTP server after it has been installed on a Rocky Linux system.
            If you can read this page, it means that the software is working
            correctly.</p>
      </div>
...
```

Voilà ce qu'on devrait avoir :
```shell
cd /var/www/
ll
# total 4
# drwxr-xr-x.  3 rathgate rathgate   18 Dec 18 03:51 default
# drwxr-xr-x.  3 rathgate rathgate   18 Dec 18 03:43 documentation
# drwxr-xr-x.  4 rathgate rathgate   48 Dec 18 03:46 example
```

## Configuration des hôtes virtuels

Attention, pour une meilleure compréhension on va inverser l'ordre et commencer par le site par défaut, `http://rathgate.lan`.

Pour chaque vhost correspondra son fichier situé dans le dossier `/etc/httpd/conf.d/`. Pour rappel, ces fichiers agissent comme une extension du fichier principal `/etc/httpd/conf/httpd.conf` pour une meilleure lisibilité.

### 1. Default

Créons le premier fichier de configuration `/etc/httpd/conf.d/00-rathgate.conf`, lié à notre site par défaut.

```conf
# /etc/httpd/conf.d/00-rathgate.conf
#
# http://rathgate.lan
<VirtualHost *:80>
  ServerAdmin marianne.corbel@ynov.com
  DocumentRoot "/var/www/default/html"
  ServerName rathgate.lan
  ServerAlias rathgate
  ErrorLog logs/rathgate-error_log
  CustomLog logs/rathgate-access_log common
</VirtualHost>
```

Dans le fichier principal `/etc/httpd/conf/httpd.conf`, il faut supprimer les références aux dossiers de l'ancien site par défaut :

```conf
DocumentRoot "/var/www/html"
```
... et un peu en dessous :
```conf
<Directory "/var/www/html">
  Options Indexes FollowSymLinks
  AllowOverride None
  Require all granted
</Directory>
```
**Attention** : Il vaudrait mieux ne pas supprimer les quelques lignes entre ces deux blocs, sous peine de grandes souffrances...

On teste la nouvelle configuration et on relance Apache :
```shell
apachectl configtest
# Syntax OK
systemctl restart httpd
```

En chargeant de nouveau la page dans un navigateur, le bon site devrait s'afficher :
![[linux_1.png]]

Maintenant on prend les mêmes... et on recommence ! Ou presque.
### 2. Example 

On crée le fichier de configuration de l'hôte virtuel `/etc/httpd/conf.d/10-example.rathgate.conf` et on le remplit :
```conf
# /etc/httpd/conf.d/10-example.rathgate.conf
#
# http://example.rathgate.lan
<VirtualHost *:80>
  ServerAdmin marianne.corbel@ynov.com
  DocumentRoot "/var/www/example/html"
  ServerName example.rathgate.lan
  ServerAlias example.rathgate
  ErrorLog logs/example.rathgate-error_log
  CustomLog logs/example.rathgate-access_log common
</VirtualHost>
```

Attention : petite nuance ici. Le navigateur ne devrait pas parvenir à charger directement la page `http://example.rathgate.lan` : il faut soit l'ajouter au DNS du réseau, soit l'ajouter au fichier `hosts` de toutes les machines qui veulent y accéder, y compris le serveur lui-même (`C:\Windows\System32\drivers\etc\hosts` sur Windows et `/etc/hosts` sur Linux).
```txt
...
192.168.1.68 example.rathgate example.rathgate.lan
```
**Note** : Sur le serveur, l'adresse sera `127.0.0.1`
### 2. Documentation 

On crée le fichier de configuration de l'hôte virtuel `/etc/httpd/conf.d/20-documentation.rathgate.conf` et on le remplit :
```conf
# /etc/httpd/conf.d/20-documentationrathgate.conf
#
# http://documentation.rathgate.lan
<VirtualHost *:80>
  ServerAdmin marianne.corbel@ynov.com
  DocumentRoot "/var/www/documentation/html"
  ServerName documentation.rathgate.lan
  ServerAlias documentation.rathgate
  ErrorLog logs/documentation.rathgate-error_log
  CustomLog logs/documentation.rathgate-access_log common
</VirtualHost>
```

Attention : petite nuance ici. Le navigateur ne devrait pas parvenir à charger directement la page `http://example.rathgate.lan` : il faut soit l'ajouter au DNS du réseau, soit l'ajouter au fichier `hosts` de toutes les machines qui veulent y accéder, y compris le serveur lui-même (`C:\Windows\System32\drivers\etc\hosts` sur Windows et `/etc/hosts` sur Linux).
```txt
...
192.168.1.68 documentation.rathgate documentation.rathgate.lan
```
**Note** : Sur le serveur, l'adresse sera `127.0.0.1`

## Test des sites 

Plus qu'à tester ! Si tout se passe bien, chaque URL devrait mener à son site.

- `http://rathgate.lan` :
![[linux_2.png]]

- `http://example.rathgate.lan` :
![[linux_3.png]]

- `http://documentation.rathgate.lan` :
![[linux_4.png]]

