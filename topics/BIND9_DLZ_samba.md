
### Установка Samba AD DC с BIND9_DLZ <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get install -y task-samba-dc bind                                                    
                                                                                              
 
```

#### Отключение chroot для BIND <!-- NAME -->

```CODE
control bind-chroot disabled                                                             
                                                                                              
 
```

#### Подключение конфигурации BIND9_DLZ <!-- NAME -->

```CODE
grep -q 'bind-dns' /etc/bind/named.conf || echo 'include                                 
  "/var/lib/samba/bind-dns/named.conf";' >> /etc/bind/named.conf                              
                  
 
```

#### В /etc/bind/options.conf добавить <!-- NAME -->

```CODE
tkey-gssapi-keytab "/var/lib/samba/bind-dns/dns.keytab";
  minimal-responses yes;                                                                      
 
```

> tkey-gssapi-keytab(путь к keytab для GSSAPI); minimal-responses(минимальные ответы DNS)

#### Остановка BIND перед настройкой <!-- NAME -->

```CODE
systemctl stop bind                                                                      
                                                                                              
 
```

#### В /etc/sysconfig/network <!-- NAME -->

```CODE
NETWORKING=yes                                                                           
  CONFMETHOD=etcnet                                                                           
  HOSTNAME=srv-hq.ad.team                                                                     
  RESOLV_MODS=yes                                                                             
 
```

> HOSTNAME(полное имя сервера с доменом); RESOLV_MODS(разрешить изменение resolv.conf)

#### Установка hostname <!-- NAME -->

```CODE
hostnamectl set-hostname srv-hq.ad.team;exec bash                                        
  domainname ad.team                                                                          
 
```

> exec bash перезагружает оболочку для применения изменений

### Очистка старых конфигураций <!-- HEAD -->

#### Удаление старых файлов Samba <!-- NAME -->

```CODE
rm -f /etc/samba/smb.conf                                                                
  rm -rf /var/lib/samba                                                                       
  rm -rf /var/cache/samba                                                                     
  mkdir -p /var/lib/samba/sysvol                                                              
 
```

> Конфликты зон возникают при одинаковых доменах в BIND и SAMBA BIND9_DLZ

#### В /etc/resolv.conf указать локальный DNS <!-- NAME -->

```CODE
nameserver 127.0.0.1                                                                     
 
```

> Контроллер домена должен использовать себя как DNS-сервер

### Создание домена <!-- HEAD -->

#### Провижининг домена Samba AD <!-- NAME -->

```CODE
samba-tool domain provision --realm=ad.team --domain=ad --adminpass='P@ssw0rd'           
  --dns-backend=BIND9_DLZ --server-role=dc --use-rfc2307                                      
 
```

> --realm(полное имя домена); --domain(NetBIOS имя); --dns-backend(BIND9_DLZ или SAMBA_INTERNAL); --server-role(dc - контроллер домена); --use-rfc2307(поддержка POSIX атрибутов)

#### Запуск служб <!-- NAME -->

```CODE
systemctl enable --now samba
  systemctl enable --now bind                                                                 
                                                                                              
 
```

#### Копирование конфигурации Kerberos <!-- NAME -->

```CODE
cp /var/lib/samba/private/krb5.conf /etc/krb5.conf                                       
                                                                                              
 
```

### Проверка контроллера домена <!-- HEAD -->

#### Проверка информации о домене <!-- NAME -->

```CODE
samba-tool domain info 127.0.0.1                                                         
                                                                                              
 
```

#### Проверка DNS SRV-записей <!-- NAME -->

```CODE
host -t SRV _kerberos._udp.ad.team                                                       
  host -t SRV _ldap._tcp.ad.team                                                              
  host -t A srv-hq.ad.team                                                                    
 
```

> SRV-записи должны указывать на контроллер домена

#### Проверка Kerberos <!-- NAME -->

```CODE
kinit administrator@AD.TEAM                                                              
  klist                                                                                       
 
```

> kinit(получение билета); klist(просмотр билетов); realm указывать ЗАГЛАВНЫМИ буквами

### Присоединение клиента к домену <!-- HEAD -->

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
                                                                                              
  [realms]                                                                                    
  AD.TEAM={                                                                                   
          kdc = 192.168.11.67                                                                 
          default_domain = ad.team                                                            
          admin_server = 192.168.11.67                                                        
  }                                                                                           
                                                                                              
  [domain_realm]                                                                              
  .ad.team = AD.TEAM
  ad.team = AD.TEAM                                                                           
 
```

> kdc(IP контроллера домена); ticket_lifetime(время жизни билета); renew_lifetime(время обновления); forwardable(передача билета)

#### В /etc/resolv.conf на клиенте <!-- NAME -->

```CODE
domain ad.team
  nameserver 192.168.11.67                                                                    
  nameserver 192.168.33.67                                                                    
  nameserver 8.8.8.8                                                                          
 
```

> Первым указывать IP контроллера домена

#### Проверка Kerberos на клиенте <!-- NAME -->

```CODE
kinit administrator                                                                      
  klist                                                                                       
                                                                                              
 
```

#### Присоединение к домену <!-- NAME -->

```CODE
net ads join -U administrator@AD.TEAM -S 192.168.11.67                                   
 
```

> -U(пользователь); -S(IP сервера)

#### Проверка DNS на клиенте <!-- NAME -->

```CODE
host srv-hq                                                                              
  host $(hostname)                                                                            
                                                                                              
 
```

#### Перезагрузка клиента <!-- NAME -->

```CODE
reboot                                                                                   
                                                                                              
 
```

#### Вход под доменным пользователем <!-- NAME -->

```CODE
su -
  id
```
