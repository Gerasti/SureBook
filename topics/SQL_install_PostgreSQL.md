
### Установка <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get install -y postgresql16 postgresql16-server postgresql16-contrib                 
```

> postgresql16-contrib(дополнительные модули и утилиты)

#### Создание системных БД <!-- NAME -->

```CODE
/etc/init.d/postgresql initdb

```

#### Запуск службы <!-- NAME -->

```CODE
systemctl enable --now postgresql                                                        

```

#### Установка пароля для пользователя postgres <!-- NAME -->

```CODE
psql -U postgres                                                                         
ALTER USER postgres WITH PASSWORD 'P@ssw0rd';                                               
\q                                                                                          

```

### Настройка <!-- HEAD -->

#### Разрешение доступа из сети в /var/lib/pgsql/data/postgresql.conf <!-- NAME -->

```CODE
listen_addresses = '*'                                                                   
```

> Найти listen_addresses = 'localhost' и заменить на '*'

> listen_addresses(адреса для прослушивания) {'*', 'localhost', '192.168.1.1'}

#### Перезапуск службы после изменения postgresql.conf <!-- NAME -->

```CODE
systemctl restart postgresql                                                             

```

#### Настройка парольной аутентификации в /var/lib/pgsql/data/pg_hba.conf <!-- NAME -->

```CODE
host    all             all             0.0.0.0/0               md5                      
host    replication     all             0.0.0.0/0               md5                         
```

> Добавить строки в конец файла перед секцией IPv6

> host(тип подключения) {host, local, hostssl}

> all(база данных) {all, имя_БД}

> all(пользователь) {all, имя_пользователя}

> 0.0.0.0/0(IP-адреса клиентов) {0.0.0.0/0, 192.168.1.0/24, конкретный_IP}

> md5(метод аутентификации) {md5, trust, reject, scram-sha-256}

> Первая строка для обычных подключений, вторая для репликации

#### Перезапуск службы после изменения pg_hba.conf <!-- NAME -->

```CODE
systemctl restart postgresql                                                             

```

#### Создание базы данных и пользователя <!-- NAME -->

```CODE
psql -U postgres                                                                         
CREATE DATABASE db01;                                                                       
CREATE USER user01 WITH PASSWORD 'P@ssw0rd';
GRANT ALL PRIVILEGES ON DATABASE db01 TO user01;                                            
\q                                                                                          
```

> db01(имя создаваемой БД); user01(имя пользователя)

#### Создание нескольких баз данных и пользователей <!-- NAME -->

```CODE
psql -U postgres                                                                         
CREATE DATABASE one;                                                                        
CREATE DATABASE two;                                                                        
CREATE USER oneuser WITH PASSWORD 'P@ssw0rd';                                               
CREATE USER twouser WITH PASSWORD 'P@ssw0rd';                                               
GRANT ALL PRIVILEGES ON DATABASE one TO oneuser;                                            
GRANT ALL PRIVILEGES ON DATABASE two TO twouser;                                            
\q                                                                                          

```

#### Заполнение базы данных тестовыми данными <!-- NAME -->

```CODE
pgbench -U postgres -i one                                                               
pgbench -U postgres -i two                                                                  
```

> Опционально, для тестирования производительности

### Проверка <!-- HEAD -->

#### Проверка открытого порта PostgreSQL <!-- NAME -->

```CODE
ss -tlpn | grep postgres                                                                 
```

> Показывает открытый порт 5432

#### Проверка БД и пользователей на сервере <!-- NAME -->

```CODE
psql -U postgres                                                                         
SELECT datname FROM pg_database;                                                            
SELECT usename, usesuper, usecreatedb FROM pg_catalog.pg_user;                              
\q                                                                                          
```

> Показывает список баз данных и пользователей

#### Проверка таблиц в базе данных <!-- NAME -->

```CODE
psql -U postgres                                                                         
\c one                                                                                      
\dt+                                                                                        
\c two                                                                                      
\dt+                                                                                        
\q              
```

> \c(подключение к БД); \dt+(список таблиц с размерами)

#### Локальное подключение на клиенте <!-- NAME -->

```CODE
psql -U user01 db01                                                                      
```

> Подключение к БД db01 от имени user01

#### Удалённое подключение на клиенте <!-- NAME -->

```CODE
psql -U user01 -h IP_сервера -d db01                                                     
```

> -h(хост сервера); -d(имя базы данных)
