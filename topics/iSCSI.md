
### Установка <!-- HEAD -->

#### Установка пакета scsitarget-utils <!-- NAME -->

```CODE
apt-get update && apt-get install -y scsitarget-utils               
```

#### Включение службы tgt <!-- NAME -->

```CODE
systemctl enable --now tgt                                          
```

#### Просмотр списка блочных устройств <!-- NAME -->

```CODE
lsblk                                                               
```

> Определить диск для использования (в примере sda)

### Настройка <!-- HEAD -->

#### В /etc/tgt/targets.conf добавить в конец файла <!-- NAME -->

```CODE
<target iqn.2026-05.ru.example:storage.disk1>                       
backing-store /dev/sda                                             
initiator-address 192.168.20.0/24                                  
</target>                                                              
```

> iqn.2026-05.ru.example:storage.disk1 - уникальный идентификатор target; backing-store - путь к диску; initiator-address - разрешенная подсеть клиентов

#### Перезапуск службы tgt <!-- NAME -->

```CODE
systemctl restart tgt                                               

```

### Проверка <!-- HEAD -->

#### Проверка target-ов <!-- NAME -->

```CODE
tgtadm --lld iscsi --op show --mode target                          
```

> Показывает список доступных target-ов и их параметры

### Настройка LVM <!-- HEAD -->

#### В /etc/lvm/lvm.conf в блоке devices <!-- NAME -->

```CODE
filter = [ "r|/dev/sd.*|" ]                                         
```

> Исключает iSCSI-диски из сканирования LVM

### Установка на клиенте <!-- HEAD -->

#### Установка пакета open-iscsi <!-- NAME -->

```CODE
apt-get update && apt-get install -y open-iscsi                     
```

#### Включение службы iscsid <!-- NAME -->

```CODE
systemctl enable --now iscsid                                       

```

### Настройка на клиенте <!-- HEAD -->

#### Поиск доступных target-ов <!-- NAME -->

```CODE
iscsiadm -m discovery -t sendtargets -p 192.168.20.2                
```

> 192.168.20.2 - IP-адрес сервера iSCSI

#### Подключение target-ов <!-- NAME -->

```CODE
iscsiadm -m node --login                                            
```

#### В /etc/iscsi/iscsid.conf <!-- NAME -->

```CODE
node.startup = automatic                                            
```

> Закомментировать node.startup = manual, раскомментировать node.startup = automatic

#### В /var/lib/iscsi/send_targets/<TargetServer>,<Port>/st_config <!-- NAME -->

```CODE
discovery.sendtargets.use_discoveryd = Yes                          
```

> Изменить с No на Yes

#### Перезагрузка системы <!-- NAME -->

```CODE
reboot                                                              

```

### Проверка на клиенте <!-- HEAD -->

#### Проверка подключенного диска <!-- NAME -->

```CODE
lsblk                                                               
```

> Должен появиться новый блочный диск (в примере 5 ГБ)
