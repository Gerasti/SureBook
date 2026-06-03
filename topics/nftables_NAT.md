
### Настройка <!-- HEAD -->

#### В /etc/net/sysctl.conf изменить строку <!-- NAME -->

```CODE
net.ipv4.ip_forward = 1                                                                  
```

> Включение пересылки пакетов между интерфейсами

#### Применение изменений <!-- NAME -->

```CODE
sysctl -p                                                                                
```

#### В /etc/nftables/nftables.nft добавить таблицу NAT <!-- NAME -->

```CODE
table ip nat {                                                                           
chain postrouting {                                                                     
type nat hook postrouting priority 100; policy accept;                              
oif "ens32" masquerade                                                              
}                                                                                       
}                                                                                           
```

> table ip nat (таблица NAT); chain postrouting (обработка после маршрутизации); oif ens32 (исходящий интерфейс); masquerade (подмена адреса источника на адрес интерфейса)

#### Применение конфигурации nftables <!-- NAME -->

```CODE
nft -f /etc/nftables/nftables.nft                                                        
```

> Загрузка правил из файла

#### Включение службы nftables <!-- NAME -->

```CODE
systemctl enable nftables                                                                
systemctl restart nftables         
```
