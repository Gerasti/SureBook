
### Проброс портов в nftables <!-- HEAD -->

#### Перенаправление порта на внутренний сервер <!-- NAME -->

```CODE
nft add rule ip nat PREROUTING iifname "ВНЕШНИЙ_ИНТЕРФЕЙС" tcp dport ПОРТ_ВНЕШНИЙ dnat to
IP_СЕРВЕРА:ПОРТ_ВНУТРЕННИЙ                                                                 
nft add rule ip filter FORWARD ip daddr IP_СЕРВЕРА tcp dport ПОРТ_ВНУТРЕННИЙ accept         
```

> PREROUTING(обработка до маршрутизации); dnat to(изменение адреса назначения); iifname(входящий интерфейс); FORWARD(разрешение пересылки)

#### Пример проброса SSH <!-- NAME -->

```CODE
nft add rule ip nat PREROUTING iifname "ens33" tcp dport 2222 dnat to 192.168.1.10:22
nft add rule ip filter FORWARD ip daddr 192.168.1.10 tcp dport 22 accept                    

```

#### Пример проброса HTTP <!-- NAME -->

```CODE
nft add rule ip nat PREROUTING iifname "ens33" tcp dport 80 dnat to 192.168.1.20:80      
nft add rule ip filter FORWARD ip daddr 192.168.1.20 tcp dport 80 accept 
```
