
### Настройка базовой HTTP-аутентификации <!-- HEAD -->

> Для ограничения доступа к веб-приложению через встроенную HTTP-аутентификацию nginx

#### Установка утилиты для создания файла паролей <!-- NAME -->

```CODE
apt-get install apache2-utils                                                            
                                                                                              
 
```

#### Создание файла с учётными записями <!-- NAME -->

```CODE
htpasswd -c /etc/nginx/.htpasswd WEB                                                     
 
```

> Потребуется ввести пароль: P@ssw0rd

> WEB(имя пользователя); P@ssw0rd(пароль); /etc/nginx/.htpasswd(файл хранения учётных записей)

#### В блок location добавить параметры аутентификации <!-- NAME -->

```CODE
location / { 
      auth_basic "Restricted Area";                                                           
      auth_basic_user_file /etc/nginx/.htpasswd;                                              
                                                                                              
      proxy_pass http://10.0.0.10:8080;                                                       
                                                                                              
      proxy_http_version 1.1;                                                                 
                  
      proxy_set_header Host $host;                                                            
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                            
      proxy_set_header X-Forwarded-Proto $scheme;                                             
  }                                                                                           
                                                                                              
 
```

### Проверка <!-- HEAD -->

#### Проверка корректности настроек <!-- NAME -->

```CODE
nginx -t                                                                                 
                                                                                              
 
```

#### Применение изменений <!-- NAME -->

```CODE
systemctl reload nginx 
```
