
### Настройка VLAN-интерфейсов <!-- HEAD -->

### Создание VLAN-интерфейса <!-- HEAD -->

#### Создание каталога VLAN-интерфейса <!-- NAME -->

```CODE
mkdir -p /etc/net/ifaces/ens32.100                                                       
 
```

> Формат: физический_интерфейс.номер_VLAN

#### Настройка параметров в /etc/net/ifaces/ens32.100/options <!-- NAME -->

```CODE
TYPE=vlan                                                                                
  CONFIG_IPV4=yes                                                                             
  BOOTPROTO=static                                                                            
  VID=100                                                                                     
  HOST=ens32                                                                                  
 
```

> TYPE=vlan(тип интерфейса VLAN); VID(идентификатор VLAN); HOST(физический интерфейс); BOOTPROTO(протокол получения IP) {static, dhcp}; HOST(для нескольких интерфейсов) 'ens32 ens33'

#### Настройка IP-адреса в /etc/net/ifaces/ens32.100/ipv4address <!-- NAME -->

```CODE
192.168.11.67/24
                                                                                              
 
```

#### Применение изменений <!-- NAME -->

```CODE
systemctl restart network                                                                
                                                                                              
 
```

### Ручное управление VLAN <!-- HEAD -->

#### Запуск VLAN-интерфейса <!-- NAME -->

```CODE
ifup ens32.100                                                                           
                                                                                              
 
```

#### Остановка VLAN-интерфейса <!-- NAME -->

```CODE
ifdown ens32.100                                                                         
                                                                                              
 
```

### Проверка VLAN <!-- HEAD -->

#### Просмотр интерфейсов <!-- NAME -->

```CODE
ip a                                                                                     
```
