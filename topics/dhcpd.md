
### Установка DHCP-сервера <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install dhcp-server                                                              
```

> Устанавливает ISC DHCP Server — стандартную реализацию DHCP для Linux

#### Определение сетевого интерфейса <!-- NAME -->

```CODE
ip a -c                                                                                  
```

> Показывает список сетевых интерфейсов с подсветкой

### Настройка основного конфигурационного файла <!-- HEAD -->

#### Редактирование /etc/dhcp/dhcpd.conf <!-- NAME -->

```CODE
default-lease-time 3600;                                                                 
max-lease-time 86400;                                                                       
authoritative;                                                                              
ddns-update-style none;                                                                     

subnet 10.21.211.0 netmask 255.255.255.0 {                                                  
range 10.21.211.10 10.21.211.230;                                                       

option routers 10.21.211.1;                                                             
option subnet-mask 255.255.255.0;                                                       
option broadcast-address 10.21.211.255;                                                 
option domain-name "example.local";                                                     
option domain-name-servers 192.168.1.1, 8.8.8.8;                                        
}                                                                                           
```

> default-lease-time(время аренды по умолчанию в секундах, 3600 = 1 час); max-lease-time(максимальное время аренды, 86400 = 24 часа); authoritative(сервер является авторитетным для данной сети); ddns-update-style(метод динамического обновления DNS: {none, interim, standard})

> subnet(определение подсети и маски, может быть несколько); range(диапазон IP-адресов для динамической выдачи); option routers(шлюз по умолчанию); option subnet-mask(маска подсети); option broadcast-address(широковещательный адрес); option domain-name(доменное имя); option domain-name-servers(DNS-серверы через запятую)

### Динамическое обновление DNS (DDNS) <!-- HEAD -->

#### Отключение DDNS <!-- NAME -->

```CODE
ddns-update-style none;                                                                  
```

> none(динамическое обновление DNS отключено, DHCP не будет обновлять записи на DNS-сервере)

#### Настройка DDNS с использованием interim <!-- NAME -->

```CODE
ddns-update-style interim;
ignore client-updates;                                                                      

zone example.local. {                                                                       
primary 192.168.1.1;                                                                    
key DHCP_UPDATER;                                                                       
}               

zone 211.21.10.in-addr.arpa. {
primary 192.168.1.1;
key DHCP_UPDATER;                                                                       
}                                                                                           
```

> interim(устаревший метод DDNS, используется для совместимости со старыми версиями BIND); ignore client-updates(игнорировать запросы клиентов на обновление DNS); zone(определение зоны DNS для обновления); primary(IP-адрес первичного DNS-сервера); key(имя ключа TSIG для аутентификации)

#### Настройка DDNS с использованием standard <!-- NAME -->

```CODE
ddns-update-style standard;
ddns-domainname "example.local";                                                            
ddns-rev-domainname "in-addr.arpa";                                                         

update-static-leases on;                                                                    
update-conflict-detection off;                                                              

zone example.local. {
primary 192.168.1.1;                                                                    
key DHCP_UPDATER;                                                                       
}                                                                                           

zone 211.21.10.in-addr.arpa. {                                                              
primary 192.168.1.1;                                                                    
key DHCP_UPDATER;                                                                       
}                                                                                           
```

> standard(современный метод DDNS согласно RFC 4702); ddns-domainname(доменное имя для прямых записей); ddns-rev-domainname(доменное имя для обратных записей); update-static-leases(обновлять DNS для статических резервирований); update-conflict-detection(проверка конфликтов имён перед обновлением)

#### Создание ключа TSIG для безопасного обновления DNS <!-- NAME -->

```CODE
dnssec-keygen -a HMAC-MD5 -b 128 -n HOST DHCP_UPDATER
```

> Генерирует ключ TSIG для аутентификации обновлений между DHCP и DNS

#### Добавление ключа TSIG в конфигурацию DHCP <!-- NAME -->

```CODE
key DHCP_UPDATER {                                                                       
algorithm hmac-md5;                                                                     
secret "base64-encoded-key-here";                                                       
}                                                                                           
```

> key(определение ключа TSIG); algorithm(алгоритм шифрования: {hmac-md5, hmac-sha1, hmac-sha256}); secret(секретный ключ в формате base64)

#### Настройка обновления только прямых или только обратных зон <!-- NAME -->

```CODE
ddns-update-style standard;
ddns-updates on;                                                                            
update-optimization off;                                                                    

subnet 10.21.211.0 netmask 255.255.255.0 {                                                  
range 10.21.211.10 10.21.211.230;                                                       

ddns-updates on;                                                                        
}                                                                                           
```

> ddns-updates(включить или отключить DDNS для конкретной подсети); update-optimization(оптимизация обновлений, отключение заставляет обновлять DNS при каждом продлении аренды)

### Резервирование IP-адреса по MAC-адресу <!-- HEAD -->

#### Добавление статического хоста <!-- NAME -->

```CODE
host Server-01 {                                                                         
hardware ethernet 00:0c:29:41:f2:9f;                                                    
fixed-address 10.21.211.5;                                                              
}                                                                                           
```

> host(имя резервирования); hardware ethernet(MAC-адрес устройства); fixed-address(фиксированный IP-адрес для этого устройства)

#### Резервирование с дополнительными параметрами <!-- NAME -->

```CODE
host Printer-Office {
hardware ethernet 00:1a:2b:3c:4d:5e;                                                    
fixed-address 10.21.211.50;                                                             
option host-name "printer.example.local";                                               
}                                                                                           
```

> option host-name(устанавливает имя хоста для устройства)

#### Резервирование с обновлением DNS <!-- NAME -->

```CODE
host Server-01 {                                                                         
hardware ethernet 00:0c:29:41:f2:9f;                                                    
fixed-address 10.21.211.5;                                                              
ddns-hostname "server01";                                                               
ddns-domainname "example.local";                                                        
}                                                                                           
```

> ddns-hostname(имя хоста для записи в DNS); ddns-domainname(доменное имя для этого хоста)

### Проверка и запуск DHCP-сервера <!-- HEAD -->

#### Проверка синтаксиса конфигурации <!-- NAME -->

```CODE
dhcpd -t -cf /etc/dhcp/dhcpd.conf                                                        
```

> -t(тестовый режим без запуска сервера); -cf(указание пути к конфигурационному файлу)

#### Проверка конфигурации с указанием интерфейса <!-- NAME -->

```CODE
dhcpd -t -cf /etc/dhcp/dhcpd.conf ens34                                                  
```

> Проверяет конфигурацию и привязку к конкретному интерфейсу

### Настройка интерфейса для DHCP-сервера <!-- HEAD -->

#### Редактирование /etc/default/isc-dhcp-server <!-- NAME -->

```CODE
DHCP_CONF=/etc/dhcp/dhcpd.conf                                                           
DHCP_PID=/var/run/dhcpd.pid                                                                 
DHCP_OPTS="-4"                                                                              

INTERFACEv4="ens34"                                                                         
INTERFACEv6=""                                                                              
```

> DHCP_CONF(путь к основному конфигурационному файлу); DHCP_PID(путь к PID-файлу процесса); DHCP_OPTS(опции запуска, -4 = только IPv4); INTERFACEv4(интерфейс для раздачи IPv4); INTERFACEv6(интерфейс для IPv6, пустое значение = отключено)

#### Альтернативный способ указания интерфейса в /etc/sysconfig/dhcpd <!-- NAME -->

```CODE
DHCPDARGS=ens34
```

> Используется в дистрибутивах на базе Red Hat/CentOS/ALT Linux

### Управление службой DHCP <!-- HEAD -->

#### Запуск и добавление в автозагрузку <!-- NAME -->

```CODE
systemctl enable --now dhcpd                                                             
```

> enable(добавить в автозагрузку); --now(запустить немедленно)

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status dhcpd                                                                   
```

> Показывает состояние процесса и последние логи

#### Перезапуск службы после изменения конфигурации <!-- NAME -->

```CODE
systemctl restart dhcpd                                                                  
```

> Требуется после любых изменений в /etc/dhcp/dhcpd.conf

#### Просмотр логов DHCP-сервера <!-- NAME -->

```CODE
journalctl -u dhcpd -f                                                                   
```

> -u(фильтр по юниту); -f(следить за новыми записями в реальном времени)

### Дополнительные опции DHCP <!-- HEAD -->

#### Настройка времени обновления адреса <!-- NAME -->

```CODE
subnet 10.21.211.0 netmask 255.255.255.0 {                                               
range 10.21.211.10 10.21.211.230;                                                       

default-lease-time 3600;                                                                
max-lease-time 86400;                                                                   
min-lease-time 1800;                                                                    
}                                                                                           
```

> min-lease-time(минимальное время аренды, 1800 = 30 минут)

#### Настройка NTP-серверов для клиентов <!-- NAME -->

```CODE
option ntp-servers 10.21.211.1, 192.168.1.2;                                             
```

> option ntp-servers(список серверов синхронизации времени)

#### Настройка доменного суффикса поиска <!-- NAME -->

```CODE
option domain-search "example.local", "backup.local";                                    
```

> option domain-search(список доменов для автодополнения при поиске хостов)

#### Настройка MTU для клиентов <!-- NAME -->

```CODE
option interface-mtu 1500;                                                               
```

> option interface-mtu(максимальный размер пакета для интерфейса в байтах)

#### Настройка WINS-серверов для Windows-клиентов <!-- NAME -->

```CODE
option netbios-name-servers 10.21.211.1;                                                 
option netbios-node-type 8;                                                                 
```

> option netbios-name-servers(WINS-серверы для разрешения NetBIOS-имён); option netbios-node-type(тип узла: {1=B-node, 2=P-node, 4=M-node, 8=H-node})

### Расширенная конфигурация <!-- HEAD -->

#### Настройка пула адресов с ограничениями <!-- NAME -->

```CODE
subnet 10.21.211.0 netmask 255.255.255.0 {                                               
pool {                                                                                  
range 10.21.211.10 10.21.211.50;                                                    
allow members of "trusted-devices";                                                 
}                                                                                       

pool {                                                                                  
range 10.21.211.100 10.21.211.200;
deny members of "trusted-devices";                                                  
}                                                                                       
}                                                                                           

group trusted-devices {
host device1 {                                                                          
hardware ethernet 00:11:22:33:44:55;                                                
}                                                                                       
}                                                                                           
```

> pool(отдельный пул адресов с правилами доступа); allow/deny members of(разрешить или запретить группе устройств)

#### Настройка DHCP Relay для удалённых подсетей <!-- NAME -->

```CODE
shared-network office-network {
subnet 10.21.211.0 netmask 255.255.255.0 {                                              
option routers 10.21.211.1;                                                         
}                                                                                       

subnet 10.21.212.0 netmask 255.255.255.0 {                                              
range 10.21.212.10 10.21.212.100;
option routers 10.21.212.1;                                                         
}                                                                                       
}                                                                                           
```

> shared-network(объединение подсетей, подключенных к одному физическому сегменту)

### Настройка DHCP-клиента <!-- HEAD -->

#### Получение IP-адреса через DHCP <!-- NAME -->

```CODE
dhcpcd                                                                                   
```

> Запускает DHCP-клиент для автоматического получения IP-адреса, шлюза и DNS

#### Получение адреса на конкретном интерфейсе <!-- NAME -->

```CODE
dhcpcd ens34                                                                             
```

> Запускает DHCP-клиент только на указанном интерфейсе

#### Принудительное обновление аренды <!-- NAME -->

```CODE
dhcpcd -n ens34                                                                          
```

> -n(запросить новый адрес вместо попытки продлить текущий)

#### Освобождение IP-адреса <!-- NAME -->

```CODE
dhcpcd -k ens34                                                                          
```

> -k(отправить DHCPRELEASE и освободить текущий адрес)

### Диагностика и мониторинг DHCP <!-- HEAD -->

#### Просмотр активных аренд <!-- NAME -->

```CODE
cat /var/lib/dhcp/dhcpd.leases                                                           
```

> Файл содержит базу данных всех выданных и истёкших аренд

#### Просмотр последних выданных адресов <!-- NAME -->

```CODE
tail -f /var/lib/dhcp/dhcpd.leases                                                       
```

> -f(следить за файлом в реальном времени)

#### Анализ DHCP-трафика <!-- NAME -->

```CODE
tcpdump -i ens34 -n port 67 or port 68                                                   
```

> Перехватывает DHCP-пакеты (порты 67=сервер, 68=клиент)

#### Проверка доступности DHCP-сервера из сети <!-- NAME -->

```CODE
nmap --script broadcast-dhcp-discover                                                    
```

> Отправляет broadcast DHCP DISCOVER для обнаружения серверов в сети

#### Мониторинг количества свободных адресов <!-- NAME -->

```CODE
grep "lease" /var/lib/dhcp/dhcpd.leases | grep -c "binding state active"                 
```

> Подсчитывает количество активных аренд

#### Проверка обновлений DNS от DHCP <!-- NAME -->

```CODE
grep "DHCID" /var/log/syslog                                                             
```

> Показывает записи об обновлениях DNS (DHCID = DHCP Client Identifier)

### Устранение типичных проблем <!-- HEAD -->

#### Проблема: DHCP не запускается <!-- NAME -->

```CODE
systemctl status dhcpd
journalctl -xeu dhcpd                                                                       
```

> Проверка ошибок в логах и статусе службы

#### Проблема: конфликт IP-адресов <!-- NAME -->

```CODE
option ping-check true;                                                                  
ping-timeout 2;                                                                             
```

> ping-check(проверять адрес через ping перед выдачей); ping-timeout(время ожидания ответа в секундах)

#### Проблема: клиенты не получают адреса <!-- NAME -->

```CODE
ip a show ens34
systemctl status firewalld                                                                  
```

> Проверка состояния интерфейса и правил firewall (должны быть открыты порты 67/udp и 68/udp)

#### Открытие портов в firewall <!-- NAME -->

```CODE
firewall-cmd --permanent --add-service=dhcp
firewall-cmd --reload                                                                       
```

> Добавляет правило для DHCP-сервиса и применяет изменения

#### Проблема: DDNS не обновляется <!-- NAME -->

```CODE
named-checkconf /etc/named.conf                                                          
journalctl -u named -f                                                                      
```

> Проверка конфигурации DNS-сервера и логов для диагностики проблем с обновлением
