hostname
### Prérequis

- VM basique sous Rocky Linux 8

## Nom d'hôte

Si besoin, il peut-être intéressant de changer le nom d'hôte de la machine pour ne pas avoir à s'y référer en utilisant l'IP.
```shell
hostnamectl set-hostname rathgate.lan
reboot
```

Si le réseau dispose d'un DNS modifiable manuellement, il sera possible d'entrer directement l'alias dans les fichiers de celui-ci. Sinon, toutes les machines du réseau (y compris la VM elle-même) devront avoir l'alias dans leurs fichiers `hosts` respectifs.

Dans le fichier `/etc/hosts` de la VM sous Rocky Linux 8 :
```txt
127.0.0.1 localhost localhost.localdomain localhost4 localhost4.localdomain4
::1       localhost localhost.localdomain localhost6 locahost6.localdomain6

127.0.0.1 rathgate  rathgate.lan
```

Dans le fichier `C:\Windows\System32\drivers\etc\hosts` de la machine hôte sous Windows:
```txt
::1 localhost
127.0.0.1 localhost

192.168.1.68 rathgate.lan
```

Si tout fonctionne, toutes les machines ayant mentionné l'alias dans leur fichier `host` devraient pouvoir ping la VM :
```shell
ping rathgate.lan
# Envoi d'une requête 'ping' sur rathgate.lan (192.168.1.68) avec 32 octets de données :
# Réponse de 192.168.1.68 : octets=32 temps<1ms TTL=64
# ...
```

## Ports et pare-feu

Dans le pare-feu, il faut tout d'abord ouvrir l'accès aux ports qui serviront à accéder à Apache. Par défaut, les ports 80 (HTTP) et 443 (HTTPS) sont utilisés. Il est possible d'en changer, mais il s'agit d'une convention généralisée.

```shell
firewall-cmd --permanent --add-service=http
# success
firewall-cmd --reload
# success
firewall-cmd --list-services
# http ssh
```
**Note** : Seul le port HTTP a été ouvert ici. Il faudrait ajouter le service `https` pour ouvrir le port 443.

## Installation

Contrairement à d'autres systèmes Linux qui utilisent le paquet `apache2`, RHEL utilise `httpd` (ce qui semble revenir sensiblement au même, dénomination mise à part) :
```shell
dnf install -y httpd
```

**Note** : A l'installation, un utilisateur `apache` et un groupe `apache` seront crées pour gérer le service.

## Mise en place du serveur 

Dans un premier temps, il faut activer et lancer le serveur :
```shell 
systemctl enable httpd --now
```

On peut également installer un navigateur en mode texte ELinks pour visualiser "grossièrement" le résultat du serveur :
```shell
dnf install -y elinks
elinks http://localhost
```

Le résultat - la page affichée par défaut - devrait apparaître de cette manière :
![[linux_5.png]]

Sinon, on peut accéder à la page depuis un navigateur sur le réseau local
- soit par son IP (ici `192.168.1.68`)
- soit par son nom d'hôte (nécessite une configuration DNS ou une modification du  fichier `hosts` de la machine où se trouve le navigateur)
![[linux_6.png]]

## Configuration

La configuration du serveur Apache s'effectue avec une multitudes de fichiers au format `*.conf*`:
- Le fichier principal `/etc/httpd/conf/httpd.conf`
- Les sous-fichiers (notamment les vhosts) dans le dossier `etc/httpd/conf.d` 
- Les modules dans le dossier `etc/httpd/conf.modules.d` 

Dans la mesure où le fichier principal `/etc/httpd/conf/httpd.conf` est majoritairement rempli de commentaires et peut vite devenir illisible, il peut être intéressant d'en faire une copie vide de toute annotation :
```shell
cd /etc/httpd/conf
mv httpd.conf httpd.conf.orig
grep -Ev '^#|^$|^[ ]{4}#|^[ ]{6}#' httpd.conf.orig > httpd.conf
```
**Note** : L'expression régulière ci-dessus cherche les lignes commençant par "#" ou "$" ainsi que les lignes où ces caractères seraient indentés, le tout correspondant au format des commentaires.

### Configuration initiale

Si le serveur est utilisable en l'état, certains paramètres du fichiers `/etc/httpd/conf/httpd.conf` doivent être modifiés ou ajoutés.

```txt
ServerAdmin marianne.corbel@ynov.com
ServerName rathgate.lan
CustomLog "logs/access_log" common
AddDefaultCharset Off
```

**Remarques** : 
- `ServerAdmin` : Adresse e-mail de l'administrateur
- `ServerName` : Dans le cas d'un serveur dédié, on renseigne le nom de domaine du serveur. A noter qu'il doit s'agir dans tous les cas du *Fully Qualified Domain Name*, récupérable par le biais de `hostname --fqdn`.
- `CustomLog` : Permet une journalisation plus succincte.
- `AddDefaultCharset` : Permet aux pages hébergées d'utiliser leur propre encodage.

Ensuite, dans la mesure où les scripts CGI ne serviront pas, on peut supprimer les lignes correspondantes du fichier :
```txt
<IfModule alias_module>
    ScriptAlias /cgi-bin/ "/var/www/cgi-bin/"
</IfModule>
<Directory "/var/www/cgi-bin">
    AllowOverride None
    Options None
    Require all granted
</Directory>
```

Enfin, on teste la validité du fichier de configuration et relancer le serveur :
```shell
apachectl configtest
# Syntax OK
systemctl reload httpd
```

## Héberger un site statique 

Dans la configuration par défaut (qui peut être modifiée par le biais du fichier `/etc/httpd/conf/httpd.conf` sous la propriété `DocumentRoot`), Apache pioche les fichiers du serveur dans le dossier `/var/www/html/`.

Déjà, il peut être utile de supprimer le dossier `cgi-bin` dans la mesure où comme dit précédemment, ils ne serviront pas ici :
```shell
cd /var/www/
rmdir cgi-bin
```

Dans l'article de blog utilisé ici, [Serveur web Apache sous RL8](https://blog.microlinux.fr/apache-rocky-linux-8/) par Kiki Novak, il est proposé de piocher les fichiers dans la documentation archivée de Slackware Linux de cette manière :
```shell
cd /var/www/html/
wget -r -np -nH --cut-dirs=1 http://www.slackbook.org/html/
```

Il est également possible de prendre les fichiers sur github, par exemple ! Ici, je vais réutiliser ma documentation statique pour le projet d'Infrastructure et Réseaux réalisée en première année d'études :
```
cd /var/www/html/
git clone https://github.com/evzs/projet-uf.git
mv projet-uf/* ./
rm -r projet-uf/
```

Une fois cela fait, l'index du site devrait apparaître à la racine du dossier `/var/www/html/` :
```shell
ls /var/www/html/
# assets  exploitation.html  index.html  README.md
```

En rechargeant la page sur le navigateur (attention au cache !), la modification est effective :
![[linux_7.png]]

## Permissions des fichiers

Il est important de noter qu'Apache est dans un premier temps lancé par `root`, puis transféré à l'utilisateur spécial défini par les directives `User` et `Group` dans `/etc/httpd/conf/httpd.conf`, par défaut `apache`.

Par mesure de sécurité, il vaut mieux que les contenus d'un serveur web n'appartiennent pas aux processus faisant tourner le serveur. Dans cette optique, on va les attribuer à un utilisateur non-privilégié et restreindre les droits d'accès du groupe :
```shell
chown -R rathgate:rathgate /var/www/html/
cd /var/www/html/
find . -type d -exec chmod 0755 {} \;
find . -type f -exec chmod 0644 {} \;
```

**Note** : Attention à ne pas modifier l'utilisateur `apache` sous `User` et `Group` dans la configuration d'apache. Si à première vue le serveur semble tourner correctement, les choses se corsent passablement lorsque `php-fpm` est appelé, lançant à tout-va des erreurs 503 pouvant coûter plusieurs heures de cassage de tête à un développeur fatigué...