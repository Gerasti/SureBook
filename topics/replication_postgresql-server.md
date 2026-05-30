
### Установка PostgreSQL на резервном сервере <!-- HEAD -->

#### На SRV-BR установка пакетов <!-- NAME -->

```CODE
apt-get install -y postgresql16 postgresql16-server postgresql16-contrib                 
 
```

> SRV-BR(резервный сервер); SRV-HQ(основной сервер)

### Настройка основного сервера <!-- HEAD -->

#### На SRV-HQ в /var/lib/pgsql/data/postgresql.conf <!-- NAME -->

```CODE
wal_level = replica                                                                      
  max_wal_senders = 2                                                                         
  max_replication_slots = 2                                                                   
  hot_standby = on                                                                            
  hot_standby_feedback = on                                                                   
 
```

> wal_level(уровень журналирования); max_wal_senders(количество процессов репликации); hot_standby(чтение на реплике)

#### Перезапуск службы на SRV-HQ <!-- NAME -->

```CODE
systemctl restart postgresql
                                                                                              
 
```

### Настройка репликации на резервном сервере <!-- HEAD -->

#### На SRV-BR остановка службы <!-- NAME -->

```CODE
systemctl stop postgresql                                                                
                                                                                              
 
```

#### Очистка директории данных <!-- NAME -->

```CODE
rm -rf /var/lib/pgsql/data/*                                                             
 
```

> удаляет существующие данные для создания реплики

#### Создание базовой копии с SRV-HQ <!-- NAME -->

```CODE
pg_basebackup -h 192.168.11.67 -U postgres -D /var/lib/pgsql/data --wal-method=stream    
  --write-recovery-conf                                                                       
 
```

> -h(IP основного сервера); -U(пользователь); -D(директория данных); --wal-method(метод передачи WAL); --write-recovery-conf(создание конфига репликации)

#### Установка прав доступа <!-- NAME -->

```CODE
chown -R postgres:postgres /var/lib/pgsql/data/
                                                                                              
 
```

#### Запуск службы на SRV-BR <!-- NAME -->

```CODE
systemctl start postgresql                                                               
                                                                                              
 
```

### Проверка репликации <!-- HEAD -->

#### Подключение к базе данных <!-- NAME -->

```CODE
psql -U postgres                                                                         
 
```

> подключение к PostgreSQL

#### Проверка статуса репликации на SRV-HQ <!-- NAME -->

```CODE
SELECT * FROM pg_stat_replication;                                                       
 
```

> показывает подключенные реплики

#### Проверка данных на SRV-BR <!-- NAME -->

```CODE
\c one                                                                                   
  \dt+                                                                                        
 
```

> \c(подключение к БД); \dt+(список таблиц с размерами)
