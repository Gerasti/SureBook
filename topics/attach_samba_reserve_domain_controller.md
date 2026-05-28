
### Установка Samba DC <!-- HEAD -->

#### Установка пакета task-samba-dc <!-- NAME -->

```CODE
apt-get install -y task-samba-dc                                                                      
                                                                                                           
 
```

### Настройка DNS <!-- HEAD -->

#### В /etc/resolv.conf <!-- NAME -->

```CODE
search ad.team                                                                                        
  nameserver 192.168.11.67                                                                                 
  nameserver 192.168.33.67                                                                                 
  nameserver 8.8.8.8                                                                                       
 
```

> search(домен поиска); nameserver(DNS серверы)

### Настройка Kerberos <!-- HEAD -->

#### В /etc/krb5.conf <!-- NAME -->

```CODE
[libdefaults]                                                                                         
  default_realm = AD.TEAM                                                                                  
  dns_lookup_kdc = true                                                                                    
  dns_lookup_realm = false                                                                                 
                                                                                                           
  [realms]                                                                                                 
  AD.TEAM = {                                                                                              
  kdc = srv-hq.ad.team                                                                                     
  default_domain = ad.team                                                                                 
  }                                                                                                        
                                                                                                           
  [domain_realm]                                                                                           
  .ad.team = AD.TEAM
  ad.team = AD.TEAM                                                                                        
 
```

> default_realm(область по умолчанию); dns_lookup_kdc(поиск KDC через DNS); kdc(контроллер домена); domain_realm(сопоставление доменов)

### Регистрация вторичного DC в DNS <!-- HEAD -->

#### Добавление A-записи в BIND9_DLZ <!-- NAME -->

```CODE
samba-tool dns add srv-hq ad.team srv-dt A 192.168.33.67 -Uadministrator                              
 
```

> samba-tool dns add(добавление DNS записи); A(тип записи); -U(пользователь)

### Проверка подключения <!-- HEAD -->

#### Проверка разрешения имени <!-- NAME -->

```CODE
host srv-hq                                                                                           
 
```

> должен вернуть srv-hq.ad.team has address 192.168.11.67

#### Получение Kerberos билета <!-- NAME -->

```CODE
kinit administrator                                                                                   
 
```

> вводится пароль administrator@AD.TEAM

#### Проверка полученных билетов <!-- NAME -->

```CODE
klist                                                                                                 
 
```

> показывает кэш билетов и срок действия

### Присоединение к домену <!-- HEAD -->

#### Подключение как контроллер домена <!-- NAME -->

```CODE
samba-tool domain join ad.team DC -Uadministrator --realm=ad.team --workgroup=ad                      
 
```

> domain join(присоединение к домену); DC(режим контроллера домена); --realm(область Kerberos); --workgroup(рабочая группа)

#### Запуск службы Samba <!-- NAME -->

```CODE
systemctl enable --now samba
```
