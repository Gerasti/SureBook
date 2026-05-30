
### Установка RADIUS сервера <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get update && apt-get install -y freeradius freeradius-utils                         
 
```

#### Запуск службы <!-- NAME -->

```CODE
systemctl enable --now radiusd                                                           
                                                                                              
 
```

### Настройка RADIUS сервера <!-- HEAD -->

#### В /etc/raddb/clients.conf <!-- NAME -->

```CODE
client ALL {                                                                             
    ipaddr = 0.0.0.0
    netmask = 0                                                                               
    secret = P@ssw0rd                                                                         
  }                                                                                           
 
```

> ipaddr(IP клиента); netmask(маска сети); secret(общий секрет)

#### В конец /etc/raddb/users <!-- NAME -->

```CODE
netuser Cleartext-Password := "P@ssw0rd"                                                 
          Service-Type = Administrative-User,                                                 
          Cisco-AVPair = "shell:roles=admin"                                                  
 
```

> Cleartext-Password(пароль пользователя); Service-Type(тип доступа); Cisco-AVPair(роль для Cisco)

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart radiusd
                                                                                              
 
```

### Проверка RADIUS сервера <!-- HEAD -->

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status radiusd                                                                 
 
```

> служба должна быть active (running)

#### Тестирование аутентификации <!-- NAME -->

```CODE
radtest netuser P@ssw0rd localhost 0 P@ssw0rd                                            
 
```

> должен вернуть Access-Accept

### Установка RADIUS клиента <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get update && apt-get install -y pam_radius                                          
 
```

#### В /etc/pam_radius_auth.conf <!-- NAME -->

```CODE
<ip сервера> P@ssw0rd 3                                                                  
 
```

> формат: IP секрет таймаут

#### В /etc/pam.d/sshd и /etc/pam.d/system-auth-local <!-- NAME -->

```CODE
auth  sufficient  pam_radius_auth.so                                                     
 
```

> sufficient(достаточно для авторизации); pam_radius_auth.so(модуль RADIUS)

#### Создание пользователя <!-- NAME -->

```CODE
useradd netuser                                                                          
 
```

> пользователь должен совпадать с настроенным на сервере

### Проверка RADIUS клиента <!-- HEAD -->

#### Проверка подключения через SSH <!-- NAME -->

```CODE
ssh netuser@<ip клиента>                                                                 
 
```

> вход должен пройти с паролем P@ssw0rd через RADIUS-сервер
