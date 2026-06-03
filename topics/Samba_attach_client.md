
#### Установка пакетов на клиенте <!-- NAME -->

```CODE
apt-get update && apt-get install -y task-auth-ad-sssd                                   

```

#### Запуск служб на клиенте <!-- NAME -->

```CODE
systemctl enable --now smb winbind sssd                                                  

```

#### Содержимое /etc/krb5.conf на клиенте <!-- NAME -->

```CODE
[libdefaults]                                                                            
default_realm = AD.TEAM                                                                     
dns_lookup_kdc = true
dns_lookup_realm = false                                                                    
ticket_lifetime = 24h                                                                       
renew_lifetime = 7d                                                                         
forwardable = true                                                                          
rdns = false                                                                                
default_ccache_name = KEYRING:persistent:%{uid}                                             

```

#### Установка пакетов на клиенте <!-- NAME -->

```CODE
apt-get update && apt-get install -y task-auth-ad-sssd                                   
```

> task-auth-ad-sssd(метапакет для аутентификации в Active Directory через SSSD)

#### Запуск служб на клиенте <!-- NAME -->

```CODE
systemctl enable --now smb winbind sssd
```

> smb(Samba, интеграция с Windows-сетями); winbind(связь между Linux и AD); sssd(System Security Services Daemon, аутентификация и авторизация)

#### Содержимое /etc/krb5.conf на клиенте <!-- NAME -->

```CODE
[libdefaults]
default_realm = AD.TEAM                                                                     
dns_lookup_kdc = true                                                                       
dns_lookup_realm = false                                                                    
ticket_lifetime = 24h                                                                       
renew_lifetime = 7d                                                                         
forwardable = true                                                                          
rdns = false                                                                                
default_ccache_name = KEYRING:persistent:%{uid}                                             

[realms]
AD.TEAM = {                                                                                 
kdc = 192.168.11.67                                                                     
default_domain = ad.team                                                                
admin_server = 192.168.11.67                                                            
}                                                                                           

[domain_realm]                                                                              
.ad.team = AD.TEAM                                                                          
ad.team = AD.TEAM                                                                           
```

> [libdefaults](глобальные настройки Kerberos); default_realm(realm по умолчанию, должен быть в верхнем регистре); dns_lookup_kdc(искать KDC через DNS SRV-записи); dns_lookup_realm(искать realm через DNS TXT-записи); ticket_lifetime(время жизни билета аутентификации, формат: {Ns, Nm, Nh, Nd}); renew_lifetime(максимальное время продления билета без повторного ввода пароля); forwardable(разрешить передачу билета другим службам); rdns(reverse DNS lookup, отключить для избежания проблем с разрешением имён); default_ccache_name(расположение кеша учётных данных: KEYRING сохраняет в ядре, persistent сохраняется между сессиями, %{uid} подставляет UID пользователя)

> [realms](описание конкретных realm); kdc(IP-адрес или hostname контроллера домена Key Distribution Center); default_domain(доменное имя в нижнем регистре); admin_server(сервер администрирования Kerberos для смены паролей)

> [domain_realm](маппинг доменных имён на realm); .ad.team(поддомены домена); ad.team(сам домен); оба мапятся на realm AD.TEAM в верхнем регистре

#### В /etc/resolv.conf на клиенте <!-- NAME -->

```CODE
domain ad.team
nameserver 192.168.11.67                                                                    
nameserver 192.168.33.67                                                                    
nameserver 8.8.8.8                                                                          
```

> domain(доменный суффикс для поиска); nameserver(DNS-серверы); первым указывать IP контроллера домена для корректной работы DNS-запросов к AD

#### Проверка Kerberos на клиенте <!-- NAME -->

```CODE
kinit administrator
klist                                                                                       
```

> kinit(получить Kerberos-билет для пользователя, запросит пароль); klist(показать кешированные билеты с временем жизни и сроком действия)

#### Присоединение к домену <!-- NAME -->

```CODE
net ads join -U administrator@AD.TEAM -S 192.168.11.67
```

> net ads join(присоединить машину к домену Active Directory); -U(пользователь с правами присоединения к домену); -S(IP-адрес сервера AD)

#### Дополнительно в ALT Linux можно воспользоваться GUI <!-- NAME -->

```CODE
apt-get install admc
```

#### Запуск admc от root(также иметь билет Kerberos для administrator) <!-- LIST -->
- Пользователи -> Аутентификация
- Домен Active Directory
    - Домен(ad.team)
    - Имя компьютера(hostname)
    - SSSD(в единственном домене)
- Применить
    - Имя пользователя(Administrator)
    - Пароль(P@ssw0rd)
    - ОК

> При успешном подключении будет уведомление "Добро пожаловать в домен"

#### Проверка DNS на клиенте <!-- NAME -->

```CODE
host srv-hq  
host $(hostname)                                                                            
```

> host(проверить разрешение DNS-имени); проверяет разрешение имени сервера и собственного hostname

#### Перезагрузка клиента <!-- NAME -->

```CODE
reboot       
```

> Применяет все изменения конфигурации

#### Вход под доменным пользователем <!-- NAME -->

```CODE
su - username@AD.TEAM                                                                    
id                                                                                          
```

> su - (переключиться на пользователя с загрузкой его окружения); id(показать UID, GID и группы пользователя) [realms]
