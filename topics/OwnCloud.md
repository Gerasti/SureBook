
### Установка <!-- HEAD -->

#### Установка MariaDB <!-- NAME -->

```CODE
apt-get update && apt-get install -y mariadb-server                                      

```

#### Запуск MariaDB <!-- NAME -->

```CODE
systemctl enable --now mariadb                                                           

```

#### Создание базы данных и пользователя <!-- NAME -->

```CODE
mysql -uroot                                                                             
CREATE DATABASE owncloud DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;        
GRANT ALL PRIVILEGES ON owncloud.* TO owncloud@'%' IDENTIFIED BY 'owncloud';                
EXIT;                                                                                       
```

> owncloud(имя базы данных, пользователя и пароль)

#### Установка пакетов PHP <!-- NAME -->

```CODE
apt-get install php7                                                                     
php7-{fpm-fcgi,pdo,zip,dom,intl,gd,mysqli,pdo_mysql,mbstring,json,xmlreader,curl,fileinfo}  

```

#### Запуск php-fpm <!-- NAME -->

```CODE
systemctl enable --now php7-fpm.service

```

#### Установка веб-сервера <!-- NAME -->

```CODE
apt-get install -y nginx                                                                 

```

#### Установка утилит для загрузки архива <!-- NAME -->

```CODE
apt-get install -y wget bzip2                                                            

```

#### Загрузка OwnCloud <!-- NAME -->

```CODE
cd /tmp                                                                                  
wget https://download.owncloud.com/server/stable/owncloud-complete-latest.tar.bz2           
```

> Ссылку на последнюю версию копировать со страницы https://owncloud.com/download-server/#edition

#### Создание директории для файлов OwnCloud <!-- NAME -->

```CODE
mkdir -p /var/www/webapps/owncloud                                                       

```

#### Распаковка архива <!-- NAME -->

```CODE
tar -xvjf owncloud-*.tar.bz2 -C /var/www/webapps/owncloud                                
mv /var/www/webapps/owncloud/owncloud/* /var/www/webapps/owncloud/                          
rm -rf /var/www/webapps/owncloud/owncloud/*                                                 

```

### Настройка <!-- HEAD -->

#### Содержимое файла /etc/nginx/sites-available.d/owncloud.conf <!-- NAME -->

```CODE
upstream php-handler {                                                                   
server unix:/var/run/php7-fpm/php7-fpm.sock;                                            
}                                                                                           

server {                                                                                    
listen 80;  
server_name cloud.example.com;                                                          
return 301 https://$server_name$request_uri;                                            
}                                                                                           

server {                                                                                    
listen 443 ssl;
server_name cloud.example.com;                                                          

ssl_certificate /var/lib/ssl/certs/owncloud.pem;                                        
ssl_certificate_key /var/lib/ssl/private/owncloud.key;                                  

add_header Strict-Transport-Security "max-age=15552000; includeSubDomains";             
add_header X-Content-Type-Options nosniff;                                              
add_header X-Frame-Options "SAMEORIGIN";                                                
add_header X-XSS-Protection "1; mode=block";                                            
add_header X-Robots-Tag none;                                                           
add_header X-Download-Options noopen;                                                   
add_header X-Permitted-Cross-Domain-Policies none;                                      

root /var/www/webapps/owncloud;                                                         

location = /robots.txt {                                                                
allow all;
log_not_found off;                                                                  
access_log off;                                                                     
}                                                                                       

location = /.well-known/carddav {                                                       
return 301 $scheme://$host/remote.php/dav;
}                                                                                       
location = /.well-known/caldav {
return 301 $scheme://$host/remote.php/dav;                                          
}                                                                                       

location /.well-known/acme-challenge { }                                                

client_max_body_size 512M;                                                              
fastcgi_buffers 64 4K;

gzip off;                                                                               

error_page 403 /core/templates/403.php;                                                 
error_page 404 /core/templates/404.php;

location / {                                                                            
rewrite ^ /index.php$uri;                                                           
}                                                                                       

location ~ ^/(?:build|tests|config|lib|3rdparty|templates|data)/ {                      
return 404;                                                                         
}                                                                                       
location ~ ^/(?:\.|autotest|occ|issue|indie|db_|console) {
return 404;                                                                         
}                                                                                       

location ~ ^/(?:index|remote|public|cron|core/ajax/update|status|ocs/v[12]|updater/.+|oc
s-provider/.+|core/templates/40[34])\.php(?:$|/) {
fastcgi_split_path_info ^(.+\.php)(/.*)$;                                           
include fastcgi_params;                                                             
fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;                   
fastcgi_param PATH_INFO $fastcgi_path_info;                                         
fastcgi_param HTTPS on;                                                             
fastcgi_param modHeadersAvailable true;                                             
fastcgi_param front_controller_active true;                                         
fastcgi_pass php-handler;                                                           
fastcgi_intercept_errors on;                                                        
fastcgi_request_buffering off;                                                      
}                                                                                       

location ~ ^/(?:updater|ocs-provider)(?:$|/) {                                          
try_files $uri $uri/ =404;
index index.php;                                                                    
}                                                                                       

location ~* \.(?:css|js)$ {                                                             
try_files $uri /index.php$uri$is_args$args;
add_header Cache-Control "public, max-age=7200";                                    

add_header X-Content-Type-Options nosniff;                                          
add_header X-Frame-Options "SAMEORIGIN";                                            
add_header X-XSS-Protection "1; mode=block";                                        
add_header X-Robots-Tag none;                                                       
add_header X-Download-Options noopen;                                               
add_header X-Permitted-Cross-Domain-Policies none;                                  

access_log off;                                                                     
}                                                                                       

location ~* \.(?:svg|gif|png|html|ttf|woff|ico|jpg|jpeg)$ {                             
try_files $uri /index.php$uri$is_args$args;                                         

access_log off;                                                                     
}                                                                                       
}                                                                                           

```

#### Создание символической ссылки <!-- NAME -->

```CODE
ln -s /etc/nginx/sites-available.d/owncloud.conf /etc/nginx/sites-enabled.d/             

```

#### Генерация самоподписанного сертификата <!-- NAME -->

```CODE
cd /var/lib/ssl                                                                          
openssl req -new -x509 -days 1461 -nodes -out certs/owncloud.pem -keyout                    
private/owncloud.key -subj "/C=RU/ST=SPb/L=SPb/O=Global Security/OU=IT                      
Department/CN=cloud.example.com/CN=owncloud"                                                
```

> Опционально, для тестирования

#### Запуск веб-сервера <!-- NAME -->

```CODE
systemctl enable --now nginx                                                             

```

#### Веб-установщик <!-- NAME -->

> Открыть в браузере https://IP_адрес_или_доменное_имя

> Игнорировать предупреждение безопасности при использовании самоподписанного сертификата

#### Параметры веб-установщика <!-- LIST -->
- Admin user: admin
- Admin password: P@ssw0rd
- Data folder: /var/www/webapps/owncloud/data
- Configure the database: MySQL/MariaDB
- Database user: owncloud
- Database password: owncloud
- Database host: localhost
- Нажать Finish setup
- Войти в созданную учётную запись

### Проверка <!-- HEAD -->

> Доступ к веб-интерфейсу: https://IP_адрес_или_доменное_имя
