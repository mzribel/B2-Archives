
**But** : Installation d'un serveur MariaDB dans le cadre d'une utilisation d'un serveur Web sous LAMP.

### Prérequis

- VM basique sous Rocky Linux 8
-  Configuration du serveur Apache (non-nécessaire si le SGBD est requis dans une autre situation que la mise en place d'un serveur LAMP)

## Installation et mise en service 

```shell
dnf install -y mariadb-server
systemctl enable mariadb --now
```

Une installation sécurisée peut être réalisée par le biais de l'utilitaire intégré `mysql_secure_installation`, adapté à un serveur de production. L'utilitaire permet de supprimer les éléments inutiles autrement ajoutés avec l'installation du SGBD.

```shell
mysql_secure_installation
```

Le premier prompt demande le mot de passe actuel de l'utilisateur `root`, qui par défaut est vide. Il suffit d'appuyer sur entrée. Il faudra ensuite choisir un nouveau mot de passe pour l'utilisateur `root`, de préférence différent de celui de l'utilisateur `root` du serveur :
```txt
NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MariaDB
      SERVERS IN PRODUCTION USE!  PLEASE READ EACH STEP CAREFULLY!

In order to log into MariaDB to secure it, we'll need the current
password for the root user.  If you've just installed MariaDB, and
you haven't set the root password yet, the password will be blank,
so you should just press enter here.

Enter current password for root (enter for none):
OK, successfully used password, moving on...

Setting the root password ensures that nobody can log into the MariaDB
root user without the proper authorisation.

Set root password? [Y/n] Y
New password:
Re-enter new password:
Password updated successfully!
Reloading privilege tables..
 ... Success!
```

Ensuite, plusieurs entrées nous proposeront d'interdire les connexions anonymes et retirer les comptes `root` accessibles de l'extérieur...
```txt
By default, a MariaDB installation has an anonymous user, allowing anyone
to log into MariaDB without having to have a user account created for
them.  This is intended only for testing, and to make the installation
go a bit smoother.  You should remove them before moving into a
production environment.

Remove anonymous users? [Y/n] Y
 ... Success!

Normally, root should only be allowed to connect from 'localhost'.  This
ensures that someone cannot guess at the root password from the network.

Disallow root login remotely? [Y/n] Y
 ... Success!
```

... enfin, il nous est proposé de supprimer la base de données de test et de recharger les privilèges associés aux tables :
```txt
By default, MariaDB comes with a database named 'test' that anyone can
access.  This is also intended only for testing, and should be removed
before moving into a production environment.

Remove test database and access to it? [Y/n] Y
 - Dropping test database...
 ... Success!
 - Removing privileges on test database...
 ... Success!

Reloading the privilege tables will ensure that all changes made so far
will take effect immediately.

Reload privilege tables now? [Y/n] Y
 ... Success!

Cleaning up...

All done!  If you've completed all of the above steps, your MariaDB
installation should now be secure.
```

## Post-installation 

Pour assainir entièrement la configuration du SGBD, on va d'abord se connecter à MariaDB en tant que `root`, avec le mot de passe choisi au préalable :
```shell
mysql -u root -p
#Enter password:
#Welcome to the MariaDB monitor.  Commands end with ; or \g.
#Your MariaDB connection id is 17
#Server version: 10.3.39-MariaDB MariaDB Server

#Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

#Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
MariaDB [(none)] >
```

Dans un premier temps, on va supprimer tous les utilisateurs `root` qui n'ont pas `localhost` en hôte défini :
```shell
MariaDB [(none)]> USE mysql;
MariaDB [mysql]> SELECT user, host FROM user;
#+------+-----------+
#| user | host      |
#+------+-----------+
#| root | 127.0.0.1 |
#| root | ::1       |
#| root | localhost |
#+------+-----------+
#3 rows in set (0.000 sec)

MariaDB [mysql]> DELETE FROM user WHERE host != 'localhost';
#Query OK, 2 rows affected (0.000 sec)

MariaDB [mysql]> select user, host from user;
#+------+-----------+
#| user | host      |
#+------+-----------+
#| root | localhost |
#+------+-----------+
#1 row in set (0.000 sec)
```

Plus qu'à quitter le terminal mysql et le tour est joué !
```shell
MariaDB [mysql]> QUIT;
# Bye
```