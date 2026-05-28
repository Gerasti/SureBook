
### Установка <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install -y MySQL-server                                                          
   
 
```

#### Включение и запуск службы <!-- NAME -->

```CODE
systemctl enable --now mysqld

 
```

### Настройка MySQL <!-- HEAD -->

#### Установка пароля root <!-- NAME -->

```CODE
mysql -u root
  ALTER USER 'root'@'localhost' IDENTIFIED BY 'P@ssw0rd';
  EXIT;

 
```

#### Разрешение доступа из сети в /etc/my.cnf.d/server.cnf <!-- NAME -->

```CODE
sed -i "s/skip-networking/#skip-networking/g" /etc/my.cnf.d/server.cnf
                                                                                              
 
```

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart mysqld                                                                 
                                                                                              
 
```

#### Разрешение доступа для root по сети <!-- NAME -->

```CODE
mysql -u root -p                                                                         
  GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';                                          
  UPDATE mysql.user SET host='%' WHERE user='root';                                           
  FLUSH PRIVILEGES;                                                                           
  EXIT;                                                                                       
 
```

> host='%' разрешает подключение с любого узла

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart mysqld                                                                 
                                                                                              
 
```

### Проверка MySQL <!-- HEAD -->

#### Проверка пользователей на сервере <!-- NAME -->

```CODE
mysql -u root -p                                                                         
  SELECT user, HOST FROM mysql.user;                                                          
  EXIT;                                                                                       
                                                                                              
 
```

#### Удаленное подключение с клиента <!-- NAME -->

```CODE
mysql -h IP_СЕРВЕРА -u root -p                                                           
                                                                                              
 
```

### Создание БД и пользователей <!-- HEAD -->

#### Создание базы данных <!-- NAME -->

```CODE
mysql -u root -p                                                                         
  CREATE DATABASE db01;                                                                       
 
```

> db01 - имя создаваемой БД

#### Создание пользователя <!-- NAME -->

```CODE
CREATE USER 'user01'@'%' IDENTIFIED BY 'P@ssw0rd';                                       
 
```

> '%' означает подключение с любого хоста

#### Предоставление прав пользователю <!-- NAME -->

```CODE
GRANT ALL PRIVILEGES ON db01.* TO 'user01'@'%';                                          
  FLUSH PRIVILEGES;                                                                           
                                                                                              
 
```

#### Проверка существования БД и пользователей <!-- NAME -->

```CODE
SHOW DATABASES;                                                                          
  SELECT user, HOST FROM mysql.user;                                                          
  EXIT;          
```
