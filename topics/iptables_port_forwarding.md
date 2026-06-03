
### Проброс портов (Port Forwarding) <!-- HEAD -->

#### Перенаправление порта на внутренний сервер <!-- NAME -->

```CODE
iptables -t nat -A PREROUTING -p tcp -i ВНЕШНИЙ_ИНТЕРФЕЙС --dport ПОРТ_ВНЕШНИЙ -j DNAT   
--to-destination IP_СЕРВЕРА:ПОРТ_ВНУТРЕННИЙ
iptables -A FORWARD -p tcp -d IP_СЕРВЕРА --dport ПОРТ_ВНУТРЕННИЙ -j ACCEPT                  
```

> PREROUTING(обработка до маршрутизации); DNAT(изменение адреса назначения); --dport(внешний порт); --to-destination(внутренний IP:порт); FORWARD(разрешение пересылки)

#### Пример проброса SSH <!-- NAME -->

```CODE
iptables -t nat -A PREROUTING -p tcp -i ens33 --dport 2222 -j DNAT --to-destination
192.168.1.10:22                                                                             
iptables -A FORWARD -p tcp -d 192.168.1.10 --dport 22 -j ACCEPT

```

#### Пример проброса HTTP <!-- NAME -->

```CODE
iptables -t nat -A PREROUTING -p tcp -i ens33 --dport 80 -j DNAT --to-destination        
192.168.1.20:80                                                                             
iptables -A FORWARD -p tcp -d 192.168.1.20 --dport 80 -j ACCEPT
```
