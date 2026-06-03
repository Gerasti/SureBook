
### Установка <!-- HEAD -->

#### Установка nginx <!-- NAME -->

```CODE
apt-get install nginx                                                                    
 
```

#### Включение автозапуска <!-- NAME -->

```CODE
systemctl enable --now nginx                                                             
                                                                                              
 
```

### Настройка обратного прокси <!-- HEAD -->

> Для настройки необходима ip-адресация и работа DNS(или hosts)

#### Создание файла конфигурации <!-- NAME -->

```CODE
nano /etc/nginx/sites-available.d/some.domain.conf                                       
                                                                                              
 
```

#### Базовая конфигурация обратного прокси <!-- NAME -->

```CODE
server {                                                                                 
      listen 80;                                                                              
      server_name some.domain;                                                                
                                                                                              
  location / {                                                                                
      proxy_pass http://10.0.0.10:8080;                                                       
      proxy_http_version 1.1;                                                                 
                                                                                              
      proxy_set_header Host $host;                                                            
      proxy_set_header X-Real-IP $remote_addr;                                                
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                            
      proxy_set_header X-Forwarded-Proto $scheme;                                             
      proxy_set_header Connection "";                                                         
  }                                                                                           
  }                                                                                           
 
```

> listen(порт прослушивания); server_name(имя виртуального хоста); location(обработка запросов к корню)

> proxy_pass(адрес внутреннего веб-приложения); proxy_http_version(версия HTTP-протокола)

> proxy_set_header Host(передача оригинального заголовка Host); X-Real-IP(реальный IP клиента)

> X-Forwarded-For(цепочка IP-адресов); X-Forwarded-Proto(протокол http или https); Connection(управление соединением)

#### Конфигурация для нескольких приложений <!-- NAME -->

```CODE
server {                                                                                 
      listen 80;  
      server_name app1.some.domain;                                                           
                                                                                              
  location / {                                                                                
      proxy_pass http://10.0.0.10:8080;                                                       
      proxy_http_version 1.1;                                                                 
                                                                                              
      proxy_set_header Host $host;                                                            
      proxy_set_header X-Real-IP $remote_addr;                                                
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                            
      proxy_set_header X-Forwarded-Proto $scheme;                                             
  }                                                                                           
  }                                                                                           
                                                                                              
  server {        
      listen 80;                                                                              
      server_name app2.some.domain;                                                           
                                                                                              
  location / {                                                                                
      proxy_pass http://10.0.0.20:8080;                                                       
      proxy_http_version 1.1;                                                                 
                                                                                              
      proxy_set_header Host $host;                                                            
      proxy_set_header X-Real-IP $remote_addr;                                                
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                            
      proxy_set_header X-Forwarded-Proto $scheme;                                             
  }                                                                                           
  }                                                                                           
 
```

> app1.some.domain перенаправляет на 10.0.0.10:8080; app2.some.domain перенаправляет на 10.0.0.20:8080

#### Конфигурация с SSL-сертификатом <!-- NAME -->

```CODE
server {                                                                                 
      listen 443 ssl;
      server_name some.domain;                                                                
                                                                                              
  ssl_certificate /etc/letsencrypt/some.domain/cert.cer;                                      
  ssl_certificate_key /etc/letsencrypt/some.domain/cert.key;                                  
  ssl_protocols TLSv1.2 TLSv1.3;                                                              
  ssl_prefer_server_ciphers on;                                                               
                                                                                              
  location / {                                                                                
      proxy_pass http://10.0.0.10:8080;                                                       
      proxy_set_header Host $host;                                                            
      proxy_set_header X-Real-IP $remote_addr;                                                
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                            
      proxy_set_header X-Forwarded-Proto $scheme;                                             
  }                                                                                           
  }                                                                                           
 
```

> listen 443 ssl(прослушивание порта 443 с поддержкой SSL/TLS)

> ssl_certificate(путь к SSL-сертификату); ssl_certificate_key(путь к приватному ключу)

> ssl_protocols(разрешенные версии TLS); ssl_prefer_server_ciphers(приоритет шифров сервера)

#### Конфигурация с таймаутами <!-- NAME -->

```CODE
server {                                                                                 
      listen 80;  
      server_name some.domain;                                                                
                                                                                              
  location / {                                                                                
      proxy_pass http://10.0.0.10:8080;                                                       
      proxy_http_version 1.1;                                                                 
                                                                                              
      proxy_set_header Host $host;                                                            
      proxy_set_header X-Real-IP $remote_addr;                                                
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                            
      proxy_set_header X-Forwarded-Proto $scheme;                                             
                                                                                              
      proxy_connect_timeout 5s;                                                               
      proxy_send_timeout 30s;                                                                 
      proxy_read_timeout 30s;                                                                 
  }                                                                                           
  }                                                                                           
 
```

> proxy_connect_timeout(время ожидания подключения к backend); proxy_send_timeout(время отправки запроса)

> proxy_read_timeout(время ожидания ответа от backend)

#### Создание символической ссылки <!-- NAME -->

```CODE
ln -s /etc/nginx/sites-available.d/some.domain.conf /etc/nginx/sites-enabled.d/          
 
```

### Проверка <!-- HEAD -->

#### Проверка синтаксиса конфигурации <!-- NAME -->

```CODE
nginx -t                                                                                 
                                                                                              
 
```

#### Применение настроек <!-- NAME -->

```CODE
systemctl restart nginx                                                                  
 
```

> можно использовать systemctl reload nginx

#### Проверка открытых портов <!-- NAME -->

```CODE
ss -tulpn | grep nginx                                                                   
                                                                                              
 
```

#### Проверка доступности backend-сервера <!-- NAME -->

```CODE
curl -I http://10.0.0.10:8080                                                            
                                                                                              
 
```

#### Просмотр логов nginx <!-- NAME -->

```CODE
journalctl -u nginx --no-pager
```
