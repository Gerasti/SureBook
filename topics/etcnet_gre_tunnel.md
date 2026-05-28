
### Настройка GRE-туннеля <!-- HEAD -->

#### Включение IP-forwarding в /etc/net/sysctl.conf <!-- NAME -->

```CODE
net.ipv4.ip_forward=1                                                                    
 
```

> Разрешает маршрутизацию пакетов между интерфейсами

#### Применение настроек sysctl <!-- NAME -->

```CODE
sysctl -p                                                                                
                                                                                              
 
```

#### Создание каталога для туннельного интерфейса <!-- NAME -->

```CODE
mkdir -p /etc/net/ifaces/tun                                                             
                                                                                              
 
```

#### Настройка параметров туннеля в /etc/net/ifaces/tun/options <!-- NAME -->

```CODE
TYPE=iptun                                                                               
  TUNTYPE=gre                                                                                 
  TUNLOCAL=172.16.4.1
  TUNREMOTE=172.16.5.1                                                                        
  TUNOPTIONS='ttl 64'                                                                         
  TUNTTL=64                                                                                   
  TUNMTU=1476                                                                                 
 
```

> TYPE=iptun(тип интерфейса - IP-туннель); TUNTYPE=gre(протокол туннелирования GRE); TUNLOCAL(локальный IP внешнего интерфейса); TUNREMOTE(удалённый IP внешнего интерфейса); TUNTTL(время жизни пакета); TUNMTU(максимальный размер пакета)

#### Настройка IP-адреса туннеля в /etc/net/ifaces/tun/ipv4address <!-- NAME -->

```CODE
10.10.10.2/30
 
```

> Внутренний IP-адрес туннеля с маской /30

#### Перезапуск сети <!-- NAME -->

```CODE
systemctl restart network                                                                
                                                                                              
 
```

> Аналогичную настройку необходимо выполнить на втором роутере с зеркальными параметрами TUNLOCAL и TUNREMOTE
