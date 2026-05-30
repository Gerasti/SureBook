
### Управление временем через timedatectl <!-- HEAD -->

#### Просмотр текущего времени и настроек <!-- NAME -->

```CODE
timedatectl  
 
```

> Показывает локальное время, UTC, часовой пояс, синхронизацию NTP

#### Просмотр статуса синхронизации времени <!-- NAME -->

```CODE
timedatectl status                                                           
 
```

> Показывает полную информацию

### Настройка времени <!-- HEAD -->

#### Установка текущей даты и времени <!-- NAME -->

```CODE
timedatectl set-time "2026-05-31 10:30:00"
 
```

> Формат: YYYY-MM-DD HH:MM:SS

#### Установка только даты <!-- NAME -->

```CODE
timedatectl set-time "2026-05-31"                                            
                                                                                  
 
```

#### Установка только времени <!-- NAME -->

```CODE
timedatectl set-time "10:30:00"                                              
                                                                                  
 
```

### Настройка часового пояса <!-- HEAD -->

#### Просмотр текущего часового пояса <!-- NAME -->

```CODE
timedatectl show-timezones
 
```

> Показывает список всех доступных часовых поясов

#### Поиск часового пояса <!-- NAME -->

```CODE
timedatectl list-timezones | grep Moscow                                     
                                                                                  
 
```

#### Установка часового пояса <!-- NAME -->

```CODE
timedatectl set-timezone Europe/Moscow                                       
 
```

> Часовой пояс Москвы

#### Установка UTC <!-- NAME -->

```CODE
timedatectl set-timezone UTC                                                 
                                                                                  
 
```

### Настройка NTP-синхронизации <!-- HEAD -->

#### Включение NTP-синхронизации <!-- NAME -->

```CODE
timedatectl set-ntp true
 
```

> Включает автоматическую синхронизацию времени через systemd-timesyncd

#### Отключение NTP-синхронизации <!-- NAME -->

```CODE
timedatectl set-ntp false                                                    
 
```

> Отключает автоматическую синхронизацию, позволяет устанавливать время вручную

#### Проверка статуса NTP-синхронизации <!-- NAME -->

```CODE
timedatectl timesync-status                                                  
 
```

> Показывает сервер, stratum, задержку, смещение времени

### Настройка аппаратных часов <!-- HEAD -->

#### Синхронизация системного времени с аппаратными часами <!-- NAME -->

```CODE
hwclock --systohc
 
```

> Записывает системное время в аппаратные часы (RTC)

#### Синхронизация аппаратных часов с системным временем <!-- NAME -->

```CODE
hwclock --hctosys                                                            
 
```

> Устанавливает системное время из аппаратных часов

#### Просмотр аппаратных часов <!-- NAME -->

```CODE
hwclock --show                                                               
 
```

> Показывает время из RTC

#### Установка аппаратных часов в UTC <!-- NAME -->

```CODE
timedatectl set-local-rtc 0                                                  
 
```

> 0(RTC в UTC), рекомендуется для Linux

#### Установка аппаратных часов в локальное время <!-- NAME -->

```CODE
timedatectl set-local-rtc 1                                                  
 
```

> 1(RTC в локальном времени), используется для совместимости с Windows

### Проверка <!-- HEAD -->

#### Просмотр всех свойств <!-- NAME -->

```CODE
timedatectl show
 
```

> Показывает все параметры в формате ключ=значение

#### Просмотр конкретного свойства <!-- NAME -->

```CODE
timedatectl show -p Timezone                                                 
 
```

> -p(конкретное свойство): Timezone, NTPSynchronized, LocalRTC

#### Просмотр логов службы времени <!-- NAME -->

```CODE
journalctl -u systemd-timesyncd                                              
                                                                                  
 
```

### Примеры часовых поясов <!-- LIST -->
- Europe/Moscow (Москва, UTC+3)
- Asia/Yekaterinburg (Екатеринбург, UTC+5)
- Asia/Novosibirsk (Новосибирск, UTC+7)
- Asia/Vladivostok (Владивосток, UTC+10)
- UTC (Всемирное координированное время)
