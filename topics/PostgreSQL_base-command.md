
### Подключение к PostgreSQL <!-- HEAD -->

#### Подключение к БД от имени пользователя postgres <!-- NAME -->

```CODE
psql -U postgres                                                                         
 
```

> -U(имя пользователя)

#### Подключение к конкретной базе данных <!-- NAME -->

```CODE
psql -U user01 -d db01                                                                   
 
```

> -d(имя базы данных)

#### Удалённое подключение к БД <!-- NAME -->

```CODE
psql -U user01 -h 192.168.1.10 -d db01                                                   
 
```

> -h(IP-адрес или hostname сервера)

#### Подключение с указанием порта <!-- NAME -->

```CODE
psql -U user01 -h 192.168.1.10 -p 5432 -d db01                                           
 
```

> -p(порт) по умолчанию 5432

#### Выход из psql <!-- NAME -->

```CODE
\q                                                                                       
                                                                                              
 
```

### Управление базами данных <!-- HEAD -->

#### Создание базы данных <!-- NAME -->

```CODE
CREATE DATABASE mydb;                                                                    
 
```

> mydb(имя создаваемой БД)

#### Создание БД с указанием владельца и кодировки <!-- NAME -->

```CODE
CREATE DATABASE mydb OWNER myuser ENCODING 'UTF8';                                       
 
```

> OWNER(владелец БД); ENCODING(кодировка) {UTF8, LATIN1}

#### Удаление базы данных <!-- NAME -->

```CODE
DROP DATABASE mydb;                                                                      
 
```

> Удаляет БД безвозвратно

#### Переименование базы данных <!-- NAME -->

```CODE
ALTER DATABASE mydb RENAME TO newdb;                                                     
                                                                                              
 
```

#### Просмотр списка баз данных <!-- NAME -->

```CODE
\l                                                                                       
 
```

> Показывает все БД с владельцами и кодировками

#### Просмотр списка БД через SQL <!-- NAME -->

```CODE
SELECT datname FROM pg_database;                                                         
                                                                                              
 
```

#### Подключение к другой БД внутри psql <!-- NAME -->

```CODE
\c dbname                                                                                
 
```

> Переключение между базами данных

#### Просмотр размера базы данных <!-- NAME -->

```CODE
SELECT pg_size_pretty(pg_database_size('mydb'));                                         
                                                                                              
 
```

### Управление пользователями <!-- HEAD -->

#### Создание пользователя <!-- NAME -->

```CODE
CREATE USER username WITH PASSWORD 'P@ssw0rd';                                           
 
```

> username(имя пользователя)

#### Создание пользователя с правами суперпользователя <!-- NAME -->

```CODE
CREATE USER admin WITH SUPERUSER PASSWORD 'P@ssw0rd';                                    
 
```

> SUPERUSER(полные права на сервер)

#### Создание пользователя с правами создания БД <!-- NAME -->

```CODE
CREATE USER dbcreator WITH CREATEDB PASSWORD 'P@ssw0rd';                                 
 
```

> CREATEDB(право создавать базы данных)

#### Изменение пароля пользователя <!-- NAME -->

```CODE
ALTER USER username WITH PASSWORD 'NewP@ssw0rd';                                         
                                                                                              
 
```

#### Удаление пользователя <!-- NAME -->

```CODE
DROP USER username;                                                                      
                                                                                              
 
```

#### Просмотр списка пользователей <!-- NAME -->

```CODE
\du                                                                                      
 
```

> Показывает пользователей с их ролями

#### Просмотр списка пользователей через SQL <!-- NAME -->

```CODE
SELECT usename, usesuper, usecreatedb FROM pg_catalog.pg_user;                           
                                                                                              
 
```

#### Переименование пользователя <!-- NAME -->

```CODE
ALTER USER oldname RENAME TO newname;                                                    
                                                                                              
 
```

### Управление правами доступа <!-- HEAD -->

#### Предоставление всех прав на БД пользователю <!-- NAME -->

```CODE
GRANT ALL PRIVILEGES ON DATABASE mydb TO username;                                       
 
```

> ALL PRIVILEGES(все права на БД)

#### Предоставление прав на подключение к БД <!-- NAME -->

```CODE
GRANT CONNECT ON DATABASE mydb TO username;                                              
 
```

> CONNECT(право подключаться к БД)

#### Предоставление прав на схему <!-- NAME -->

```CODE
GRANT ALL ON SCHEMA public TO username;                                                  
 
```

> public(схема по умолчанию)

#### Предоставление прав на все таблицы в схеме <!-- NAME -->

```CODE
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO username;                         
                                                                                              
 
```

#### Предоставление прав на конкретную таблицу <!-- NAME -->

```CODE
GRANT SELECT, INSERT, UPDATE, DELETE ON tablename TO username;                           
 
```

> SELECT, INSERT, UPDATE, DELETE(типы операций)

#### Отзыв прав у пользователя <!-- NAME -->

```CODE
REVOKE ALL PRIVILEGES ON DATABASE mydb FROM username;                                    
                                                                                              
 
```

#### Изменение владельца базы данных <!-- NAME -->

```CODE
ALTER DATABASE mydb OWNER TO newowner;                                                   
                                                                                              
 
```

#### Изменение владельца таблицы <!-- NAME -->

```CODE
ALTER TABLE tablename OWNER TO newowner;                                                 
                                                                                              
 
```

### Управление таблицами <!-- HEAD -->

#### Просмотр списка таблиц <!-- NAME -->

```CODE
\dt                                                                                      
 
```

> Показывает таблицы в текущей БД

#### Просмотр списка таблиц с размерами <!-- NAME -->

```CODE
\dt+                                                                                     
 
```

> Показывает таблицы с размерами и описанием

#### Просмотр структуры таблицы <!-- NAME -->

```CODE
\d tablename                                                                             
 
```

> Показывает столбцы, типы данных, индексы

#### Создание таблицы <!-- NAME -->

```CODE
CREATE TABLE users (                                                                     
      id SERIAL PRIMARY KEY,                                                                  
      username VARCHAR(50) NOT NULL,                                                          
      email VARCHAR(100) UNIQUE,                                                              
      created_at TIMESTAMP DEFAULT NOW()                                                      
  );                                                                                          
 
```

> SERIAL(автоинкремент); PRIMARY KEY(первичный ключ); NOT NULL(обязательное поле); UNIQUE(уникальное значение)

#### Удаление таблицы <!-- NAME -->

```CODE
DROP TABLE tablename;
                                                                                              
 
```

#### Переименование таблицы <!-- NAME -->

```CODE
ALTER TABLE oldname RENAME TO newname;                                                   
                                                                                              
 
```

#### Добавление столбца в таблицу <!-- NAME -->

```CODE
ALTER TABLE tablename ADD COLUMN columnname VARCHAR(50);                                 
                                                                                              
 
```

#### Удаление столбца из таблицы <!-- NAME -->

```CODE
ALTER TABLE tablename DROP COLUMN columnname;                                            
                                                                                              
 
```

#### Изменение типа данных столбца <!-- NAME -->

```CODE
ALTER TABLE tablename ALTER COLUMN columnname TYPE INTEGER;                              
                                                                                              
 
```

#### Очистка таблицы <!-- NAME -->

```CODE
TRUNCATE TABLE tablename;                                                                
 
```

> Удаляет все строки, но сохраняет структуру

### Работа с данными <!-- HEAD -->

#### Вставка данных в таблицу <!-- NAME -->

```CODE
INSERT INTO users (username, email) VALUES ('john', 'john@example.com');                 
                                                                                              
 
```

#### Вставка нескольких строк <!-- NAME -->

```CODE
INSERT INTO users (username, email) VALUES                                               
  ('alice', 'alice@example.com'),                                                             
  ('bob', 'bob@example.com');                                                                 
                                                                                              
 
```

#### Выборка всех данных из таблицы <!-- NAME -->

```CODE
SELECT * FROM users;                                                                     
                                                                                              
 
```

#### Выборка конкретных столбцов <!-- NAME -->

```CODE
SELECT username, email FROM users;                                                       
                                                                                              
 
```

#### Выборка с условием <!-- NAME -->

```CODE
SELECT * FROM users WHERE id = 1;                                                        
 
```

> WHERE(условие фильтрации)

#### Выборка с сортировкой <!-- NAME -->

```CODE
SELECT * FROM users ORDER BY created_at DESC;                                            
 
```

> ORDER BY(сортировка); DESC(по убыванию) {ASC, DESC}

#### Выборка с ограничением количества строк <!-- NAME -->

```CODE
SELECT * FROM users LIMIT 10;                                                            
 
```

> LIMIT(ограничение количества строк)

#### Обновление данных <!-- NAME -->

```CODE
UPDATE users SET email = 'newemail@example.com' WHERE id = 1;                            
                                                                                              
 
```

#### Удаление данных <!-- NAME -->

```CODE
DELETE FROM users WHERE id = 1;                                                          
                                                                                              
 
```

#### Подсчёт количества строк <!-- NAME -->

```CODE
SELECT COUNT(*) FROM users;                                                              
                                                                                              
 
```

### Резервное копирование и восстановление <!-- HEAD -->

#### Создание резервной копии БД <!-- NAME -->

```CODE
pg_dump -U postgres -d mydb -f backup.sql                                                
 
```

> -f(файл для сохранения резервной копии)

#### Создание резервной копии в сжатом формате <!-- NAME -->

```CODE
pg_dump -U postgres -d mydb -F c -f backup.dump                                          
 
```

> -F c(custom format, сжатый формат)

#### Создание резервной копии всех БД <!-- NAME -->

```CODE
pg_dumpall -U postgres -f all_databases.sql                                              
 
```

> pg_dumpall(резервное копирование всех БД и пользователей)

#### Восстановление БД из SQL файла <!-- NAME -->

```CODE
psql -U postgres -d mydb -f backup.sql                                                   
 
```

> Восстановление из текстового SQL файла

#### Восстановление БД из сжатого формата <!-- NAME -->

```CODE
pg_restore -U postgres -d mydb backup.dump                                               
 
```

> pg_restore(восстановление из custom format)

#### Восстановление с созданием новой БД <!-- NAME -->

```CODE
pg_restore -U postgres -C -d postgres backup.dump                                        
 
```

> -C(создать БД перед восстановлением)

### Информационные команды psql <!-- HEAD -->

#### Список всех команд psql <!-- NAME -->

```CODE
\?                                                                                       
 
```

> Показывает все доступные команды psql

#### Список SQL команд <!-- NAME -->

```CODE
\h                                                                                       
 
```

> Показывает справку по SQL командам

#### Справка по конкретной SQL команде <!-- NAME -->

```CODE
\h CREATE TABLE                                                                          
 
```

> Показывает синтаксис команды CREATE TABLE

#### Просмотр текущей БД и пользователя <!-- NAME -->

```CODE
\conninfo                                                                                
 
```

> Показывает информацию о текущем подключении

#### Просмотр всех схем <!-- NAME -->

```CODE
\dn                                                                                      
 
```

> Показывает список схем в текущей БД

#### Просмотр всех представлений <!-- NAME -->

```CODE
\dv                                                                                      
 
```

> Показывает список представлений (views)

#### Просмотр всех индексов <!-- NAME -->

```CODE
\di                                                                                      
 
```

> Показывает список индексов

#### Просмотр всех последовательностей <!-- NAME -->

```CODE
\ds                                                                                      
 
```

> Показывает список sequences

#### Включение расширенного вывода <!-- NAME -->

```CODE
\x                                                                                       
 
```

> Переключает между обычным и расширенным форматом вывода

#### Выполнение команд из файла <!-- NAME -->

```CODE
\i /path/to/file.sql                                                                     
 
```

> Выполняет SQL команды из файла

#### Вывод результата запроса в файл <!-- NAME -->

```CODE
\o /path/to/output.txt                                                                   
  SELECT * FROM users;                                                                        
  \o                                                                                          
 
```

> \o(перенаправление вывода в файл); \o без параметра(отключение перенаправления)

#### Измерение времени выполнения запросов <!-- NAME -->

```CODE
\timing                                                                                  
 
```

> Включает/выключает отображение времени выполнения

### Управление индексами <!-- HEAD -->

#### Создание индекса <!-- NAME -->

```CODE
CREATE INDEX idx_username ON users(username);                                            
 
```

> idx_username(имя индекса); users(таблица); username(столбец)

#### Создание уникального индекса <!-- NAME -->

```CODE
CREATE UNIQUE INDEX idx_email ON users(email);                                           
 
```

> UNIQUE(индекс с уникальными значениями)

#### Удаление индекса <!-- NAME -->

```CODE
DROP INDEX idx_username;                                                                 
                                                                                              
 
```

#### Просмотр индексов таблицы <!-- NAME -->

```CODE
\d tablename                                                                             
 
```

> Показывает индексы в описании таблицы

### Управление транзакциями <!-- HEAD -->

#### Начало транзакции <!-- NAME -->

```CODE
BEGIN;                                                                                   
                                                                                              
 
```

#### Фиксация транзакции <!-- NAME -->

```CODE
COMMIT;                                                                                  
                                                                                              
 
```

#### Откат транзакции <!-- NAME -->

```CODE
ROLLBACK;
                                                                                              
 
```

#### Пример использования транзакции <!-- NAME -->

```CODE
BEGIN;                                                                                   
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;                                   
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;                                   
  COMMIT;                                                                                     
 
```

> Транзакция для атомарного выполнения нескольких операций

### Проверка <!-- HEAD -->

#### Проверка версии PostgreSQL <!-- NAME -->

```CODE
SELECT version();                                                                        
                                                                                              
 
```

#### Проверка текущего времени на сервере <!-- NAME -->

```CODE
SELECT NOW();                                                                            
                                                                                              
 
```

#### Проверка активных подключений <!-- NAME -->

```CODE
SELECT * FROM pg_stat_activity;                                                          
 
```

> Показывает все активные подключения к серверу

#### Проверка размера всех БД <!-- NAME -->

```CODE
SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database;              
                                                                                              
 
```

#### Проверка размера всех таблиц в БД <!-- NAME -->

```CODE
SELECT tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))     
  FROM pg_tables WHERE schemaname = 'public'; 
```
