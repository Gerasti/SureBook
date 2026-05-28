
### Управление пользователями и группами <!-- HEAD -->

#### Создание группы <!-- NAME -->

```CODE
samba-tool group add <имя_группы>                                                                     
                                                                                                           
 
```

#### Создание пользователя <!-- NAME -->

```CODE
samba-tool user create <имя_пользователя>                                                             
                                                                                                           
 
```

#### Добавление пользователя в группу <!-- NAME -->

```CODE
samba-tool group addmembers <имя_группы> <имя_пользователя>                                           
                                                                                                           
 
```

#### Список пользователей <!-- NAME -->

```CODE
samba-tool user list                                                                                  
                                                                                                           
 
```

#### Список участников группы <!-- NAME -->

```CODE
samba-tool group listmembers <имя_группы>                                                             
                                                                                                           
 
```

### Политика паролей <!-- HEAD -->

#### Настройка сложности и длины пароля <!-- NAME -->

```CODE
samba-tool domain passwordsettings set --complexity=off                                               
  samba-tool domain passwordsettings set --min-pwd-length=1                                                
  samba-tool domain passwordsettings set --max-pwd-age=0                                                   
  samba-tool domain passwordsettings set --min-pwd-age=0                                                   
  samba-tool domain passwordsettings set --pwd-history-length=0                                            
 
```

> --complexity(сложность паролей); --min-pwd-length(минимальная длина); --max-pwd-age(срок действия пароля); --min-pwd-age(минимальный возраст пароля); --pwd-history-length(история паролей)

### Политика блокировки <!-- HEAD -->

#### Настройка блокировки учетных записей <!-- NAME -->

```CODE
samba-tool domain passwordsettings set --lockout-threshold=0                                          
  samba-tool domain passwordsettings set --lockout-duration=30                                             
  samba-tool domain passwordsettings set --reset-count=30                                                  
 
```

> --lockout-threshold(порог блокировки); --lockout-duration(длительность блокировки); --reset-count(интервал сброса счетчика)

### Kerberos-политика <!-- HEAD -->

#### Настройка времени жизни билетов <!-- NAME -->

```CODE
samba-tool domain passwordsettings set --krb-ticket-lifetime=24                                       
  samba-tool domain passwordsettings set --krb-renewal-lifetime=168                                        
 
```

> --krb-ticket-lifetime(срок жизни билета в часах); --krb-renewal-lifetime(срок обновления билета)

### Параметры учетных записей <!-- HEAD -->

#### Хранение паролей в открытом виде <!-- NAME -->

```CODE
samba-tool domain passwordsettings set --store-plaintext-password=yes                                 
  samba-tool domain passwordsettings set --allow-plaintext-password=yes                                    
 
```

> только для тестовых стендов; не рекомендуется в продакшене

### Параметры безопасности домена <!-- HEAD -->

#### Настройка криптографии <!-- NAME -->

```CODE
samba-tool domain passwordsettings set --allow-microsecond-timestamps=yes                             
  samba-tool domain passwordsettings set --allow-weak-crypto=yes                                           
 
```

> снижает безопасность; для совместимости со старыми устройствами

### Политика времени Kerberos <!-- HEAD -->

#### Настройка флагов политики <!-- NAME -->

```CODE
samba-tool domain passwordsettings set --krb-policy-flags=0x00000000                                  
                                                                                                           
 
```

### Аудит и логирование <!-- HEAD -->

#### Просмотр уровня домена <!-- NAME -->

```CODE
samba-tool domain level show                                                                          
                                                                                                           
 
```

#### Увеличение детализации логов <!-- NAME -->

```CODE
smbcontrol all debug 3                                                                                
  smbcontrol all debug 10                                                                                  
 
```

> debug 3(средний уровень); debug 10(максимальная детализация)

### Уровень функциональности домена <!-- HEAD -->

#### Просмотр уровня домена <!-- NAME -->

```CODE
samba-tool domain level show                                                                          
                                                                                                           
 
```

#### Повышение уровня домена и леса <!-- NAME -->

```CODE
samba-tool domain level raise --domain-level=2008_R2                                                  
  samba-tool domain level raise --forest-level=2008_R2                                                     
 
```

> 2008_R2(Windows Server 2008 R2)

### Проверка политики <!-- HEAD -->

#### Просмотр всех настроек политики паролей <!-- NAME -->

```CODE
samba-tool domain passwordsettings show                                                               
                                                                                                           
 
```

### Управление DNS <!-- HEAD -->

#### Добавление A-записи в DNS <!-- NAME -->

```CODE
samba-tool dns add 127.0.0.1 <домен> <имя_устройства> A <ip_адрес> -U administrator                   
 
```

> пример: samba-tool dns add 127.0.0.1 office.ssa2026.region rtr-a A 172.20.10.254 -U administrator

### Создание организационных единиц <!-- HEAD -->

#### Создание OU <!-- NAME -->

```CODE
samba-tool ou create "OU=CLI,DC=ad-team,DC=info"                                                      
                                                                                                           
 
```

### Массовое создание пользователей <!-- HEAD -->

#### Создание нескольких пользователей циклом <!-- NAME -->

```CODE
for i in {1..5}; do samba-tool user create "hq$i" "P@ssw0rd"; done                                    
                                                                                                           
 
```

#### Создание группы <!-- NAME -->

```CODE
samba-tool group add hq                                                                               
                                                                                                           
 
```

#### Массовое добавление пользователей в группу <!-- NAME -->

```CODE
for i in {1..5}; do samba-tool group addmembers hq "hq$i"; done                                       
 
```

> цикл for создает пользователей hq1, hq2, hq3, hq4, hq5 и добавляет их в группу hq
