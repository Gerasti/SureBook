
#### Создание GPT разметки на диске /dev/sda <!-- NAME -->

```CODE
parted /dev/sda                                                                          
  mklabel gpt                                                                                 
  mkpart boot 0% 100%                                                                         
 
```

> mklabel(создание таблицы разделов) {gpt, msdos}

> mkpart(создание раздела) boot(название раздела, любое)

> 0% 100%(начало и конец раздела в процентах) {1MiB 100%, 0% 50GB}

#### Создание раздела с указанием файловой системы <!-- NAME -->

```CODE
parted /dev/sdc                                                                          
  mklabel gpt                                                                                 
  mkpart root ext4 0% 100%                                                                    
 
```

> ext4(тип файловой системы) {ext4, xfs, btrfs, swap}

> root(название раздела, может быть любым{A–Z, a–z}, {0–9}, {`-`, `_`})

#### Создание нескольких разделов <!-- NAME -->

```CODE
parted /dev/sdd                                                                          
  mklabel gpt                                                                                 
  mkpart system 0% 50%                                                                        
  mkpart data 50% 100%                                                                        
 
```

> Создание двух разделов по 50% диска с названиями system и data

#### Создание раздела с точным размером <!-- NAME -->

```CODE
parted /dev/sde                                                                          
  mklabel gpt                                                                                 
  mkpart root 1MiB 10GiB
 
```

> 1MiB(начало раздела, выравнивание) 10GiB(конец раздела)

> Единицы измерения {MiB, GiB, TiB, MB, GB, TB}

#### Создание swap раздела <!-- NAME -->

```CODE
parted /dev/sdf                                                                          
  mklabel gpt                                                                                 
  mkpart swap linux-swap 0% 4GiB
  mkpart root ext4 4GiB 100%                                                                  
 
```

> Первый раздел для swap, второй для системы

#### Создание EFI раздела для UEFI систем <!-- NAME -->

```CODE
parted /dev/sdg                                                                          
  mklabel gpt                                                                                 
  mkpart EFI fat32 1MiB 512MiB                                                                
  set 1 esp on                                                                                
  mkpart root ext4 512MiB 100%                                                                
 
```

> EFI(название раздела) для загрузчика UEFI

> esp(флаг для UEFI загрузки) обязателен для EFI раздела

> Размер EFI раздела обычно 512MiB {256MiB, 512MiB, 1GiB}

> GPT обязательна для UEFI систем

#### Создание разметки для BIOS Legacy загрузки <!-- NAME -->

```CODE
parted /dev/sdh                                                                          
  mklabel msdos                                                                               
  mkpart primary ext4 1MiB 100%                                                               
  set 1 boot on                                                                               
 
```

> msdos(таблица разделов MBR) для BIOS Legacy систем

> boot(флаг загрузочного раздела) для Legacy BIOS

> Для BIOS Legacy лучше использовать msdos, не gpt

#### Создание разметки BIOS Legacy с swap <!-- NAME -->

```CODE
parted /dev/sdi                                                                          
  mklabel msdos                                                                               
  mkpart primary linux-swap 1MiB 4GiB                                                         
  mkpart primary ext4 4GiB 100%                                                               
  set 2 boot on                                                                               
 
```

> msdos для совместимости со старыми BIOS

> boot устанавливается на корневой раздел

#### Создание полной разметки с boot разделом <!-- NAME -->

```CODE
parted /dev/sdj                                                                          
  mklabel gpt                                                                                 
  mkpart boot ext4 1MiB 512MiB                                                                
  set 1 boot on                                                                               
  mkpart swap linux-swap 512MiB 4GiB                                                          
  set 2 swap on                                                                               
  mkpart root ext4 4GiB 100%                                                                  
 
```

> boot(название и флаг загрузочного раздела) для /boot

> swap(название и флаг раздела подкачки) для swap

> Типичная схема: boot + swap + root

#### Создание разметки для UEFI с boot и swap <!-- NAME -->

```CODE
parted /dev/sdk                                                                          
  mklabel gpt                                                                                 
  mkpart EFI fat32 1MiB 512MiB                                                                
  set 1 esp on                                                                                
  mkpart boot ext4 512MiB 1GiB                                                                
  set 2 boot on                                                                               
  mkpart swap linux-swap 1GiB 5GiB                                                            
  set 3 swap on                                                                               
  mkpart root ext4 5GiB 100%                                                                  
 
```

> esp(EFI раздел) + boot(/boot) + swap(подкачка) + root(корень)

> Полная схема для UEFI системы

#### Создание разметки с LVM <!-- NAME -->

```CODE
parted /dev/sdl                                                                          
  mklabel gpt                                                                                 
  mkpart EFI fat32 1MiB 512MiB                                                                
  set 1 esp on                                                                                
  mkpart lvm 512MiB 100%                                                                      
  set 2 lvm on                                                                                
 
```

> lvm(флаг для LVM) для физического тома LVM

> LVM позволяет гибко управлять разделами: изменять размер, создавать снапшоты, объединять диски

#### Пример использования LVM после создания раздела <!-- NAME -->

```CODE
pvcreate /dev/sdl2
  vgcreate vg0 /dev/sdl2                                                                      
  lvcreate -L 4G -n swap vg0                                                                  
  lvcreate -L 20G -n root vg0                                                                 
  lvcreate -l 100%FREE -n home vg0                                                            
 
```

> pvcreate(создание физического тома)

> vgcreate(создание группы томов) vg0(название группы)

> lvcreate(создание логического тома) -L(размер) -n(название) -l(процент свободного места)

> LVM позволяет изменять размер разделов без перезагрузки

#### Создание разметки с RAID <!-- NAME -->

```CODE
parted /dev/sdm                                                                          
  mklabel gpt                                                                                 
  mkpart raid1 1MiB 100%
  set 1 raid on                                                                               
 
```

> raid(флаг для RAID) для программного RAID массива

> RAID объединяет несколько дисков для отказоустойчивости или производительности

#### Неинтерактивное создание разметки <!-- NAME -->

```CODE
parted -s /dev/sdg mklabel gpt                                                           
  parted -s /dev/sdg mkpart root 0% 100%                                                      
 
```

> -s(неинтерактивный режим, без подтверждений)

#### Удаление раздела <!-- NAME -->

```CODE
parted /dev/sdh                                                                          
  rm 1                                                                                        
 
```

> rm(удаление раздела) 1(номер раздела)

#### Изменение размера раздела <!-- NAME -->

```CODE
parted /dev/sdi                                                                          
  resizepart 1 50GiB                                                                          
 
```

> resizepart(изменение размера) 1(номер раздела) 50GiB(новый размер)

#### Установка и снятие флагов раздела <!-- NAME -->

```CODE
parted /dev/sdj                                                                          
  set 1 boot on                                                                               
  set 1 boot off                                                                              
 
```

> set(установка флага) 1(номер раздела) boot(тип флага) on/off(включить/выключить)

> Типы флагов {boot, esp, swap, raid, lvm, bios_grub}

#### Просмотр доступных флагов <!-- NAME -->

```CODE
parted /dev/sda                                                                          
  help set                                                                                    
 
```

> Показывает все доступные флаги для установки

### Проверка <!-- HEAD -->

#### Просмотр разделов дисков <!-- NAME -->

```CODE
lsblk                                                                                    
 
```

> Показывает все блочные устройства и разделы

#### Просмотр информации о разделах диска <!-- NAME -->

```CODE
parted /dev/sda print                                                                    
 
```

> Показывает таблицу разделов конкретного диска с флагами

#### Просмотр всех дисков <!-- NAME -->

```CODE
parted -l                                                                                
 
```

> Показывает информацию о всех дисках в системе

#### Проверка выравнивания разделов <!-- NAME -->

```CODE
parted /dev/sda align-check optimal 1                                                    
 
```

> align-check(проверка выравнивания) optimal(тип) 1(номер раздела)

#### Проверка активации swap <!-- NAME -->

```CODE
swapon --show                                                                            
 
```

> Показывает активные swap разделы

#### Проверка монтирования EFI раздела <!-- NAME -->

```CODE
mount | grep efi                                                                         
 
```

> Показывает смонтированные EFI разделы

#### Проверка LVM томов <!-- NAME -->

```CODE
pvdisplay                                                                                
  vgdisplay                                                                                   
  lvdisplay                                                                                   
 
```

> Показывает физические тома, группы томов и логические тома LVM Исправления: - primary заменено на осмысленные названия разделов (boot, root, swap, data) - Для BIOS Legacy использую msdos, не gpt - Добавлено объяснение LVM: технология для гибкого управления разделами (изменение размера, снапшоты, объединение дисков) - Добавлен пример создания LVM томов после разметки
