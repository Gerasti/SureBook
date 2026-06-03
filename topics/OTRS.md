
### Установка <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get update && apt-get install -y postgresql15-server otrs otrs-apache2               

```

#### Запуск Apache <!-- NAME -->

```CODE
systemctl enable --now httpd2                                                            

```

#### Создание системных баз данных PostgreSQL <!-- NAME -->

```CODE
/etc/init.d/postgresql initdb                                                            

```

#### Запуск PostgreSQL <!-- NAME -->

```CODE
systemctl enable --now postgresql                                                        

```

#### Создание пользователя и базы данных для OTRS <!-- NAME -->

```CODE
psql -U postgres                                                                         
create database otrs;                                                                       
create user otrs with encrypted password 'P@ssw0rd';                                        
grant all privileges on database otrs to otrs;                                              
alter database otrs owner to otrs;                                                          
```

> P@ssw0rd(пароль для пользователя otrs)

### Настройка <!-- HEAD -->

#### Настройка otrs-apache2 <!-- NAME -->

```CODE
apt-get install -y apache2-httpd-prefork                                                 
a2enextra httpd-addon.d                                                                     
echo "httpd-addon.d=yes" >> /etc/httpd2/conf/extra-start.d/999-otrs.conf                    

```

#### Перезагрузка Apache <!-- NAME -->

```CODE
systemctl restart httpd2                                                                 

```

#### Веб-установщик <!-- NAME -->

> Открыть в браузере http://IP_адрес_сервера/otrs/installer.pl

#### Действия в веб-установщике <!-- LIST -->
- Принять лицензию
- Настроить базу данных
    - type database: PostgreSQL
    - host: localhost
    - database: otrs
    - user: otrs
    - password: P@ssw0rd
- Запомнить пароль администратора
- Перейти по ссылке для входа в админскую учётную запись

#### Установка модулей PostgreSQL <!-- NAME -->

```CODE
apt-get install -y postgresql15-perl perl-DBD-Pg                                         

```

#### Запуск OTRS <!-- NAME -->

```CODE
rm /var/www/webapps/otrs/var/cron/otrs_daemin dist                                       
/var/www/webapps/otrs/bin/Cron.sh start otrs                                                
```

> Устранение ошибок

### Проверка <!-- HEAD -->

> Доступ администратора: http://IP_адрес_сервера/otrs/index.pl

> Доступ пользователей: http://IP_адрес_сервера/otrs/customer.pl
