
### Базовые команды <!-- HEAD -->

#### Очистка старых правил <!-- NAME -->

```CODE
iptables -F                                                                              
  iptables -t nat -F                                                                          
 
```

> iptables -F(очистка таблицы filter); iptables -t nat -F(очистка таблицы nat)

#### Сохранение правил <!-- NAME -->

```CODE
iptables-save > /etc/sysconfig/iptables                                                  
  systemctl enable iptables                                                                   
 
```

> Без сохранения правила будут потеряны после перезагрузки

### Включение IP Forwarding <!-- HEAD -->

#### Временное включение <!-- NAME -->

```CODE
echo 1 > /proc/sys/net/ipv4/ip_forward                                                   
                                                                                              
 
```

#### Постоянное включение в /etc/sysctl.conf <!-- NAME -->

```CODE
net.ipv4.ip_forward = 1                                                                  
                                                                                              
 
```

#### Применение изменений <!-- NAME -->

```CODE
sysctl -p                                                                                
                                                                                              
 
```

### Настройка NAT <!-- HEAD -->

#### Базовая настройка маскарадинга <!-- NAME -->

```CODE
iptables -t nat -A POSTROUTING -o ИНТЕРФЕЙС_ИНТЕРНЕТ -j MASQUERADE                       
  iptables -A FORWARD -i ИНТЕРФЕЙС_ИНТЕРНЕТ -o ИНТЕРФЕЙС_ЛОКАЛЬНЫЙ -j ACCEPT                  
  iptables -A FORWARD -i ИНТЕРФЕЙС_ЛОКАЛЬНЫЙ -o ИНТЕРФЕЙС_ИНТЕРНЕТ -m state --state           
  ESTABLISHED,RELATED -j ACCEPT                                                               
 
```

> MASQUERADE(подменяет внутренние IP внешним IP маршрутизатора); FORWARD(разрешает пересылку трафика); state ESTABLISHED,RELATED(разрешает только ответы на установленные соединения)

#### Безопасная настройка NAT с ограничением по сети <!-- NAME -->

```CODE
iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o ens33 -j MASQUERADE
  iptables -A FORWARD -i ens33 -o ens37 -s 192.168.1.0/24 -j ACCEPT                           
 
```

> -s(ограничение по исходной сети); только указанная сеть получает доступ в интернет

### Проверка правил <!-- HEAD -->

#### Просмотр текущих правил <!-- NAME -->

```CODE
iptables -L -n -v                                                                        
 
```

> -L(показать правила); -n(вывод IP без DNS); -v(подробный вывод)

#### Просмотр NAT-таблицы <!-- NAME -->

```CODE
iptables -t nat -L -n -v 
```
