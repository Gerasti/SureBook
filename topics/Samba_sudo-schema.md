
### Установка sudo-samba-schema <!-- HEAD -->

#### Добавление временного репозитория <!-- NAME -->

```CODE
echo "rpm http://altrepo.ru/local-p10 noarch local-p10" >>  
/etc/apt/sources.list                                          
```

#### Установка пакета <!-- NAME -->

```CODE
apt-get install sudo-samba-schema                           
```

#### Удаление временного репозитория <!-- NAME -->

```CODE
sed -i '/altrepo.ru\/local-p10/d' /etc/apt/sources.list     
```

#### Настройка DNS в /etc/resolv.conf <!-- NAME -->

```CODE
nameserver <ip_локального_сервера>                                   
```

> Оставляем только локальный DNS

#### Перезапуск Samba <!-- NAME -->

```CODE
systemctl restart samba                                     
```

### Настройка схемы sudo в AD <!-- HEAD -->

#### Применение схемы sudo <!-- NAME -->

```CODE
sudo-schema-apply                                           
```

> Ответить Yes, ввести Administrator и пароль, подтвердить Ok

#### Создание роли sudo <!-- NAME -->

```CODE
create-sudo-role                                            
```

> Вводим: OU=sudoers,dc=DOMAIN,dc=SAMPLE

> Имя роли: pravila_hq

> sudoHost: ALL

> sudoCommand: /bin/cat

> sudoUser: %hq

### Настройка через ADMC <!-- HEAD -->

#### Установка ADMC на клиенте <!-- NAME -->

```CODE
apt-get install admc                                        
```

#### Аутентификация <!-- NAME -->

```CODE
kinit administrator                                         
```

#### Запуск ADMC <!-- NAME -->

```CODE
sudo admc                                                   
```

#### Включение дополнительных возможностей <!-- NAME -->

#### Настройка правила pravila_hq <!-- LIST -->
- Настройки → Включить Дополнительные возможности
- domain.sample → sudoers → pravila_hq → Правой кнопкой мыши → Свойства
- Атрибуты → sudoOption → Изменить → Добавить параметр !authenticate → Apply
- Атрибуты → sudoCommand → Изменить → Добавить /bin/grep и /usr/bin/id → Apply

### Настройка клиента <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get install sudo libsss_sudo                            
```

#### Настройка прав sudo <!-- NAME -->

```CODE
control sudo public                                         
```

#### Настройка SSSD в /etc/sssd/sssd.conf <!-- NAME -->

```CODE
[sssd]                                                      
services = nss, pam, sudo                                      

[pam]                                                          

[domain/DOMAIN.SAMPLE]                                          
sudo_provider = ad
```

#### Настройка NSS в /etc/nsswitch.conf <!-- NAME -->

```CODE
sudoers: files sss                                          
```

#### Очистка кэша и перезапуск <!-- NAME -->

```CODE
rm -rf /var/lib/sss/db/*                                    
sss_cache -E                                                   
systemctl restart sssd                                         
```

> Можно выполнить reboot вместо очистки кэша

### Проверка <!-- HEAD -->

#### Вход за пользователя hquser1 <!-- NAME -->

```CODE
sudo cat /etc/passwd | sudo grep root && sudo id root       
```

> Должны выполниться команды без запроса пароля благодаря !authenticate
