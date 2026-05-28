
### Установка <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install haproxy                                                                  
   
 
```

#### Включение и запуск службы <!-- NAME -->

```CODE
systemctl enable --now haproxy

 
```

### Настройка HAProxy <!-- HEAD -->

#### Конфигурация в /etc/haproxy/haproxy.cfg <!-- NAME -->

```CODE
global                                                                                   
      log /dev/log daemon                                                                     
      chroot /var/lib/haproxy                                                                 
      maxconn 4000                                                                            
      user _haproxy                                                                           
      group _haproxy                                                                          
      daemon                                                                                  
      stats socket /var/lib/haproxy/stats                                                     
                                                                                              
  defaults                                                                                    
      mode http                                                                               
      log global                                                                              
      timeout connect 10s                                                                     
      timeout client 1m                                                                       
      timeout server 1m                                                                       
                                                                                              
  listen stats                                                                                
      bind 0.0.0.0:8989
      mode http                                                                               
      stats enable
      stats uri /haproxy_stats                                                                
      stats realm HAProxy\ Statistics                                                         
      stats auth admin:toor                                                                   
      stats admin if TRUE                                                                     
                                                                                              
  frontend postgre                                                                            
      bind 0.0.0.0:5432                                                                       
      default_backend POSTGRE                                                                 
                                                                                              
  backend POSTGRE                                                                             
      balance roundrobin                                                                      
      server srv-hq 192.168.11.65:5432 check                                                  
      server srv-br 192.168.33.67:5432 check                                                  
 
```

> global(глобальные параметры); log(логирование); chroot(изоляция процесса); maxconn(максимум соединений); user/group(пользователь процесса); stats socket(сокет для статистики); defaults(параметры по умолчанию); mode(режим работы) {http, tcp}; timeout(таймауты подключения); listen stats(веб-интерфейс статистики); stats auth(логин:пароль для доступа); frontend(входящие подключения); backend(серверы назначения); balance(метод балансировки); server(адрес сервера); check(проверка доступности)

### Методы балансировки <!-- HEAD -->

> roundrobin(циклическое распределение запросов, все серверы равны)

> leastconn(запросы на сервер с наименьшим количеством соединений, для долгих соединений)

> source(один IP клиента всегда на один сервер)

> uri(одинаковые URI на один сервер, для статики и API)

> url_param(балансировка по параметру URL, например ?session_id=123)

> hdr(одинаковые HTTP-заголовки на один сервер, например User-Agent или Cookie)

> rdp-cookie(балансировка по RDP Cookie для RDP-серверов)

> random(случайный сервер, приоритет настраивается через random[start_weight])

> first(всегда первый доступный сервер, для failover)

### Проверка HAProxy <!-- HEAD -->

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status haproxy                                                                 
                                                                                              
 
```

#### Доступ к веб-статистике <!-- NAME -->

```CODE
http://IP_СЕРВЕРА:8989/haproxy_stats                                                     
 
```

> Логин и пароль из параметра stats auth
