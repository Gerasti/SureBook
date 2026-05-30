
### Настройка службы резервного копирования <!-- HEAD -->

#### Создание директории для резервных копий <!-- NAME -->

```CODE
mkdir -p /var/backup
                                                                                              
 
```

#### Создание службы /etc/systemd/system/backup.service <!-- NAME -->

```CODE
[Unit]                                                                                   
  Description=Backup shared folder to /var/backup                                             
  After=network.target                                                                        
                                                                                              
  [Service]                                                                                   
  Type=oneshot                                                                                
  ExecStart=/bin/bash -c 'tar -czf /var/backup/shared-$(date +%%Y-%%m-%%d-%%H-%%M-%%S).tar.gz 
  /path/to/shared/folder'                                                                     
 
```

> Type=oneshot(служба завершается после выполнения команды); ExecStart(команда создания архива с датой и временем); %%(двойной процент для экранирования в systemd)

#### Создание таймера /etc/systemd/system/backup.timer <!-- NAME -->

```CODE
[Unit]       
  Description=Run backup.service daily at 20:00                                               
                                                                                              
  [Timer]                                                                                     
  OnCalendar=20:00                                                                            
  Persistent=true                                                                             
                                                                                              
  [Install]                                                                                   
  WantedBy=timers.target                                                                      
 
```

> OnCalendar=20:00(запуск каждый день в 20:00); Persistent=true(выполнить пропущенную задачу при загрузке, если система была выключена)

### Запуск <!-- HEAD -->

#### Перезагрузка конфигурации systemd <!-- NAME -->

```CODE
systemctl daemon-reload
 
```

> Применяет изменения после создания или редактирования unit-файлов

#### Включение и запуск таймера <!-- NAME -->

```CODE
systemctl enable --now backup.timer                                                      
                                                                                              
 
```

### Проверка <!-- HEAD -->

#### Просмотр активных таймеров <!-- NAME -->

```CODE
systemctl list-timers
 
```

> Показывает все таймеры, время следующего запуска и последнего выполнения

#### Проверка статуса таймера <!-- NAME -->

```CODE
systemctl status backup.timer                                                            
                                                                                              
 
```

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status backup.service                                                          
                                                                                              
 
```

#### Ручной запуск службы резервного копирования <!-- NAME -->

```CODE
systemctl start backup.service                                                           
 
```

> Для проверки работы службы без ожидания таймера

#### Просмотр созданных архивов <!-- NAME -->

```CODE
ls -lh /var/backup                                                                       
 
```

> -lh(список с размерами в читаемом формате)

#### Просмотр логов службы <!-- NAME -->

```CODE
journalctl -u backup.service                                                             
 
```

> Показывает логи выполнения резервного копирования

#### Просмотр логов таймера <!-- NAME -->

```CODE
journalctl -u backup.timer                                                               
                                                                                              
 
```

### Дополнительные варианты OnCalendar <!-- LIST -->
- OnCalendar=daily (каждый день в 00:00)
- OnCalendar=weekly (каждую неделю в понедельник 00:00)
- OnCalendar=--* 02:00:00 (каждый день в 02:00)
- OnCalendar=Mon,Fri 18:00 (понедельник и пятница в 18:00)
- OnCalendar=*:0/15 (каждые 15 минут)
- OnCalendar=hourly (каждый час)
