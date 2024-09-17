### Afficher le nom d'hôte
- `hostnamectl`
### Changer le nom d'hôte

- **Modifier le nom d'hôte**:

  `hostnamectl set-hostname new-hostname` ou modifier `/etc/hostname`,

  `hostnamectl set-hostname "displayed-new-hostname" --pretty`

- **Ajouter l'entrée dans `/etc/hosts`**

- **Relancer le service `systemd-hostnamed`**

  `systemctl restart systemd-hostnamed`

### Ajouter un nom d'hôte externe

- **Ajouter l'entrée dans `/etc/hosts`**