
### Установка и настройка systemd-timesyncd <!-- HEAD -->

#### Проверка установки <!-- NAME -->

```CODE
systemctl status systemd-timesyncd
 
```

> systemd-timesyncd(встроенный NTP-клиент/сервер systemd, обычно уже установлен)

#### Остановка и отключение chrony <!-- NAME -->

```CODE
systemctl stop chronyd
  systemctl disable chronyd
 
```

> systemd-timesyncd и chrony несовместимы на одной машине, работает только один NTP-сервис

### Настройка NTP-сервера <!-- HEAD -->

#### Основной конфигурационный файл <!-- NAME -->

```CODE
/etc/systemd/timesyncd.conf

 
```

#### Настройка /etc/systemd/timesyncd.conf для сервера <!-- NAME -->

```CODE
[Time]
  NTP=ntp2.vniiftri.ru
  FallbackNTP=0.pool.ntp.org 1.pool.ntp.org
 
```

> NTP(основные NTP-серверы через пробел); FallbackNTP(резервные серверы)

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart systemd-timesyncd

 
```

#### Включение службы <!-- NAME -->

```CODE
systemctl enable systemd-timesyncd

 
```

### Разрешение NTP в firewall <!-- HEAD -->

#### Разрешение UDP 123 в iptables <!-- NAME -->

```CODE
iptables -A INPUT -p udp --dport 123 -j ACCEPT
  iptables -A OUTPUT -p udp --sport 123 -j ACCEPT
 
```

> UDP порт 123 используется для NTP

#### Разрешение UDP 123 в nftables <!-- NAME -->

```CODE
nft add rule inet filter input udp dport 123 accept
  nft add rule inet filter output udp sport 123 accept

 
```

### Проверка NTP-сервера <!-- HEAD -->

#### Проверка статуса синхронизации <!-- NAME -->

```CODE
timedatectl status
 
```

> Показывает System clock synchronized, NTP service

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status systemd-timesyncd

 
```

#### Подробная информация о синхронизации <!-- NAME -->

```CODE
timedatectl timesync-status
 
```

> Показывает сервер, stratum, задержку, смещение

#### Проверка открытого UDP-порта 123 <!-- NAME -->

```CODE
ss -ulnp | grep 123

 
```

#### Просмотр логов <!-- NAME -->

```CODE
journalctl -u systemd-timesyncd

 
```

### Настройка NTP-клиента <!-- HEAD -->

#### Остановка и отключение chrony <!-- NAME -->

```CODE
systemctl stop chronyd
  systemctl disable chronyd

 
```

#### Настройка /etc/systemd/timesyncd.conf для клиента <!-- NAME -->

```CODE
[Time]
  NTP=192.168.11.67
  FallbackNTP=ntp2.vniiftri.ru
 
```

> NTP(локальный NTP-сервер); FallbackNTP(резервный внешний сервер)

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart systemd-timesyncd

 
```

#### Включение службы <!-- NAME -->

```CODE
systemctl enable systemd-timesyncd

 
```

### Проверка клиента <!-- HEAD -->

#### Проверка синхронизации <!-- NAME -->

```CODE
timedatectl status

 
```

#### Подробная информация <!-- NAME -->

```CODE
timedatectl timesync-status

 
```

#### Включение NTP-синхронизации <!-- NAME -->

```CODE
timedatectl set-ntp true
 
```

> Включает автоматическую синхронизацию времени

#### Проверка синхронизации с сервером <!-- NAME -->

```CODE
ntpdate -q 192.168.11.67
 
```

> -q(запрос без изменения времени), показывает смещение времени
