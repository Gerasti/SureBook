
### Установка и настройка Chrony NTP-сервера <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install -y chrony

 
```

#### Запуск службы <!-- NAME -->

```CODE
systemctl enable --now chronyd

 
```

### Настройка NTP-сервера <!-- HEAD -->

> Сервер получает время от внешнего NTP и раздаёт время клиентам

#### Отключение стандартных pool в /etc/chrony.conf <!-- NAME -->

```CODE
sed -i 's/^pool/#pool/' /etc/chrony.conf                                                 
                                                                                              
 
```

#### Добавление внешнего NTP-сервера в /etc/chrony.conf <!-- NAME -->

```CODE
server ntp2.vniiftri.ru iburst prefer minstratum 4                                       
  local stratum 5                                                                             
  allow 192.168.11.0/26                                                                       
  allow 192.168.11.64/28                                                                      
  allow 192.168.11.80/29                                                                      
  makestep 1.0 3                                                                              
 
```

> server(внешний NTP-сервер); iburst(быстрая синхронизация); prefer(предпочтительный сервер); minstratum 4(минимальный уровень источника); local stratum 5(локальный уровень сервера); allow(разрешить клиентам подключаться); makestep 1.0 3(корректировать время скачком, если расхождение больше 1 секунды, в первые 3 обновления)

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart chronyd
                                                                                              
 
```

### Разрешение NTP в firewall <!-- HEAD -->

#### Разрешение UDP 123 в iptables <!-- NAME -->

```CODE
iptables -A INPUT -p udp --dport 123 -j ACCEPT
  iptables -A OUTPUT -p udp --sport 123 -j ACCEPT                                             
 
```

> UDP порт 123 используется для NTP

#### Разрешение UDP 123 в nftables <!-- NAME -->

```CODE
nft add rule inet filter input udp dport 123 accept                                      
  nft add rule inet filter output udp sport 123 accept                                        
                                                                                              
 
```

### Проверка NTP-сервера <!-- HEAD -->

#### Проверка синхронизации <!-- NAME -->

```CODE
chronyc tracking
 
```

> Показывает текущий источник времени, stratum, смещение, стабильность

#### Проверка источников <!-- NAME -->

```CODE
chronyc sources                                                                          
 
```

> Показывает список NTP-серверов и их статус

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status chronyd                                                                 
                                                                                              
 
```

#### Проверка открытого UDP-порта 123 <!-- NAME -->

```CODE
ss -ulnp | grep 123
                                                                                              
 
```

### Настройка NTP-клиента <!-- HEAD -->

> Клиент синхронизирует время с локальным NTP-сервером

#### Установка пакета <!-- NAME -->

```CODE
apt-get install -y chrony                                                                
                                                                                              
 
```

#### Отключение стандартных pool <!-- NAME -->

```CODE
sed -i 's/^pool/#pool/' /etc/chrony.conf                                                 
                                                                                              
 
```

#### Добавление локального NTP-сервера в /etc/chrony.conf <!-- NAME -->

```CODE
echo "server 192.168.11.67 iburst" >> /etc/chrony.conf                                   
                                                                                              
 
```

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart chronyd                                                                
                                                                                              
 
```

### Проверка NTP-клиента <!-- HEAD -->

#### Проверка источников синхронизации <!-- NAME -->

```CODE
chronyc sources
 
```

> ^* означает текущий активный сервер

#### Проверка текущего времени <!-- NAME -->

```CODE
timedatectl                                                                              
                                                                                              
 
```

#### Принудительная синхронизация <!-- NAME -->

```CODE
chronyc makestep                                                                         
                                                                                              
 
```

#### Подробная статистика <!-- NAME -->

```CODE
chronyc sourcestats
```
