
### Установка <!-- HEAD -->

#### Скачивание пакетов <!-- NAME -->

```CODE
apt-get install fail2ban
```

### Преднастройка ALT Linux <!-- HEAD -->

#### Скачивание модуля python <!-- NAME -->

```CODE
apt-get install python3-module-systemd
```

#### В /etc/fail2ban/jail.conf в секции INCLUDES <!-- NAME -->

```CODE
before = paths-altlinux-systemd.conf
```

> Замена before = paths-altlinux.conf

### Настройка <!-- HEAD -->

#### Содержимое файла /etc/fail2ban/jail.d/sshd.conf <!-- NAME -->

```CODE
[sshd]
enabled = true
port = 22
maxretry = 3
bantime = 10
findtime = 60
```

> enabled(отслеживание sshd); bantime(время бана); findtime(время запоминания)

#### Запуск systemd-сервиса <!-- NAME -->

```CODE
systemctl enable --now fail2ban
```

### Проверка <!-- HEAD -->

```CODE
sudo fail2ban-client status sshd
```

> выводит забанненые адреса
