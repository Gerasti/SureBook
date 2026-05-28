
### Установка DHCP-сервера <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install dhcp-server                                                              
                                                                                              
 
```

#### Определение сетевого интерфейса <!-- NAME -->

```CODE
ip a -c                                                                                  
                                                                                              
 
```

#### Настройка интерфейса в /etc/sysconfig/dhcpd <!-- NAME -->

```CODE
DHCPDARGS=ens34                                                                          
 
```

> Указывает интерфейс, который будет раздавать IP-адреса

### Настройка DHCP-сервера <!-- HEAD -->

#### Основная конфигурация в /etc/dhcp/dhcpd.conf <!-- NAME -->

```CODE
ddns-update-style none;                                                                  
                                                                                              
  subnet 192.168.11.0 netmask 255.255.255.192 {                                               
          option routers                  192.168.11.1;                                       
          option domain-name              "bind.domain";                                      
          option domain-name-servers      77.88.8.8,192.168.11.1;                             
                                                                                              
          range dynamic-bootp 192.168.11.2 192.168.11.63;                                     
          default-lease-time 21600;                                                           
          max-lease-time 43200;                                                               
                                                                                              
  host R-HQ {                                                                                 
          hardware ethernet 00:0c:29:41:f2:9f;                                                
          fixed-address 192.168.11.1;                                                         
  }                                                                                           
  }                                                                                           
 
```

> subnet(определение подсети); range(диапазон выдаваемых адресов); option routers(шлюз по умолчанию); option domain-name-servers(DNS-серверы); default-lease-time(время аренды по умолчанию в секундах); max-lease-time(максимальное время аренды); host(резервирование IP по MAC-адресу)

#### Проверка конфигурации <!-- NAME -->

```CODE
dhcpd -t -cf /etc/dhcp/dhcpd.conf
                                                                                              
 
```

#### Запуск и включение службы <!-- NAME -->

```CODE
systemctl enable --now dhcpd                                                             
                                                                                              
 
```

### Проверка DHCP-сервера <!-- HEAD -->

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status dhcpd                                                                   
                                                                                              
 
```

### Настройка DHCP-клиента <!-- HEAD -->

#### Получение IP-адреса от DHCP-сервера <!-- NAME -->

```CODE
dhcpcd                                                                                   
 
```

> Клиент получит IP-адрес, шлюз и DNS-серверы из конфигурации сервера
