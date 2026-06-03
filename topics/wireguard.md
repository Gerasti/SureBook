
### Установка WireGuard <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get update && apt-get install -y wireguard-tools wireguard-tools-wg-quick
```

> wireguard-tools(утилиты для управления WireGuard); wireguard-tools-wg-quick(утилита wg-quick для быстрой настройки)

### Настройка сервера FW-L <!-- HEAD -->

#### Создание директории для ключей <!-- NAME -->

```CODE
mkdir -p /etc/wireguard/keys

```

#### Генерация ключей сервера и клиента <!-- NAME -->

```CODE
cd /etc/wireguard/keys                                                       
wg genkey | tee srv-sec.key | wg pubkey > srv-pub.key                           
wg genkey | tee cli-sec.key | wg pubkey > cli-pub.key                           
```

> wg genkey(генерация приватного ключа); wg pubkey(генерация публичного ключа из приватного); srv-sec.key(приватный ключ сервера); srv-pub.key(публичный ключ сервера); cli-sec.key(приватный ключ клиента); cli-pub.key(публичный ключ клиента)

#### Создание конфигурационного файла /etc/wireguard/wg0.conf <!-- NAME -->

```CODE
[Interface]
Address = 10.20.30.1/30                                                         
ListenPort = 51820                                                              
PrivateKey = <содержимое srv-sec.key>                                           

[Peer]                                                                          
PublicKey = <содержимое cli-pub.key>                                            
AllowedIPs = 10.20.30.2/32, 172.16.100.0/24                                     
```

> [Interface](настройки сервера); Address(адрес в VPN-сети); ListenPort(порт сервера, обычно 51820); PrivateKey(приватный ключ сервера); [Peer](настройки клиента); PublicKey(публичный ключ клиента); AllowedIPs(разрешённые маршруты от клиента)

#### Включение и автозагрузка туннельного интерфейса <!-- NAME -->

```CODE
systemctl enable --now wg-quick@wg0

```

### Настройка клиента FW-R <!-- HEAD -->

#### Создание директории для ключей <!-- NAME -->

```CODE
mkdir -p /etc/wireguard/keys

```

#### Копирование ключей с сервера <!-- NAME -->

```CODE
cd /etc/wireguard/keys
scp root@4.4.4.2:/etc/wireguard/keys/cli-sec.key ./                             
scp root@4.4.4.2:/etc/wireguard/keys/srv-pub.key ./                             
```

> Копируем приватный ключ клиента и публичный ключ сервера

#### Создание конфигурационного файла /etc/wireguard/wg0.conf <!-- NAME -->

```CODE
[Interface]                                                                  
Address = 10.20.30.2/30                                                         
PrivateKey = <содержимое cli-sec.key>                                           

[Peer]                                                                          
PublicKey = <содержимое srv-pub.key>                                            
Endpoint = 4.4.4.2:51820                                                        
AllowedIPs = 10.20.30.1/32, 192.168.100.0/24                                    
PersistentKeepalive = 25                                                        
```

> Endpoint(адрес и порт сервера); AllowedIPs(разрешённые маршруты к серверу); PersistentKeepalive(интервал проверки соединения в секундах, обычно 25)

#### Включение и автозагрузка туннельного интерфейса <!-- NAME -->

```CODE
systemctl enable --now wg-quick@wg0

```

### Разрешение WireGuard в firewall <!-- HEAD -->

#### Разрешение UDP 51820 в iptables на сервере <!-- NAME -->

```CODE
iptables -A INPUT -p udp --dport 51820 -j ACCEPT
```

> UDP порт 51820 используется для WireGuard

#### Разрешение UDP 51820 в nftables на сервере <!-- NAME -->

```CODE
nft add rule inet filter input udp dport 51820 accept                        

```

### Проверка <!-- HEAD -->

#### Проверка статуса туннеля <!-- NAME -->

```CODE
wg show wg0  
```

> Показывает информацию о туннеле, пиры, передачу данных

#### Проверка интерфейса wg0 <!-- NAME -->

```CODE
ip -c a | grep wg0                                                           

```

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status wg-quick@wg0                                                

```

#### Проверка связности через туннель <!-- NAME -->

```CODE
ping 10.20.30.2                                                              
```

> С сервера пинг клиента, с клиента ping 10.20.30.1

#### Проверка связности из LAN LEFT в LAN RIGHT <!-- NAME -->

```CODE
ping 172.16.100.10                                                           
```

> С машины в сети 192.168.100.0/24 пинг в сеть 172.16.100.0/24

### Управление туннелем <!-- HEAD -->

#### Остановка туннеля <!-- NAME -->

```CODE
systemctl stop wg-quick@wg0

```

#### Запуск туннеля <!-- NAME -->

```CODE
systemctl start wg-quick@wg0                                                 

```

#### Перезапуск туннеля <!-- NAME -->

```CODE
systemctl restart wg-quick@wg0                                               

```

#### Ручное поднятие интерфейса <!-- NAME -->

```CODE
wg-quick up wg0                                                              

```

#### Ручное отключение интерфейса <!-- NAME -->

```CODE
wg-quick down wg0                                                            

```

### Настройка динамической маршрутизации OSPF <!-- HEAD -->

#### Установка FRR на обоих серверах <!-- NAME -->

```CODE
apt-get install -y frr
```

> FRR(Free Range Routing, пакет для динамической маршрутизации OSPF, BGP)

#### Изменение конфигурации WireGuard на сервере <!-- NAME -->

```CODE
[Interface]                                                                  
Address = 10.20.30.1/30                                                         
ListenPort = 51820                                                              
PrivateKey = <содержимое srv-sec.key>                                           
Table = off                                                                     

[Peer]                                                                          
PublicKey = <содержимое cli-pub.key>
AllowedIPs = 10.20.30.2/32                                                      
```

> Table = off(отключить автоматическое управление маршрутами, маршруты будут управляться через OSPF); AllowedIPs(только адрес клиента, без сетей)

#### Изменение конфигурации WireGuard на клиенте <!-- NAME -->

```CODE
[Interface]  
Address = 10.20.30.2/30                                                         
PrivateKey = <содержимое cli-sec.key>                                           
Table = off                                                                     

[Peer]                                                                          
PublicKey = <содержимое srv-pub.key>                                            
Endpoint = 4.4.4.2:51820                                                        
AllowedIPs = 10.20.30.1/32                                                      
PersistentKeepalive = 25                                                        

```

#### Перезапуск туннеля на обоих серверах <!-- NAME -->

```CODE
systemctl restart wg-quick@wg0                                               

```

#### Включение демона OSPF на обоих серверах <!-- NAME -->

```CODE
sed -i 's/ospfd=no/ospfd=yes/g' /etc/frr/daemons                             

```

#### Запуск и автозагрузка FRR на обоих серверах <!-- NAME -->

```CODE
systemctl enable --now frr                                                   

```

#### Настройка OSPF на сервере FW-L <!-- NAME -->

```CODE
vtysh                                                                        
configure terminal                                                              
router ospf     
passive-interface default                                                       
network 10.20.30.0/30 area 0
network 192.168.100.0/24 area 0                                                 
exit                                                                            
interface wg0                                                                   
no ip ospf passive                                                              
exit                                                                            
end                                                                             
wr mem                                                                          
```

> vtysh(интерактивная оболочка FRR); router ospf(включить OSPF); passive-interface default(все интерфейсы пассивные по умолчанию); network(объявить сети в OSPF area 0); no ip ospf passive(сделать wg0 активным для OSPF); wr mem(сохранить конфигурацию)

#### Настройка OSPF на клиенте FW-R <!-- NAME -->

```CODE
vtysh
configure terminal                                                              
router ospf                                                                     
passive-interface default
network 10.20.30.0/30 area 0                                                    
network 172.16.100.0/24 area 0                                                  
exit                                                                            
interface wg0                                                                   
no ip ospf passive                                                              
exit            
end                                                                             
wr mem          

```

#### Проверка OSPF соседей <!-- NAME -->

```CODE
vtysh -c "show ip ospf neighbor"                                             
```

> Должен показать соседа в состоянии Full

#### Проверка маршрутов OSPF <!-- NAME -->

```CODE
ip -c r | grep ospf                                                          
```

> Показывает маршруты, полученные через OSPF

#### Проверка таблицы маршрутизации OSPF <!-- NAME -->

```CODE
vtysh -c "show ip route ospf"                                                

```

#### Проверка статуса OSPF <!-- NAME -->

```CODE
vtysh -c "show ip ospf"                                                      

```

#### Проверка интерфейсов OSPF <!-- NAME -->

```CODE
vtysh -c "show ip ospf interface"
```
