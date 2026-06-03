
### Настройка <!-- HEAD -->

#### Содержимое файла /etc/nftables/nftables.nft <!-- NAME -->

```CODE
table inet filter {                                                                      
chain input {                                                                             
type filter hook input priority filter; policy drop;                                    
ct state established,related accept                                                     
iif lo accept                                                                           
icmp type { echo-request, echo-reply } accept                                           
tcp dport { 80, 443 } accept                                                            
udp dport { 53, 123 } accept                                                            
udp dport { 67 } accept                                                                 
ip saddr { 192.168.2.0/24, 192.168.24.0/24, 10.10.10.0/30 } accept                      
}                                                                                         
chain forward {                                                                           
type filter hook forward priority filter; policy drop;                                  
ct state established,related accept                                                     
ip saddr { 192.168.2.0/24, 192.168.24.0/24, 10.10.10.0/30 } accept                      
}                                                                                         
chain output {                                                                            
type filter hook output priority filter; policy accept;                                 
ct state established,related accept                                                     
udp sport 67 udp dport 68 accept                                                        
ip protocol ospf accept                                                                 
ip daddr { 224.0.0.5, 224.0.0.6 } accept                                                
udp dport { 53, 123 } accept                                                            
udp dport { 514 } accept                                                                
tcp dport { 514 } accept                                                                
tcp dport { 80 } accept                                                                 
icmp type { echo-request, echo-reply } accept                                           
ip saddr { 192.168.2.0/24 } accept                                                      
}                                                                                         
}                                                                                           
```

> chain input (входящий); policy drop (запретить по умолчанию);

> state established,related (разрешить установленные); iif lo (loopback); icmp type (ping); tcp dport 80,443 (HTTP/HTTPS); udp dport 53,123 (DNS/NTP); udp dport 67 (DHCP); ip saddr (разрешенные подсети 192.168.2.0/24, 192.168.24.0/24, 10.10.10.0/30); chain forward (транзит); chain output (исходящий); udp sport 67 dport 68 (DHCP-клиент); ip protocol ospf (маршрутизация); ip daddr 224.0.0.5,224.0.0.6 (multicast OSPF)

### Проверка <!-- HEAD -->

#### Проверка маршрута по умолчанию <!-- NAME -->

```CODE
ip route                                                                                 
```

> Проверить наличие default via 192.168.24.1 dev ens3.100

#### Проверка доступности подсети 192.168.2.0/24 <!-- NAME -->

```CODE
ping 192.168.2.1                                                                         
```

> Проверить получение ответа от 192.168.2.1

#### Проверка доступности подсети 192.168.24.0/24 <!-- NAME -->

```CODE
ping 192.168.24.1                                                                        
```

> Проверить получение ответа от 192.168.24.1

#### Проверка доступа в интернет <!-- NAME -->

```CODE
ping 77.88.8.8
```
