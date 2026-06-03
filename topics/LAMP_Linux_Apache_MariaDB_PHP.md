
### Установка LAMP-сервера <!-- HEAD -->

#### Что такое LAMP <!-- NAME -->

```CODE
LAMP = Linux + Apache + MariaDB + PHP
```

> Linux(операционная система); Apache(веб-сервер); MariaDB(система управления базами данных); PHP(язык серверной веб-разработки)

#### Установка готового набора пакетов <!-- NAME -->

```CODE
apt-get install lamp-server
```

> Устанавливает все компоненты LAMP одной командой

### Подготовка файлов сайта <!-- HEAD -->

#### Копирование файлов в директорию Apache <!-- NAME -->

```CODE
cp /mnt/web/index.php /var/www/html/
cp /mnt/web/logo.png /var/www/html/
```

> /var/www/html/(стандартная директория для файлов веб-сервера Apache)

### Настройка PHP-приложения <!-- HEAD -->

#### Редактирование файла index.php <!-- NAME -->

```CODE
nano /var/www/html/index.php

```

#### Параметры подключения к базе данных <!-- NAME -->

```CODE
$servername = "localhost";
$username = "webc";
$password = "P@ssw0rd";
$dbname = "webdb";
```

> $servername(адрес сервера базы данных); $username(пользователь MariaDB); $password(пароль пользователя); $dbname(имя базы данных)

### Настройка MariaDB <!-- HEAD -->

#### Запуск и добавление в автозагрузку <!-- NAME -->

```CODE
systemctl enable --now mariadb
```

> enable(добавить в автозагрузку); --now(запустить немедленно)

#### Подключение к MariaDB <!-- NAME -->

```CODE
mariadb -u root
```

> -u(user, указание пользователя для подключения); root(административный пользователь по умолчанию)

#### Создание базы данных <!-- NAME -->

```CODE
create database webdb;
```

> create database(создание новой базы данных); webdb(имя базы данных)

#### Создание пользователя <!-- NAME -->

```CODE
create user 'webc'@'localhost' identified by 'P@ssw0rd';
```

> create user(создание нового пользователя); 'webc'@'localhost'(имя пользователя и хост, с которого разрешено подключение); identified by(установка пароля)

#### Выдача прав пользователю <!-- NAME -->

```CODE
grant all privileges on webdb.* to 'webc'@'localhost' with grant option;
```

> grant all privileges(выдать все права); webdb.*(база данных и все её таблицы); with grant option(право передавать свои привилегии другим пользователям)

#### Выход из MariaDB <!-- NAME -->

```CODE
exit;
```

> Завершает сеанс работы с MariaDB

### Импорт базы данных <!-- HEAD -->

#### Загрузка дамп-файла в базу данных <!-- NAME -->

```CODE
mariadb -u webc -p -D webdb < /mnt/web/dump.sql
```

> -u(указание пользователя); -p(запрос пароля); -D(указание базы данных для импорта); <(перенаправление содержимого файла в команду)

### Запуск Apache <!-- HEAD -->

#### Включение автозапуска и запуск веб-сервера <!-- NAME -->

```CODE
systemctl enable --now httpd2.service
```

> httpd2.service(имя службы веб-сервера Apache в ALT Linux)

### Проверка работы <!-- HEAD -->

#### Проверка статуса MariaDB <!-- NAME -->

```CODE
systemctl status mariadb
```

> Показывает состояние службы и последние записи логов

#### Проверка статуса Apache <!-- NAME -->

```CODE
systemctl status httpd2
```

> Показывает состояние веб-сервера

#### Проверка открытых портов <!-- NAME -->

```CODE
ss -tulpn | grep -E '80|443'
```

> ss(socket statistics, утилита для просмотра сетевых соединений); -t(показать TCP-сокеты); -u(показать UDP-сокеты); -l(показать слушающие сокеты); -p(показать процессы); -n(не разрешать имена портов и адресов); grep -E '80|443'(фильтр по портам HTTP и HTTPS)

#### Проверка сайта в браузере <!-- NAME -->

```CODE
http://<IP_СЕРВЕРА>
```

> Открыть в браузере для проверки работы веб-приложения

### Управление службами <!-- HEAD -->

#### Перезапуск Apache <!-- NAME -->

```CODE
systemctl restart httpd2
```

> Применяет изменения конфигурации без перезагрузки системы

#### Перезапуск MariaDB <!-- NAME -->

```CODE
systemctl restart mariadb
```

> Перезапускает службу базы данных

#### Просмотр логов Apache <!-- NAME -->

```CODE
journalctl -u httpd2
```

> -u(фильтр по юниту службы); показывает все записи журнала для Apache

#### Просмотр логов MariaDB <!-- NAME -->

```CODE
journalctl -u mariadb
```

> Показывает журнал работы службы базы данных

#### Просмотр логов Apache в реальном времени <!-- NAME -->

```CODE
journalctl -u httpd2 -f
```

> -f(follow, следить за новыми записями)

### Устранение типичных проблем <!-- HEAD -->

#### Проблема: Apache не запускается <!-- NAME -->

```CODE
apachectl configtest
```

> Проверяет синтаксис конфигурационных файлов Apache на ошибки

#### Проблема: ошибка подключения к БД <!-- NAME -->

```CODE
mariadb -u webc -p
```

> Проверка подключения к базе данных вручную для диагностики проблем с логином, паролем или правами пользователя

#### Проверка существования базы данных <!-- NAME -->

```CODE
mariadb -u root -e "show databases;"
```

> -e(execute, выполнить SQL-команду); show databases(показать список всех баз данных)

#### Проверка прав пользователя <!-- NAME -->

```CODE
mariadb -u root -e "show grants for 'webc'@'localhost';"
```

> show grants(показать привилегии пользователя)
