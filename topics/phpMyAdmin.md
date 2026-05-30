
### Установка <!-- HEAD -->

#### Установка MariaDB <!-- NAME -->

```CODE
apt-get update -y && apt-get install -y mariadb-server                                   
                                                                                              
 
```

#### Запуск MariaDB <!-- NAME -->

```CODE
systemctl enable --now mariadb                                                           
                                                                                              
 
```

#### Установка PHP расширений для phpMyAdmin <!-- NAME -->

```CODE
apt-get install -y php8.2 php8.2-{fpm-fcgi,mbstring,zip,gd,libs,mysqlnd,mysqlnd-mysqli,bz
  2,curl,mcrypt,opcache,openssl} libmcrypt wget                                               
 
```

> Расширения для дополнительных функций и производительности phpMyAdmin

#### Загрузка phpMyAdmin <!-- NAME -->

```CODE
wget https://files.phpmyadmin.net/phpMyAdmin/5.2.1/phpMyAdmin-5.2.1-all-languages.zip    
 
```

> Ссылку на последнюю версию копировать со страницы https://docs.phpmyadmin.net

#### Распаковка архива <!-- NAME -->

```CODE
unzip phpMyAdmin-5.2.1-all-languages.zip                                                 
                                                                                              
 
```

#### Перемещение в рабочую директорию <!-- NAME -->

```CODE
mv phpMyAdmin-5.2.1-all-languages /usr/share/phpmyadmin                                  
                                                                                              
 
```

#### Создание директории для временных файлов <!-- NAME -->

```CODE
mkdir -p /var/lib/phpmyadmin/tmp                                                         
                                                                                              
 
```

#### Установка веб-сервера Apache <!-- NAME -->

```CODE
apt-get install -y httpd2 apache2-{httpd-prefork,mod_php8.2}                             
                                                                                              
 
```

#### Назначение владельца файлов phpMyAdmin <!-- NAME -->

```CODE
chown -R apache2:apache2 /usr/share/phpmyadmin                                           
  chown -R apache2:apache2 /var/lib/phpmyadmin                                                
 
```

> apache2(пользователь веб-сервера)

#### Создание конфигурационного файла phpMyAdmin <!-- NAME -->

```CODE
cp /usr/share/phpmyadmin/config.sample.inc.php /usr/share/phpmyadmin/config.inc.php      
                                                                                              
 
```

#### Создание базы данных и таблиц phpMyAdmin <!-- NAME -->

```CODE
mariadb < /usr/share/phpmyadmin/sql/create_tables.sql                                    
 
```

> Создание базы данных хранилища конфигурации

#### Создание пользователя pma для phpMyAdmin <!-- NAME -->

```CODE
mariadb                                                                                  
  GRANT SELECT, INSERT, UPDATE, DELETE ON phpmyadmin.* TO 'pma'@'localhost' IDENTIFIED BY     
  'P@ssw0rd';                                                                                 
  EXIT;                                                                                       
 
```

> pma(пользователь для административных задач phpMyAdmin)

### Настройка <!-- HEAD -->

#### В /usr/share/phpmyadmin/config.inc.php параметр blowfish_secret <!-- NAME -->

```CODE
$cfg['blowfish_secret'] = 'случайная_строка_32_символа';
 
```

> Строка из 32 случайных символов для шифрования AES

> Если короче 32 символов - менее надежные куки

#### Генерация случайной строки для blowfish_secret <!-- NAME -->

```CODE
openssl rand -base64 32                                                                  
 
```

> Генерирует случайную строку, результат скопировать в config.inc.php

> Альтернативные способы {openssl rand -hex 16, pwgen 32 1, head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32}

#### Пример сгенерированной строки в config.inc.php <!-- NAME -->

```CODE
$cfg['blowfish_secret'] = 'a8b7c6d5e4f3g2h1i0j9k8l7m6n5o4p3';
 
```

> Использовать результат команды openssl rand -base64 32

#### В /usr/share/phpmyadmin/config.inc.php раскомментировать controluser и controlpass <!-- NAME -->

```CODE
$cfg['Servers'][$i]['controluser'] = 'pma';                                              
  $cfg['Servers'][$i]['controlpass'] = 'P@ssw0rd';                                            
 
```

> Пользователь для административных задач в многопользовательских сценариях

#### В /usr/share/phpmyadmin/config.inc.php раскомментировать Storage database and tables <!-- NAME -->

```CODE
$cfg['Servers'][$i]['pmadb'] = 'phpmyadmin';                                             
  $cfg['Servers'][$i]['bookmarktable'] = 'pma__bookmark';                                     
  $cfg['Servers'][$i]['relation'] = 'pma__relation';                                          
  $cfg['Servers'][$i]['table_info'] = 'pma__table_info';                                      
  $cfg['Servers'][$i]['table_coords'] = 'pma__table_coords';                                  
  $cfg['Servers'][$i]['pdf_pages'] = 'pma__pdf_pages';                                        
  $cfg['Servers'][$i]['column_info'] = 'pma__column_info';                                    
  $cfg['Servers'][$i]['history'] = 'pma__history';                                            
  $cfg['Servers'][$i]['table_uiprefs'] = 'pma__table_uiprefs';                                
  $cfg['Servers'][$i]['tracking'] = 'pma__tracking';                                          
  $cfg['Servers'][$i]['userconfig'] = 'pma__userconfig';                                      
  $cfg['Servers'][$i]['recent'] = 'pma__recent';                                              
  $cfg['Servers'][$i]['favorite'] = 'pma__favorite';                                          
  $cfg['Servers'][$i]['users'] = 'pma__users';                                                
  $cfg['Servers'][$i]['usergroups'] = 'pma__usergroups';                                      
  $cfg['Servers'][$i]['navigationhiding'] = 'pma__navigationhiding';                          
  $cfg['Servers'][$i]['savedsearches'] = 'pma__savedsearches';                                
  $cfg['Servers'][$i]['central_columns'] = 'pma__central_columns';                            
  $cfg['Servers'][$i]['designer_settings'] = 'pma__designer_settings';                        
  $cfg['Servers'][$i]['export_templates'] = 'pma__export_templates';                          
 
```

> Определение базы данных и таблиц хранилища конфигурации

#### В /usr/share/phpmyadmin/config.inc.php настроить временную директорию <!-- NAME -->

```CODE
$cfg['TempDir'] = '/var/lib/phpmyadmin/tmp';                                             
 
```

> Использование созданной ранее директории для временных файлов

#### В /usr/share/phpmyadmin/config.inc.php разрешить указывать сервер БД <!-- NAME -->

```CODE
$cfg['AllowArbitraryServer'] = true;                                                     
 
```

> Опционально, для явного указания IP-адреса или имени сервера БД

#### Настройка удалённого доступа к MariaDB в /etc/my.cnf.d/server.cnf <!-- NAME -->

```CODE
bind-address = 0.0.0.0                                                                   
  #skip-networking                                                                            
 
```

> bind-address(IP-адрес для подключений) {0.0.0.0, 192.168.1.0/24, конкретный_IP}

> 0.0.0.0(разрешено подключаться всем и отовсюду)

> skip-networking(закомментировать для разрешения сетевых подключений)

> Опционально, не влияет на работу phpMyAdmin

#### Предоставление привилегий пользователю root для удалённого доступа <!-- NAME -->

```CODE
mariadb                                                                                  
  GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'P@ssw0rd' WITH GRANT OPTION;       
  EXIT;                                                                                       
 
```

> Опционально, если необходимо удалённое подключение

> GRANT ALL PRIVILEGES(полные права на все операции)

> *.*(все базы данных и таблицы)

> 'root'@'%'(пользователь root с любого хоста)

> %(с любого хоста)

#### Запуск веб-сервера Apache <!-- NAME -->

```CODE
systemctl enable --now httpd2                                                            
                                                                                              
 
```

#### Содержимое файла /etc/httpd2/conf/sites-available/phpmyadmin.conf <!-- NAME -->

```CODE
Alias /phpmyadmin /usr/share/phpmyadmin                                                  
                                                                                              
  <Directory /usr/share/phpmyadmin>                                                           
      Options FollowSymLinks                                                                  
      DirectoryIndex index.php                                                                
      AllowOverride All
      Require all granted                                                                     
  </Directory>                                                                                
                                                                                              
 
```

#### Включение конфигурационного файла <!-- NAME -->

```CODE
a2ensite phpmyadmin                                                                      
                                                                                              
 
```

#### Проверка синтаксиса конфигурации Apache <!-- NAME -->

```CODE
apachectl configtest                                                                     
                                                                                              
 
```

#### Применение изменений Apache <!-- NAME -->

```CODE
systemctl reload httpd2                                                                  
                                                                                              
 
```

#### Исправление ошибки входа в phpMyAdmin в /etc/my.cnf.d/server.cnf <!-- NAME -->

```CODE
skip-grant-tables                                                                        
 
```

> Опционально, если возникает ошибка при входе

#### Перезагрузка MariaDB после изменений <!-- NAME -->

```CODE
systemctl restart mariadb                                                                
                                                                                              
 
```

### Проверка <!-- HEAD -->

#### Проверка открытого порта MariaDB <!-- NAME -->

```CODE
ss -tlpn | grep mysqld                                                                   
 
```

> Показывает открытый порт 3306 для удалённых подключений

#### Проверка удалённого доступа с клиента <!-- NAME -->

```CODE
mariadb -h IP_адрес_сервера -u root -p                                                   
 
```

> На клиенте должен быть установлен пакет mariadb-client

#### Доступ к phpMyAdmin <!-- NAME -->

> Открыть в браузере http://IP_адрес_сервера/phpmyadmin

> Вход под пользователем root с паролем P@ssw0rd
