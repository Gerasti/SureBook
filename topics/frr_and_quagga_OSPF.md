
### Установка FRR <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install frr                                                                      
   
 
```

#### Включение OSPF в /etc/frr/daemons <!-- NAME -->

```CODE
ospfd=yes    

 
```

#### Добавление в автозагрузку и запуск <!-- NAME -->

```CODE
systemctl enable --now frr
 
```

> FRR (Free Range Routing) - пакет протоколов маршрутизации; необходимо включить только нужные протоколы маршрутизации

### Установка Quagga (старая версия для ALT Linux) <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install quagga                                                                   
                                                                                              
 
```

#### Назначение прав <!-- NAME -->

```CODE
chown -R quagga:quagga /etc/quagga                                                       
                                                                                              
 
```

#### Включение и запуск служб <!-- NAME -->

```CODE
systemctl enable zebra ospfd                                                             
  systemctl start zebra ospfd                                                                 
 
```

> Важно включать и запускать службы отдельно

### Настройка OSPF <!-- HEAD -->

> Перед настройкой OSPF маршрутизаторы должны иметь IP-связность через GRE-туннели, VLAN, выделенные каналы или VPN

#### Полная конфигурация OSPF в vtysh <!-- NAME -->

```CODE
vtysh
  conf t       
  ip forwarding                                                                               
  router ospf     
      ospf router-id 1.1.1.1                                                                  
      network 10.10.10.0/30 area 0                                                            
      network 192.168.11.0/26 area 0                                                          
      network 192.168.11.65/28 area 0                                                         
      network 192.168.11.81/29 area 0                                                         
      passive-interface default                                                               
      area 0 authentication message-digest                                                    
  int tun                                                                                     
      no ip ospf passive                                                                      
      ip ospf message-digest-key 1 md5 P@ssw0rd                                               
      ip ospf network point-to-point                                                          
  int ens35                                                                                   
      no ip ospf passive                                                                      
  do wr mem                                                                                   
 
```

> router ospf(включение процесса OSPF); ospf router-id(уникальный идентификатор маршрутизатора); network(сети участвующие в OSPF); area 0(backbone area, центральная область OSPF); passive-interface default(все интерфейсы пассивны по умолчанию); no ip ospf passive(отключить пассивный режим); area 0 authentication message-digest(MD5-аутентификация для area); ip ospf message-digest-key(номер ключа, тип хеширования, пароль); ip ospf network(тип сети OSPF); do wr mem(сохранение конфигурации); пароли на обеих сторонах должны совпадать

### Типы сетей OSPF <!-- HEAD -->

> point-to-point(для 2 узлов, экономит трафик, multicast 224.0.0.5)

> broadcast(для >2 узлов, поддерживает DR/BDR, multicast 224.0.0.5 и 224.0.0.6)

### Проверка OSPF <!-- HEAD -->

#### Проверка соседей <!-- NAME -->

```CODE
show ip ospf neighbor                                                                    
 
```

> Показывает соседние маршрутизаторы, состояние соседства, Router ID

#### Проверка маршрутов <!-- NAME -->

```CODE
ip route show                                                                            
 
```

> Маршруты OSPF помечаются буквой O

#### Просмотр интерфейсов OSPF <!-- NAME -->

```CODE
show ip ospf interface                                                                   
                                                                                              
 
```

#### Просмотр конфигурации <!-- NAME -->

```CODE
show running-config
```
