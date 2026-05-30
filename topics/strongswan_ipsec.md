
### Установка <!-- HEAD -->

#### Установка StrongSwan <!-- NAME -->

```CODE
apt-get install strongswan
                                                                                              
 
```

### Настройка первого маршрутизатора <!-- HEAD -->

#### Основной конфигурационный файл <!-- NAME -->

```CODE
/etc/strongswan/ipsec.conf
                                                                                              
 
```

#### Настройка /etc/strongswan/ipsec.conf на маршрутизаторе 10.10.10.1 <!-- NAME -->

```CODE
config setup                                                                             
                                                                                              
  conn nameConnect                                                                            
      authby=psk                                                                              
      keyexchange=ikev2                                                                       
                                                                                              
  leftid=10.10.10.1                                                                           
  left=10.10.10.1                                                                             
  leftsubnet=10.10.10.0/30                                                                    
                                                                                              
  rightid=10.10.10.2                                                                          
  right=10.10.10.2                                                                            
  rightsubnet=10.10.10.0/30                                                                   
                                                                                              
  auto=start                                                                                  
 
```

> authby=psk(аутентификация по общему ключу); keyexchange=ikev2(протокол обмена ключами); leftid(публичный идентификатор локального узла); left(локальный IP-адрес); leftsubnet(локальная подсеть); rightid(публичный идентификатор удалённого узла); right(удалённый IP-адрес); rightsubnet(удалённая подсеть); auto=start(автоматический запуск туннеля)

#### Файл с общими ключами <!-- NAME -->

```CODE
/etc/strongswan/ipsec.secrets                                                            
                                                                                              
 
```

#### Настройка /etc/strongswan/ipsec.secrets на маршрутизаторе 10.10.10.1 <!-- NAME -->

```CODE
10.10.10.1 10.10.10.2 : PSK "P@ssw0rd"                                                   
 
```

> Формат: локальный_IP удалённый_IP : PSK "пароль"

### Настройка второго маршрутизатора <!-- HEAD -->

#### Настройка /etc/strongswan/ipsec.conf на маршрутизаторе 10.10.10.2 <!-- NAME -->

```CODE
config setup 
                                                                                              
  conn nameConnect                                                                            
      authby=psk
      keyexchange=ikev2                                                                       
                                                                                              
  leftid=10.10.10.2                                                                           
  left=10.10.10.2                                                                             
  leftsubnet=10.10.10.0/30                                                                    
                                                                                              
  rightid=10.10.10.1                                                                          
  right=10.10.10.1                                                                            
  rightsubnet=10.10.10.0/30                                                                   
                                                                                              
  auto=start                                                                                  
 
```

> Зеркальная конфигурация: left и right меняются местами

#### Настройка /etc/strongswan/ipsec.secrets на маршрутизаторе 10.10.10.2 <!-- NAME -->

```CODE
10.10.10.2 10.10.10.1 : PSK "P@ssw0rd"                                                   
 
```

> Тот же пароль, адреса в обратном порядке

### Запуск <!-- HEAD -->

#### Запуск и автозагрузка службы на обоих маршрутизаторах <!-- NAME -->

```CODE
systemctl enable --now strongswan-starter ipsec
                                                                                              
 
```

### Проверка <!-- HEAD -->

#### Проверка статуса туннеля <!-- NAME -->

```CODE
ipsec status
 
```

> Показывает состояние IPsec соединений

#### Проверка связности через туннель <!-- NAME -->

```CODE
ping 10.10.10.2                                                                          
 
```

> С первого маршрутизатора, с второго ping 10.10.10.1
