
### Балансировка нагрузки <!-- HEAD -->

#### Добавление блока upstream в конфигурацию сайта <!-- NAME -->

```CODE
upstream backend_site1 {
      server 192.168.1.101;                                                                   
      server 192.168.1.102;                                                                   
  }                                                                                           
                                                                                              
  server {                                                                                    
      listen 80;                                                                              
      server_name some.domain;                                                                
                                                                                              
  location / {                                                                                
      proxy_pass http://backend_site1;                                                        
      proxy_set_header Host $host;                                                            
      proxy_set_header X-Real-IP $remote_addr;                                                
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                            
      proxy_set_header X-Forwarded-Proto $scheme;                                             
  }                                                                                           
  }                                                                                           
 
```

> upstream(группа backend-серверов); backend_site1(имя группы); proxy_pass использует имя upstream

#### Метод round-robin с весами <!-- NAME -->

```CODE
upstream backend_site1 {                                                                 
      server 192.168.1.101 weight=3;                                                          
      server 192.168.1.102 weight=1;                                                          
  }                                                                                           
 
```

> weight(вес сервера, по умолчанию 1); сервер с weight=3 получит в 3 раза больше запросов

#### Метод least_conn <!-- NAME -->

```CODE
upstream backend_site1 {                                                                 
      least_conn;                                                                             
      server 192.168.1.101;                                                                   
      server 192.168.1.102;                                                                   
  }                                                                                           
 
```

> least_conn(запросы направляются на сервер с минимальным количеством активных соединений)

#### Метод ip_hash <!-- NAME -->

```CODE
upstream backend_site1 {                                                                 
      ip_hash;                                                                                
      server 192.168.1.101;                                                                   
      server 192.168.1.102;                                                                   
  }                                                                                           
 
```

> ip_hash(клиент всегда направляется на один и тот же сервер по IP-адресу)

#### Настройка keepalive соединений <!-- NAME -->

```CODE
upstream backend_site1 {                                                                 
      server 192.168.1.101;                                                                   
      server 192.168.1.102;                                                                   
      keepalive 32;                                                                           
  }                                                                                           
 
```

> keepalive(количество постоянных соединений к backend-серверам)

#### Настройка таймаутов и проверки доступности <!-- NAME -->

```CODE
upstream backend_site1 {                                                                 
      server 192.168.1.101 max_fails=3 fail_timeout=30s;                                      
      server 192.168.1.102 max_fails=3 fail_timeout=30s;                                      
  }                                                                                           
 
```

> max_fails(количество неудачных попыток); fail_timeout(время, на которое сервер считается недоступным)

#### Комбинированная конфигурация <!-- NAME -->

```CODE
upstream backend_site1 {
      least_conn;                                                                             
      server 192.168.1.101 weight=2 max_fails=3 fail_timeout=30s;                             
      server 192.168.1.102 weight=1 max_fails=3 fail_timeout=30s;                             
      keepalive 32;                                                                           
  }                                                                                           
                                                                                              
  server {                                                                                    
      listen 80;                                                                              
      server_name some.domain;                                                                
                                                                                              
  location / {                                                                                
      proxy_pass http://backend_site1;                                                        
      proxy_http_version 1.1;                                                                 
      proxy_set_header Connection "";                                                         
      proxy_set_header Host $host;                                                            
      proxy_set_header X-Real-IP $remote_addr;                                                
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                            
      proxy_set_header X-Forwarded-Proto $scheme;                                             
  }                                                                                           
  }                                                                                           
 
```

> least_conn с весами и проверкой доступности; proxy_http_version 1.1 и Connection "" для keepalive
