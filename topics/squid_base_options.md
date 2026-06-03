
### Установка <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get install squid squid-helpers                                                      
```

> squid(прокси-сервер); squid-helpers(модули аутентификации)

### Настройка Squid с аутентификацией через Samba AD <!-- HEAD -->

#### В /etc/squid/squid.conf <!-- NAME -->

```CODE
auth_param basic program /usr/lib/squid/basic_smb_lm_auth AD/srv-hq.ad.team
auth_param basic children 5                                                                 
auth_param basic realm Proxy Authentication Required                                        
auth_param basic credentialsttl 2 hours                                                     

external_acl_type check_group %LOGIN /usr/lib/squid/ext_wbinfo_group_acl -d                 

acl authenticated proxy_auth REQUIRED                                                       
acl group1 external check_group group1
acl group2 external check_group group2                                                      
acl group3 external check_group group3                                                      
acl enterprise_services dst 192.168.0.0/16                                                  
acl monitoring_system dst 192.168.1.100                                                     
acl cli_hq src 192.168.2.10                                                                 
acl forbidden_domains dstdomain vk.com mail.yandex.ru worldskills.org                       

http_access allow authenticated group1 enterprise_services                                  
http_access allow authenticated group2 monitoring_system                                    
http_access deny group3                                                                     
http_access allow cli_hq !forbidden_domains                                                 
http_access deny all                                                                        

http_port 3128                                                                              
```

> basic_smb_lm_auth(аутентификация через SMB); ext_wbinfo_group_acl(проверка групп через Winbind); authenticated(требует аутентификацию); dst(назначение); src(источник); !(отрицание); правила обрабатываются сверху вниз

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart squid

```

### Управление пользователями <!-- HEAD -->

#### Смена пароля пользователя в Samba <!-- NAME -->

```CODE
samba-tool user setpassword USER
```

> USER(имя пользователя домена)

### Проверка <!-- HEAD -->

#### Проверка конфигурации Squid <!-- NAME -->

```CODE
squid -k parse
```

> проверяет синтаксис squid.conf

#### Проверка работы прокси с аутентификацией <!-- NAME -->

```CODE
curl -v -x http://<ip прокси>:3128 --proxy-user "user1:P@ssw0rd" http://192.168.0.10     
```

> -x(адрес прокси); --proxy-user(учетные данные); -v(подробный вывод)

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status squid                                                                   
```

> служба должна быть active (running)

#### Просмотр логов доступа <!-- NAME -->

```CODE
tail -f /var/log/squid/access.log                                                        
```

> показывает запросы в реальном времени
