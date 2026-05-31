
### Установка и настройка dnsmasq <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install dnsmasq                                                                  
   
 
```

#### Включение автозапуска <!-- NAME -->

```CODE
systemctl enable --now dnsmasq
                                                                                              
 
```

### Настройка DNS в dnsmasq <!-- HEAD -->

#### Конфигурация DNS в /etc/dnsmasq.conf <!-- NAME -->

```CODE
listen-address=127.0.0.1,192.168.0.1                                                     
                                                                                              
  domain=no.do                                                                                
                                                                                              
  local=/home.lan/                                                                            
                  
  cache-size=1000                                                                             
                  
  server=9.9.9.9                                                                              
                  
  expand-hosts                                                                                
                  
  log-queries                                                                                 
  log-facility=/var/log/dnsmasq.log
 
```

> listen-address(IP-адреса для приёма DNS-запросов); domain(локальный домен сети); local(запрет пересылки локальной зоны во внешний DNS); cache-size(размер DNS-кэша); server(внешний DNS-сервер для пересылки); expand-hosts(использовать /etc/hosts); log-queries(логирование DNS-запросов); log-facility(файл логов)

### Настройка DHCP в dnsmasq <!-- HEAD -->

#### Конфигурация DHCP в /etc/dnsmasq.conf <!-- NAME -->

```CODE
interface=ens3                                                                           
  bind-interfaces                                                                             
                                                                                              
  dhcp-range=192.168.0.50,192.168.0.150,12h                                                   
                  
  dhcp-option=3,192.168.0.1                                                                   
  dhcp-option=6,192.168.0.1
  dhcp-option=15,no.do                                                                        
 
```

> interface(интерфейс для работы DHCP); bind-interfaces(работать только на указанном интерфейсе); dhcp-range(диапазон IP-адресов и время аренды); dhcp-option=3(шлюз по умолчанию); dhcp-option=6(DNS-сервер); dhcp-option=15(доменное имя сети)

#### Дополнительные параметры в /etc/dnsmasq.conf <!-- NAME -->

```CODE
user=nobody
  group=nogroup                                                                               
 
```

> user(пользователь процесса); group(группа процесса); except-interface(исключить интерфейс из работы dnsmasq)

#### Применение конфигурации <!-- NAME -->

```CODE
systemctl restart dnsmasq
                                                                                              
 
```

### Проверка dnsmasq <!-- HEAD -->

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status dnsmasq
```
