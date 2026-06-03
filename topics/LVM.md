
### Основы LVM <!-- HEAD -->

> LVM(Logical Volume Manager) - система управления логическими томами

> Основа LVM: абстракция физических дисков для гибкого управления хранилищем

> Зачем LVM: изменение размера разделов без перезагрузки, создание снапшотов, объединение дисков, миграция данных

> Преимущества: динамическое изменение размера, перемещение данных между дисками, создание резервных копий на лету

> LVM vs mdadm: LVM для гибкого управления томами, mdadm для отказоустойчивости

> LVM может striping и mirroring, но mdadm лучше для RAID (производительность, надёжность)

> Часто используют вместе: mdadm для RAID массива, затем LVM поверх для управления томами

#### Компоненты LVM <!-- LIST -->
- Physical Volume (PV)
- физический том, диск или раздел
- Volume Group (VG)
- группа томов, объединяет несколько PV
- Logical Volume (LV)
- логический том, используется как обычный раздел
- Physical Extent (PE)
- минимальная единица данных для распределения

### Установка <!-- HEAD -->

#### Установка пакета LVM <!-- NAME -->

```CODE
apt-get install -y lvm2                                                                  
```

> lvm2(пакет для работы с LVM)

#### Создание разметки на дисках <!-- NAME -->

```CODE
parted /dev/sda                                                                          
mklabel gpt                                                                                 
mkpart primary 0% 100%
set 1 lvm on                                                                                
```

> set 1 lvm on(установка флага LVM на раздел)

#### Создание разметки на втором диске <!-- NAME -->

```CODE
parted /dev/sdb                                                                          
mklabel gpt                                                                                 
mkpart primary 0% 100%                                                                      
set 1 lvm on                                                                                

```

#### Создание Physical Volume <!-- NAME -->

```CODE
pvcreate /dev/sda1 /dev/sdb1                                                             
```

> pvcreate(инициализация физических томов для LVM)

#### Создание Volume Group <!-- NAME -->

```CODE
vgcreate vg01 /dev/sda1 /dev/sdb1                                                        
```

> vgcreate(создание группы томов) vg01(имя группы)

> Объединяет несколько физических томов в один пул

#### Создание Logical Volume <!-- NAME -->

```CODE
lvcreate -L 10G -n lv_data vg01                                                          
```

> lvcreate(создание логического тома) -L(размер) -n(имя тома)

> Альтернатива: -l 100%FREE(использовать всё свободное место)

#### Создание LV с использованием всего пространства <!-- NAME -->

```CODE
lvcreate -l 100%FREE -n lv_data vg01                                                     
```

> -l 100%FREE(использовать 100% свободного места в VG)

#### Создание файловой системы на LV <!-- NAME -->

```CODE
mkfs.ext4 /dev/vg01/lv_data                                                              
```

> Форматирование логического тома {ext4, xfs, btrfs}

#### Создание точки монтирования <!-- NAME -->

```CODE
mkdir /mnt/data                                                                          

```

#### Монтирование LV <!-- NAME -->

```CODE
mount /dev/vg01/lv_data /mnt/data                                                        

```

### Настройка striped (RAID 0) <!-- HEAD -->

> striped(чередование) - данные распределяются по дискам для увеличения скорости

> Требуется минимум 2 диска

#### Создание PV для striped <!-- NAME -->

```CODE
pvcreate /dev/sda1 /dev/sdb1                                                             

```

#### Создание VG для striped <!-- NAME -->

```CODE
vgcreate vg01 /dev/sda1 /dev/sdb1                                                        

```

#### Создание striped LV <!-- NAME -->

```CODE
lvcreate -l 100%FREE -n lv_data -i2 vg01                                                 
```

> -i2(количество дисков для striping, страйпинг по 2 дискам)

> Увеличивает скорость чтения/записи, но нет отказоустойчивости

#### Создание файловой системы <!-- NAME -->

```CODE
mkfs.ext4 /dev/vg01/lv_data                                                              

```

#### Монтирование <!-- NAME -->

```CODE
mkdir /mnt/data                                                                          
mount /dev/vg01/lv_data /mnt/data                                                           

```

### Настройка mirroring (RAID 1) <!-- HEAD -->

> mirroring(зеркалирование) - данные дублируются на несколько дисков для отказоустойчивости

> Требуется минимум 2 диска

#### Создание PV для mirroring <!-- NAME -->

```CODE
pvcreate /dev/sda1 /dev/sdb1                                                             

```

#### Создание VG для mirroring <!-- NAME -->

```CODE
vgcreate vg01 /dev/sda1 /dev/sdb1                                                        

```

#### Создание mirrored LV <!-- NAME -->

```CODE
lvcreate -l 100%FREE -n lvmirror -m1 vg01                                                
```

> -m1(количество копий минус одна, одно зеркало = 2 копии)

> Обеспечивает отказоустойчивость, выдерживает отказ одного диска

#### Создание файловой системы <!-- NAME -->

```CODE
mkfs.ext4 /dev/vg01/lvmirror                                                             

```

#### Монтирование <!-- NAME -->

```CODE
mkdir /mnt/mirror                                                                        
mount /dev/vg01/lvmirror /mnt/mirror                                                        

```

### Управление LVM <!-- HEAD -->

#### Увеличение размера LV <!-- NAME -->

```CODE
lvextend -L +5G /dev/vg01/lv_data                                                        
```

> -L +5G(добавить 5GB к текущему размеру)

> Изменение размера без перезагрузки и размонтирования

#### Увеличение размера файловой системы <!-- NAME -->

```CODE
resize2fs /dev/vg01/lv_data                                                              
```

> resize2fs(для ext4); xfs_growfs(для xfs)

> Расширяет файловую систему на весь размер LV

#### Уменьшение размера LV <!-- NAME -->

```CODE
umount /mnt/data                                                                         
e2fsck -f /dev/vg01/lv_data                                                                 
resize2fs /dev/vg01/lv_data 5G                                                              
lvreduce -L 5G /dev/vg01/lv_data                                                            
mount /dev/vg01/lv_data /mnt/data                                                           
```

> Сначала уменьшить ФС, потом LV; требует размонтирования

#### Добавление диска в VG <!-- NAME -->

```CODE
pvcreate /dev/sdc1                                                                       
vgextend vg01 /dev/sdc1                                                                     
```

> vgextend(расширение группы томов новым диском)

#### Удаление диска из VG <!-- NAME -->

```CODE
pvmove /dev/sda1                                                                         
vgreduce vg01 /dev/sda1                                                                     
```

> pvmove(перемещение данных с диска); vgreduce(удаление диска из VG)

#### Создание снапшота LV <!-- NAME -->

```CODE
lvcreate -L 1G -s -n lv_data_snap /dev/vg01/lv_data                                      
```

> -s(создание снапшота); -L 1G(размер для хранения изменений)

> Снапшот для резервного копирования без остановки системы

#### Восстановление из снапшота <!-- NAME -->

```CODE
lvconvert --merge /dev/vg01/lv_data_snap                                                 
```

> Откат LV к состоянию снапшота; требует перезагрузки или размонтирования

#### Удаление снапшота <!-- NAME -->

```CODE
lvremove /dev/vg01/lv_data_snap                                                          

```

#### Удаление LV <!-- NAME -->

```CODE
umount /mnt/data                                                                         
lvremove /dev/vg01/lv_data                                                                  

```

#### Удаление VG <!-- NAME -->

```CODE
vgremove vg01                                                                            

```

#### Удаление PV <!-- NAME -->

```CODE
pvremove /dev/sda1                                                                       

```

### Автомонтирование <!-- HEAD -->

#### В /etc/fstab добавить строку <!-- NAME -->

```CODE
/dev/vg01/lv_data   /mnt/data   ext4   defaults   0 0                                    
```

> Автоматическое монтирование при загрузке

#### Применение изменений fstab без перезагрузки <!-- NAME -->

```CODE
mount -a                                                                                 
```

> mount -a(монтирует все из /etc/fstab, что ещё не смонтировано)

### Проверка <!-- HEAD -->

#### Просмотр Physical Volumes <!-- NAME -->

```CODE
pvdisplay                                                                                
pvs
```

> pvdisplay(детальная информация); pvs(краткая таблица)

#### Просмотр Volume Groups <!-- NAME -->

```CODE
vgdisplay                                                                                
vgs                                                                                         
```

> Показывает размер VG, свободное место, количество PV

#### Просмотр Logical Volumes <!-- NAME -->

```CODE
lvdisplay                                                                                
lvs                                                                                         
```

> Показывает размер LV, VG, состояние

#### Просмотр всех компонентов LVM <!-- NAME -->

```CODE
lsblk                                                                                    
```

> Показывает иерархию дисков, разделов и LVM томов

#### Проверка монтирования <!-- NAME -->

```CODE
df -h                                                                                    
```

> Показывает смонтированные файловые системы и использование

#### Проверка автомонтирования после перезагрузки <!-- NAME -->

```CODE
reboot                                                                                   
df -h                                                                                       
```

> Опционально, только для проверки автомонтирования после перезагрузки

> Вместо перезагрузки можно использовать mount -a

#### Проверка состояния mirrored LV <!-- NAME -->

```CODE
lvs -a -o +devices                                                                       
```

> Показывает устройства и состояние зеркал

#### Проверка снапшотов <!-- NAME -->

```CODE
lvs -a -o +snap_percent                                                                  
```

> Показывает процент использования снапшота
