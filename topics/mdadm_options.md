
### Основные уровни RAID <!-- HEAD -->

#### Сравнение уровней RAID <!-- NAME -->

> RAID 0(striping, высокая скорость, нет отказоустойчивости, минимум 2 диска, объём = сумма дисков); RAID 1(mirroring, отказ 1 диска, минимум 2 диска, объём = размер 1 диска); RAID 5(striping+parity, отказ 1 диска, минимум 3 диска, объём = (N-1)×диск); RAID 6(double parity, отказ 2 диска, минимум 4 диска, объём = (N-2)×диск); RAID 10(mirror+stripe, высокая отказоустойчивость, минимум 4 диска, объём = 50%)

> Программный RAID(реализован на уровне ОС, использует CPU) vs Аппаратный RAID(реализован контроллером, имеет собственный процессор)

### Установка mdadm <!-- HEAD -->

#### Установка утилиты mdadm <!-- NAME -->

```CODE
apt-get install -y mdadm                                                                 
```

> mdadm(Multiple Device Administration, утилита для управления программными RAID-массивами в Linux); -y(автоматическое подтверждение установки)

### Создание RAID массивов <!-- HEAD -->

#### Создание RAID 0 массива <!-- NAME -->

```CODE
mdadm --create --verbose /dev/md0 --level=0 --raid-devices=2 /dev/sdb /dev/sdc           
```

> --create(создать новый массив); --verbose(подробный вывод); /dev/md0(имя создаваемого RAID-устройства); --level(уровень RAID: {0, 1, 4, 5, 6, 10}); --raid-devices(количество активных дисков в массиве); /dev/sdb /dev/sdc(список физических дисков)

#### Создание RAID 1 массива <!-- NAME -->

```CODE
mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 /dev/sdb /dev/sdc

```

#### Создание RAID 4 массива <!-- NAME -->

```CODE
mdadm --create --verbose /dev/md0 --level=4 --raid-devices=3 /dev/sdb /dev/sdc /dev/sdd
```

> RAID 2(bit-level striping with Hamming code) и RAID 3(byte-level striping) устарели и не поддерживаются mdadm

#### Создание RAID 5 массива <!-- NAME -->

```CODE
mdadm --create --verbose /dev/md0 --level=5 --raid-devices=3 /dev/sdb /dev/sdc /dev/sdd

```

#### Создание RAID 6 массива <!-- NAME -->

```CODE
mdadm --create --verbose /dev/md0 --level=6 --raid-devices=4 /dev/sdb /dev/sdc /dev/sdd
/dev/sde                                                                                    

```

#### Создание RAID 10 массива <!-- NAME -->

```CODE
mdadm --create --verbose /dev/md0 --level=10 --raid-devices=4 /dev/sdb /dev/sdc /dev/sdd
/dev/sde                                                                                    

```

#### Создание массива с spare диском <!-- NAME -->

```CODE
mdadm --create --verbose /dev/md0 --level=5 --raid-devices=3 --spare-devices=1 /dev/sdb
/dev/sdc /dev/sdd /dev/sde                                                                  
```

> --spare-devices(количество резервных дисков); spare(горячий резерв) - диск автоматически заменит отказавший и начнёт процесс rebuild

### Настройка массива <!-- HEAD -->

#### Создание файловой системы на массиве <!-- NAME -->

```CODE
mkfs.ext4 /dev/md0                                                                       
```

> mkfs(make filesystem, создание файловой системы); форматы: {ext4, xfs, btrfs}

#### Создание точки монтирования <!-- NAME -->

```CODE
mkdir /mnt/raid                                                                          

```

#### Монтирование массива <!-- NAME -->

```CODE
mount /dev/md0 /mnt/raid                                                                 

```

#### Добавление в /etc/fstab для автомонтирования <!-- NAME -->

```CODE
/dev/md0   /mnt/raid   ext4   defaults   0 0                                             
```

> /dev/md0(устройство); /mnt/raid(точка монтирования); ext4(тип ФС); defaults(опции по умолчанию: rw,suid,dev,exec,auto,nouser,async); первый 0(dump, не создавать резервные копии); второй 0(fsck, не проверять ФС при загрузке)

### Настройка mdadm.conf <!-- HEAD -->

#### Сохранение конфигурации массива <!-- NAME -->

```CODE
mdadm --detail --scan >> /etc/mdadm.conf                                                 
```

> --detail(детальная информация о массиве); --scan(сканировать все массивы); >>(добавить в конец файла); создаёт строку ARRAY с UUID, уровнем и метаданными массива

#### Пример строки ARRAY в mdadm.conf <!-- NAME -->

```CODE
ARRAY /dev/md0 metadata=1.2 name=hostname:0 UUID=12345678:abcdefgh:12345678:abcdefgh     
```

> ARRAY(определение массива); /dev/md0(имя устройства); metadata(версия метаданных: {0.90, 1.0, 1.1, 1.2}); name(имя массива hostname:номер); UUID(уникальный идентификатор массива)

#### Добавление параметров устройств в mdadm.conf <!-- NAME -->

```CODE
DEVICE /dev/sdb /dev/sdc /dev/sdd /dev/sde
```

> DEVICE(список физических дисков для поиска массивов); можно использовать wildcards: /dev/sd*

#### Настройка email-уведомлений в mdadm.conf <!-- NAME -->

```CODE
MAILADDR admin@example.com
MAILFROM mdadm@server.local                                                                 
```

> MAILADDR(адрес для отправки уведомлений о проблемах с массивом); MAILFROM(адрес отправителя)

#### Настройка программы мониторинга в mdadm.conf <!-- NAME -->

```CODE
PROGRAM /usr/local/bin/raid-notify.sh
```

> PROGRAM(скрипт, который будет выполнен при событии с массивом); получает параметры: событие и устройство

#### Ручное редактирование mdadm.conf <!-- NAME -->

```CODE
nano /etc/mdadm.conf
```

> Файл можно редактировать вручную для тонкой настройки параметров

#### Применение изменений из mdadm.conf <!-- NAME -->

```CODE
mdadm --assemble --scan                                                                  
```

> --assemble(собрать массивы); --scan(использовать конфигурацию из /etc/mdadm.conf)

#### Обновление конфигурации после изменения массива <!-- NAME -->

```CODE
mdadm --detail --scan > /etc/mdadm.conf.new                                              
mv /etc/mdadm.conf.new /etc/mdadm.conf                                                      
```

> Перезапись файла с актуальной конфигурацией всех массивов

#### Резервное копирование mdadm.conf <!-- NAME -->

```CODE
cp /etc/mdadm.conf /etc/mdadm.conf.backup                                                
```

> Сохранение копии перед внесением изменений

#### Добавление spare диска в существующий массив <!-- NAME -->

```CODE
mdadm --add /dev/md0 /dev/sde                                                            
```

> --add(добавить диск в массив как горячий резерв)

### Управление массивом <!-- HEAD -->

#### Остановка массива <!-- NAME -->

```CODE
mdadm --stop /dev/md0                                                                    
```

> --stop(остановить массив); необходимо размонтировать перед остановкой

#### Запуск массива <!-- NAME -->

```CODE
mdadm --assemble /dev/md0 /dev/sdb /dev/sdc /dev/sdd                                     
```

> --assemble(собрать массив из указанных дисков)

#### Автоматическая сборка всех массивов из mdadm.conf <!-- NAME -->

```CODE
mdadm --assemble --scan
```

> Собирает все массивы, описанные в /etc/mdadm.conf

#### Пометка диска как отказавшего <!-- NAME -->

```CODE
mdadm --fail /dev/md0 /dev/sdc                                                           
```

> --fail(пометить диск как failed); для имитации отказа при тестировании

#### Удаление диска из массива <!-- NAME -->

```CODE
mdadm --remove /dev/md0 /dev/sdc                                                         
```

> --remove(удалить диск из массива); диск должен быть помечен как failed

#### Добавление нового диска взамен отказавшего <!-- NAME -->

```CODE
mdadm --add /dev/md0 /dev/sde                                                            
```

> Автоматически начнётся процесс rebuild (восстановление данных на новом диске)

#### Увеличение количества дисков в массиве <!-- NAME -->

```CODE
mdadm --grow /dev/md0 --raid-devices=4 --add /dev/sde                                    
```

> --grow(изменить параметры массива); расширение с пересчётом данных

#### Изменение уровня RAID <!-- NAME -->

```CODE
mdadm --grow /dev/md0 --level=6                                                          
```

> Преобразование массива (например RAID 5 в RAID 6), требует времени на пересчёт

### Проверка состояния <!-- HEAD -->

#### Проверка состояния всех RAID массивов <!-- NAME -->

```CODE
cat /proc/mdstat                                                                         
```

> Краткая информация: состояние, прогресс rebuild/resync, активные/отказавшие диски

#### Детальная информация о массиве <!-- NAME -->

```CODE
mdadm --detail /dev/md0                                                                  
```

> Показывает уровень RAID, состояние дисков, размер, UUID

#### Проверка информации о диске в массиве <!-- NAME -->

```CODE
mdadm --examine /dev/sdb                                                                 
```

> --examine(прочитать метаданные RAID на диске); показывает UUID массива, уровень RAID, роль диска

#### Мониторинг состояния массива <!-- NAME -->

```CODE
mdadm --monitor --scan --daemonise
```

> --monitor(режим мониторинга); --daemonise(запустить как демон); отправляет уведомления об ошибках

#### Проверка скорости rebuild <!-- NAME -->

```CODE
cat /proc/sys/dev/raid/speed_limit_min
cat /proc/sys/dev/raid/speed_limit_max                                                      
```

> Показывает минимальную и максимальную скорость восстановления в KB/s

#### Изменение скорости rebuild <!-- NAME -->

```CODE
echo 50000 > /proc/sys/dev/raid/speed_limit_min                                          
echo 200000 > /proc/sys/dev/raid/speed_limit_max                                            
```

> Значения в KB/s; низкая скорость снижает нагрузку, высокая ускоряет восстановление

#### Проверка целостности массива <!-- NAME -->

```CODE
echo check > /sys/block/md0/md/sync_action                                               
```

> Запуск проверки целостности без исправления ошибок

#### Восстановление с исправлением ошибок <!-- NAME -->

```CODE
echo repair > /sys/block/md0/md/sync_action                                              
```

> Проверка и автоматическое исправление несоответствий в данных

#### Просмотр прогресса проверки <!-- NAME -->

```CODE
cat /proc/mdstat                                                                         
```

> Показывает прогресс операций check/repair/rebuild в процентах

### Удаление массива <!-- HEAD -->

#### Размонтирование массива <!-- NAME -->

```CODE
umount /mnt/raid                                                                         

```

#### Остановка массива <!-- NAME -->

```CODE
mdadm --stop /dev/md0                                                                    

```

#### Удаление метаданных RAID с дисков <!-- NAME -->

```CODE
mdadm --zero-superblock /dev/sdb /dev/sdc /dev/sdd                                       
```

> --zero-superblock(обнулить суперблок RAID); полное удаление информации о RAID с дисков

#### Удаление записи из /etc/fstab <!-- NAME -->

```CODE
sed -i '/\/dev\/md0/d' /etc/fstab                                                        
```

> sed -i(редактировать файл на месте); /d(удалить строку)

#### Удаление записи из /etc/mdadm.conf <!-- NAME -->

```CODE
sed -i '/\/dev\/md0/d' /etc/mdadm.conf                                                   
```

> Удаление конфигурации массива из файла
