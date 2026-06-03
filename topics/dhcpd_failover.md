
### Настройка DHCP failover <!-- HEAD -->

> Failover обеспечивает отказоустойчивость DHCP: если один сервер выходит из строя, второй продолжает выдавать IP-адреса

> Общие настройки (subnets, options) выносятся в отдельные файлы и копируются на оба сервера, специфичные настройки (primary/secondary) остаются в основном файле dhcpd.conf

#### Создание директории для конфигураций на primary <!-- NAME -->

```CODE
mkdir /etc/dhcp/dhcpd.conf.d
cat /etc/dhcp/dhcpd.conf > /etc/dhcp/dhcpd.conf.d/subnets.conf                              

```

#### Настройка include в /etc/dhcp/dhcpd.conf на primary <!-- NAME -->

```CODE
echo include \"/etc/dhcp/dhcpd.conf.d/subnets.conf\"\; > /etc/dhcp/dhcpd.conf            

```

#### Настройка failover primary в /etc/dhcp/dhcpd.conf <!-- NAME -->

```CODE
failover peer "dhcp-failover" {                                                          
primary;                                                                               
address 10.10.10.101;                                                                  
port 519;                                                                              
peer address 10.10.10.102;                                                             
peer port 520;                                                                         
max-response-delay 60;                                                                 
max-unacked-updates 10;                                                                
mclt 3600;                                                                             
split 128;                                                                             
load balance max seconds 3;                                                            
}                                                                                           

include "/etc/dhcp/dhcpd.conf.d/subnets.conf";                                              
```

> primary(основной сервер); address(адрес текущего сервера); port(порт текущего сервера); peer address(адрес secondary); peer port(порт secondary); max-response-delay(секунд до признания второго сервера недоступным); max-unacked-updates(максимум пакетов bind-update); mclt(максимальное время lease без уведомления второго сервера, только на primary); split 128(распределение адресов 50/50%, только на primary); load balance max seconds(секунд ожидания ответа второго сервера)

#### Добавление failover peer в /etc/dhcp/dhcpd.conf.d/subnets.conf <!-- NAME -->

```CODE
subnet 10.10.20.0 netmask 255.255.255.0 {
option routers 10.10.20.1;                                                                
pool {                                                                                    
failover peer "dhcp-failover";                                                          
range 10.10.20.50 10.10.20.200;                                                         
}                                                                                         
}                                                                                           
```

> pool(пул адресов с failover); failover peer(указание пира для отказоустойчивости)

#### Проверка и перезапуск на primary <!-- NAME -->

```CODE
dhcpd -t -cf /etc/dhcp/dhcpd.conf                                                        
systemctl restart dhcpd                                                                     

```

#### Копирование конфигурации на secondary <!-- NAME -->

```CODE
scp -r /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.d root@10.10.10.102:/etc/dhcp/          
```

> При изменении конфигурации необходимо копировать файлы на второй сервер

#### Настройка failover secondary в /etc/dhcp/dhcpd.conf <!-- NAME -->

```CODE
failover peer "dhcp-failover" {                                                          
secondary;                                                                              
address 10.10.10.102;                                                                   
port 520;                                                                               
peer address 10.10.10.101;                                                              
peer port 519;                                                                          
max-response-delay 60;                                                                  
max-unacked-updates 10;                                                                 
load balance max seconds 3;                                                             
}                                                                                           

include "/etc/dhcp/dhcpd.conf.d/subnets.conf";                                              
```

> secondary(вторичный сервер); без параметров mclt и split так как они только на primary

#### Проверка и перезапуск на secondary <!-- NAME -->

```CODE
dhcpd -t -cf /etc/dhcp/dhcpd.conf                                                        
systemctl restart dhcpd 
```
