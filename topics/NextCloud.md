
### Установка <!-- HEAD -->

#### Установка MariaDB <!-- NAME -->

```CODE
apt-get update && apt-get install -y mariadb-server                                      
```

#### Включение службы MariaDB <!-- NAME -->

```CODE
systemctl enable --now mariadb                                                           
```

#### Создание базы данных и пользователя <!-- NAME -->

```CODE
mariadb                                                                                  
CREATE USER 'nextcloud'@'localhost' IDENTIFIED BY 'P@ssw0rd';                               
CREATE DATABASE nextcloud DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;               
GRANT ALL PRIVILEGES ON nextcloud.* to nextcloud@localhost;                                 
EXIT;                                                                                       
```

> Создание БД nextcloud, пользователя nextcloud с паролем P@ssw0rd

#### Установка Apache2 <!-- NAME -->

```CODE
apt-get install -y apache2 apache2-mod_{ssl,php8.2} tzdata                               
```

#### Установка PHP8.2 и модулей <!-- NAME -->

```CODE
apt-get install -y php8.2 php8.2-{pdo_mysql,curl,dom,exif,fileinfo,gd2,gmp,imagick,intl,l
ibs,mbstring,memcached,opcache,openssl,pcntl,pdo,xmlreader,zip}                             
```

#### Включение модулей Apache2 <!-- NAME -->

```CODE
for i in dir env headers mime rewrite;do a2enmod $i;done                                 
```

#### Запуск веб-сервера <!-- NAME -->

```CODE
systemctl enable --now httpd2                                                            
```

#### Установка wget <!-- NAME -->

```CODE
apt-get install -y wget                                                                  
```

#### Загрузка Nextcloud <!-- NAME -->

```CODE
wget https://download.nextcloud.com/server/releases/latest.zip                           
```

#### Распаковка и перемещение <!-- NAME -->

```CODE
unzip latest.zip; rm -f latest.zip                                                       
cp -r nextcloud /var/www/html; rm -rf nextcloud                                             
```

#### Настройка прав доступа <!-- NAME -->

```CODE
chown -R root /var/www/html/nextcloud                                                    
mkdir /var/www/html/nextcloud/data                                                          
chown -R apache2 /var/www/html/nextcloud/{apps,config,data}/                                

```

### Настройка <!-- HEAD -->

#### Содержимое файла /etc/httpd2/conf/sites-available/nextcloud.conf <!-- NAME -->

```CODE
<VirtualHost *:80>                                                                       
DocumentRoot /var/www/html/nextcloud/                                                     
ServerName  nextcloud.champ.first                                                         

<Directory /var/www/html/nextcloud/>                                                      
Require all granted                                                                     
AllowOverride All                                                                       
Options FollowSymLinks MultiViews                                                       

<IfModule mod_dav.c>                                                                    
Dav off                                                                               
</IfModule>                                                                             
</Directory>                                                                              
</VirtualHost>                                                                              
```

> ServerName (доменное имя); DocumentRoot (путь к Nextcloud)

#### Активация конфигурации и перезапуск <!-- NAME -->

```CODE
ln -s /etc/httpd2/conf/sites-available/nextcloud.conf /etc/httpd2/conf/sites-enabled/    
systemctl restart httpd2                                                                    

```

### Веб-установщик <!-- HEAD -->

#### Параметры установки <!-- LIST -->
- Создать учётную запись администратора
- Пользователь БД: nextcloud
- Пароль БД: P@ssw0rd
- Название БД: nextcloud
- Сервер БД: localhost
