
### Установка <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install -y postgresql16-server                                                   
   
 
```

#### Создание системных БД <!-- NAME -->

```CODE
/etc/init.d/postgresql initdb

 
```

#### Включение и запуск службы <!-- NAME -->

```CODE
systemctl enable --now postgresql

 
```

#### Разрешение доступа из сети в /var/lib/pgsql/data/postgresql.conf <!-- NAME -->

```CODE
listen_addresses = '*'
 
```

> Найти строку listen_addresses = 'localhost' и заменить на listen_addresses = '*'

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart postgresql                                                             
                                                                                              
 
```

#### Установка пароля для пользователя postgres <!-- NAME -->

```CODE
psql -U postgres
  ALTER USER postgres WITH ENCRYPTED PASSWORD 'P@ssw0rd';                                     
  \q                                                                                          
                                                                                              
 
```

#### Настройка парольной аутентификации в /var/lib/pgsql/data/pg_hba.conf <!-- NAME -->

```CODE
host    all    all    0.0.0.0/0    md5                                                   
 
```

> Разрешает подключение с любого IP с парольной аутентификацией

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart postgresql                                                             
                                                                                              
 
```

### Создание БД и пользователей <!-- HEAD -->

#### Создание базы данных и пользователя <!-- NAME -->

```CODE
psql -U postgres                                                                         
  CREATE DATABASE db01;
  CREATE USER user01 WITH PASSWORD 'P@ssw0rd';                                                
  GRANT ALL PRIVILEGES ON DATABASE db01 TO user01;                                            
  \q                                                                                          
 
```

> db01 - имя создаваемой БД; user01 - имя пользователя

### Проверка <!-- HEAD -->

#### Проверка БД и пользователей на сервере <!-- NAME -->

```CODE
psql -U postgres                                                                         
  SELECT datname FROM pg_database;                                                            
  SELECT usename, usesuper, usecreatedb FROM pg_catalog.pg_user;                              
  \q                                                                                          
                                                                                              
 
```

#### Локальное подключение на клиенте <!-- NAME -->

```CODE
psql -U user01 db01                                                                      
                                                                                              
 
```

#### Удаленное подключение на клиенте <!-- NAME -->

```CODE
psql -U user01 -h IP_СЕРВЕРА -d db01
```
