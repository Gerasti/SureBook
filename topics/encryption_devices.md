
### Шифрование раздела с LUKS <!-- HEAD -->

#### Создание ключа шифрования <!-- NAME -->

```CODE
dd if=/dev/urandom of=/root/ext4.key bs=1024 count=4                                     
 
```

> Генерация случайного ключа размером 4 КБ

#### Шифрование раздела с указанным ключом <!-- NAME -->

```CODE
cryptsetup luksFormat /dev/data_striped/lv_data /root/ext4.key                           
 
```

> Инициализация LUKS-шифрования на разделе

#### Открытие зашифрованного раздела <!-- NAME -->

```CODE
cryptsetup luksOpen /dev/data_striped/lv_data data_crypt --key-file /root/ext4.key       
 
```

> Открывает зашифрованный раздел как /dev/mapper/data_crypt

#### Форматирование раздела <!-- NAME -->

```CODE
mkfs.ext4 /dev/mapper/data_crypt                                                         
                                                                                              
 
```

### Автоматическая разблокировка при загрузке <!-- HEAD -->

#### Настройка автоматической разблокировки в /etc/crypttab <!-- NAME -->

```CODE
data_crypt /dev/data_striped/lv_data /root/ext4.key luks                                 
 
```

> Формат: имя устройство ключ тип

#### Проверка синтаксиса <!-- NAME -->

```CODE
systemctl daemon-reexec                                                                  
  systemctl restart systemd-cryptsetup@data_crypt                                             
                                                                                              
 
```

### Монтирование раздела <!-- HEAD -->

#### Настройка автомонтирования в /etc/fstab <!-- NAME -->

```CODE
/dev/mapper/data_crypt /opt/data ext4 defaults 0 2                                       
 
```

> Формат: устройство точка_монтирования файловая_система опции dump fsck

### Защита ключа шифрования <!-- HEAD -->

#### Установка прав доступа на ключ <!-- NAME -->

```CODE
chmod 600 /root/ext4.key                                                                 
  chown root:root /root/ext4.key                                                              
 
```

> Только root может читать и записывать ключ

### Применение настроек <!-- HEAD -->

#### Перезагрузка системы <!-- NAME -->

```CODE
reboot                                                                                   
                                                                                              
 
```

#### Проверка монтирования <!-- NAME -->

```CODE
df -h                                                                                    
 
```

> Проверка, что зашифрованный раздел смонтирован
