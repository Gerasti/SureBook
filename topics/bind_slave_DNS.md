
### Настройка slave DNS-сервера <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get update && apt-get install -y bind bind-utils                                     

```

#### Базовые параметры в /etc/bind/options.conf <!-- NAME -->

```CODE
listen-on { any; };                                                                      
allow-query { any; };                                                                       
allow-transfer { none; };                                                                   

```

#### Настройка slave-зон в /etc/bind/local.conf <!-- NAME -->

```CODE
zone "bind.domain" {                                                                     
type slave;                                                                             
file "slave/bind.domain";                                                               
masters { 192.168.11.67; };                                                             
};                                                                                          

zone "11.168.192.in-addr.arpa" {                                                            
type slave; 
file "slave/11.168.192.in-addr.arpa.db";                                                
masters { 192.168.11.67; };                                                             
};                                                                                          

zone "33.168.192.in-addr.arpa" {                                                            
type slave;                                                                             
file "slave/33.168.192.in-addr.arpa.db";                                                
masters { 192.168.11.67; };                                                             
};                                                                                          
```

> type slave(вторичный сервер); masters(IP master-сервера для синхронизации)

#### Содержимое /etc/net/ifaces/ens33/resolv.conf <!-- NAME -->

```CODE
search bind.domain                                                                       
nameserver 192.168.11.67                                                                    
nameserver 192.168.33.67                                                                    
nameserver 8.8.8.8                                                                          

```

#### Перезапуск сети и запуск BIND <!-- NAME -->

```CODE
systemctl restart network                                                                
systemctl enable --now bind                                                                 

```

#### Включение slave-режима <!-- NAME -->

```CODE
control bind-slave enabled                                                               

```

### Проверка slave-режима <!-- HEAD -->

#### Проверка синхронизированных зон <!-- NAME -->

```CODE
ls -l /etc/bind/zone/slave/                                                              
```

> Должны появиться файлы зон, скопированные с master-сервера
