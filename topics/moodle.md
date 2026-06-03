
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
CREATE DATABASE moodle;                                                              
CREATE USER 'moodle'@'localhost' IDENTIFIED BY 'moodle';                             
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,CREATE TEMPORARY TABLES,DROP,INDEX,ALTER ON 
moodle.* TO 'moodle'@'localhost';                                                    
```

> Создание БД moodle, пользователя moodle с паролем moodle и выдача необходимых прав

#### Установка Apache2 <!-- NAME -->

```CODE
apt-get install -y apache2 apache2-{base,httpd-prefork,mod_php8.0,mods}           
```

#### Установка PHP и модулей <!-- NAME -->

```CODE
apt-get install -y php8.0 php8.0-{curl,fileinfo,fpm-fcgi,gd,intl,ldap,mbstring,mys
qlnd,mysqlnd-mysqli,opcache,soap,sodium,xmlreader,xmlrpc,zip,openssl}                
```

#### Запуск веб-сервера <!-- NAME -->

```CODE
systemctl enable --now httpd2                                                     
```

#### Установка git <!-- NAME -->

```CODE
apt-get install -y git                                                            
```

#### Загрузка Moodle <!-- NAME -->

```CODE
git clone git://git.moodle.org/moodle.git                                         
cd moodle                                                                            
```

#### Просмотр доступных веток <!-- NAME -->

```CODE
git branch -a                                                                     
```

#### Выбор версии Moodle <!-- NAME -->

```CODE
git branch --track MOODLE_403_STABLE origin/MOODLE_403_STABLE                     
git checkout MOODLE_403_STABLE                                                       
```

> Переключение на стабильную ветку 4.03

#### Копирование в веб-каталог <!-- NAME -->

```CODE
cd ../                                                                            
cp -R moodle /var/www/html/                                                          
```

#### Создание каталога данных <!-- NAME -->

```CODE
mkdir /var/moodledata                                                             
chown -R apache2 /var/moodledata                                                     
chmod -R 777 /var/moodledata                                                         
chmod -R 0755 /var/www/html/moodle                                                   
chown -R apache2:apache2 /var/www/html/moodle                                        

```

### Настройка <!-- HEAD -->

#### Содержимое файла /etc/httpd2/conf/sites-available/moodle.conf <!-- NAME -->

```CODE
<VirtualHost *:80>                                                                
ServerName moodle.champ.first                                                    
DocumentRoot /var/www/html/moodle                                                
<Directory "/var/www/html/moodle">                                               
AllowOverride All                                                            
Options -Indexes +FollowSymLinks                                             
</Directory>                                                                     
</VirtualHost>                                                                       
```

> ServerName (доменное имя); DocumentRoot (путь к Moodle)

#### Активация конфигурации <!-- NAME -->

```CODE
ln -s /etc/httpd2/conf/sites-available/moodle.conf /etc/httpd2/conf/sites-enabled/
```

#### Настройка PHP <!-- NAME -->

```CODE
sed -i "s/; max_input_vars = 1000/max_input_vars = 5000/g"                        
/etc/php/8.0/apache2-mod_php/php.ini                                                 
```

> Увеличение max_input_vars до 5000

#### Перезапуск Apache <!-- NAME -->

```CODE
systemctl restart httpd2                                                          

```

### Веб-установщик <!-- HEAD -->

#### Параметры установки <!-- LIST -->
- Язык: Русский
- Каталог данных: /var/moodledata
- Тип БД: MariaDB (родной/mariadb)
- Сервер БД: localhost
- Название БД: moodle
- Пользователь БД: moodle
- Пароль БД: moodle
- Префикс таблиц: mdl_
- Порт БД: 3306
- Логин администратора: admin
- Пароль, имя, фамилия: указать свои
- Электронная почта: любая
- Страна: выбрать
- Самостоятельная регистрация: Отключить
