
### Установка <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get install postgresql16-server zabbix-server-pgsql fping                            

```

#### Создание системных БД и включение в автозапуск <!-- NAME -->

```CODE
/etc/init.d/postgresql initdb
systemctl enable --now postgresql

```

### Настройка БД <!-- HEAD -->

#### Создание пользователя <!-- NAME -->

```CODE
su - postgres -s /bin/sh -c 'createuser --no-superuser --no-createdb --no-createrole
--encrypted --pwprompt zabbix'                                                              
```

> Ввести пароль для новой роли и повторить его

#### Создание базы данных <!-- NAME -->

```CODE
su - postgres -s /bin/sh -c 'createdb -O zabbix zabbix'                                  

```

#### Импорт данных в БД <!-- NAME -->

```CODE
su - postgres -s /bin/sh -c 'psql -U zabbix -f                                           
/usr/share/doc/zabbix-common-database-pgsql-*/schema.sql zabbix'                            
su - postgres -s /bin/sh -c 'psql -U zabbix -f
/usr/share/doc/zabbix-common-database-pgsql-*/images.sql zabbix'                            
su - postgres -s /bin/sh -c 'psql -U zabbix -f
/usr/share/doc/zabbix-common-database-pgsql-*/data.sql zabbix'                              
```

> Важно соблюдать порядок ввода команд

### Установка веб-сервера <!-- HEAD -->

#### Установка Apache и PHP <!-- NAME -->

```CODE
apt-get install apache2 apache2-mod_php8.2                                               
systemctl enable --now httpd2                                                               
apt-get install php8.2 php8.2-mbstring php8.2-sockets php8.2-gd php8.2-xmlreader            
php8.2-pgsql php8.2-ldap php8.2-openssl                                                     

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
systemctl enable --now zabbix_pgsql                                                      

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
