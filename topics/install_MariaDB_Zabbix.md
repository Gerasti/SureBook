
### Установка <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get install mariadb-server zabbix-server-mysql fping                                 
   
 
```

#### Включение и запуск службы <!-- NAME -->

```CODE
systemctl enable --now mysqld

 
```

### Настройка БД <!-- HEAD -->

#### Создание базы данных и пользователя <!-- NAME -->

```CODE
mysql -uroot -p
  CREATE DATABASE zabbix CHARACTER SET utf8 COLLATE utf8_bin;
  GRANT ALL PRIVILEGES ON zabbix.* TO zabbix@localhost IDENTIFIED BY 'P@ssw0rd';              
  QUIT;                                                                                       
 
```

> Пароль можно пропустить при первом входе

#### Импорт данных в БД <!-- NAME -->

```CODE
mysql -uzabbix -pP@ssw0rd zabbix <                                                       
  /usr/share/doc/zabbix-common-database-mysql-*/schema.sql                                    
  mysql -uzabbix -pP@ssw0rd zabbix < /usr/share/doc/zabbix-common-database-mysql-*/images.sql
  mysql -uzabbix -pP@ssw0rd zabbix < /usr/share/doc/zabbix-common-database-mysql-*/data.sql   
 
```

> Важно соблюдать порядок ввода команд

### Установка веб-сервера <!-- HEAD -->

#### Установка Apache и PHP <!-- NAME -->

```CODE
apt-get install apache2 apache2-mod_php8.2                                               
  systemctl enable --now httpd2                                                               
  apt-get install php8.2 php8.2-mbstring php8.2-sockets php8.2-gd php8.2-xmlreader            
  php8.2-mysqlnd-mysqli php8.2-ldap php8.2-openssl                                            
                                                                                              
 
```

#### Настройка PHP в /etc/php/8.2/apache2-mod_php/php.ini <!-- NAME -->

```CODE
memory_limit = 256M
  post_max_size = 32M                                                                         
  max_execution_time = 600                                                                    
  max_input_time = 600                                                                        
  date.timezone = Europe/Moscow                                                               
  always_populate_raw_post_data = -1                                                          
 
```

> date.timezone указать свой регион

#### Перезапуск веб-сервера <!-- NAME -->

```CODE
systemctl restart httpd2                                                                 
                                                                                              
 
```

### Настройка сервера <!-- HEAD -->

#### В /etc/zabbix/zabbix_server.conf <!-- NAME -->

```CODE
DBHost=localhost                                                                         
  DBName=zabbix                                                                               
  DBUser=zabbix                                                                               
  DBPassword=P@ssw0rd                                                                         
                                                                                              
 
```

#### Включение и запуск службы <!-- NAME -->

```CODE
systemctl enable --now zabbix_mysql                                                      
                                                                                              
 
```

### Установка веб-интерфейса <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get install zabbix-phpfrontend-apache2 zabbix-phpfrontend-php8.2                     
                                                                                              
 
```

#### Создание символической ссылки <!-- NAME -->

```CODE
ln -s /etc/httpd2/conf/addon.d/A.zabbix.conf /etc/httpd2/conf/extra-enabled/             
                                                                                              
 
```

#### Перезапуск веб-сервера <!-- NAME -->

```CODE
systemctl restart httpd2                                                                 
                                                                                              
 
```

#### Назначение прав <!-- NAME -->

```CODE
chown apache2:apache2 /var/www/webapps/zabbix/ui/conf                                    
                                                                                              
 
```

### Доступ к веб-интерфейсу <!-- HEAD -->

#### Открыть в браузере <!-- NAME -->

```CODE
http://IP_СЕРВЕРА/zabbix                                                                 
 
```

> Подключиться к БД, ввести пароль от БД

#### Вход по умолчанию <!-- NAME -->

> Логин: Admin; Пароль: zabbix
