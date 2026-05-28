
### Установка <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install -y mariadb-server                                                        
   
 
```

#### Включение и запуск службы <!-- NAME -->

```CODE
systemctl enable --now mariadb

 
```

### Настройка MariaDB <!-- HEAD -->

#### Установка пароля root <!-- NAME -->

```CODE
mariadb -u root
  ALTER USER 'root'@'localhost' IDENTIFIED BY 'P@ssw0rd';
  EXIT;

 
```

#### Разрешение доступа из сети в /etc/my.cnf.d/server.cnf <!-- NAME -->

```CODE
sed -i "s/skip-networking/#skip-networking/g" /etc/my.cnf.d/server.cnf
                                                                                              
 
```

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart mariadb                                                                
                                                                                              
 
```

#### Разрешение доступа для root по сети <!-- NAME -->

```CODE
mariadb -u root -p                                                                       
  GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';                                          
  UPDATE mysql.user SET host='%' WHERE user='root';                                           
  FLUSH PRIVILEGES;                                                                           
  EXIT;                                                                                       
 
```

> host='%' разрешает подключение с любого узла

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart mariadb                                                                
                                                                                              
 
```

### Проверка MariaDB <!-- HEAD -->

#### Проверка пользователей на сервере <!-- NAME -->

```CODE
mariadb -u root -p                                                                       
  SELECT user, HOST FROM mysql.user;                                                          
  EXIT;                                                                                       
                                                                                              
 
```

#### Удаленное подключение с клиента <!-- NAME -->

```CODE
mariadb -h IP_СЕРВЕРА -u root -p
                                                                                              
 
```

### Создание БД и пользователей <!-- HEAD -->

#### Создание базы данных <!-- NAME -->

```CODE
mariadb -u root -p                                                                       
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
