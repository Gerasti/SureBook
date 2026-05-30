
### Установка VMware Tools <!-- HEAD -->

#### Установка пакетов open-vm-tools <!-- NAME -->

```CODE
apt-get install open-vm-tools open-vm-tools-desktop xrandr
 
```

> open-vm-tools(базовые функции: общая папка, синхронизация времени, буфер обмена); open-vm-tools-desktop(автоматическое разрешение экрана, интеграция мыши, графика); xrandr(утилита для управления разрешением экрана)

#### Включение службы в автозагрузку <!-- NAME -->

```CODE
systemctl enable vmtoolsd
                                                                                  
 
```

#### Запуск службы <!-- NAME -->

```CODE
systemctl start vmtoolsd                                                     
                                                                                  
 
```

### Проверка <!-- HEAD -->

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status vmtoolsd
                                                                                  
 
```

#### Проверка версии VMware Tools <!-- NAME -->

```CODE
vmware-toolbox-cmd -v                                                        
                                                                                  
 
```

#### Проверка работы буфера обмена <!-- NAME -->

```CODE
vmware-toolbox-cmd stat clipboard                                            
                                                                                  
 
```

#### Проверка синхронизации времени <!-- NAME -->

```CODE
vmware-toolbox-cmd timesync status                                           
                                                                                  
 
```

### Настройка <!-- HEAD -->

#### Включение синхронизации времени с хостом <!-- NAME -->

```CODE
vmware-toolbox-cmd timesync enable
                                                                                  
 
```

#### Отключение синхронизации времени с хостом <!-- NAME -->

```CODE
vmware-toolbox-cmd timesync disable                                          
                                                                                  
 
```

#### Ручная настройка разрешения экрана <!-- NAME -->

```CODE
xrandr --output Virtual1 --mode 1920x1080                                    
 
```

> Virtual1(имя дисплея, может быть Virtual-1, HDMI-1); --mode(разрешение экрана)

#### Просмотр доступных разрешений <!-- NAME -->

```CODE
xrandr
```
