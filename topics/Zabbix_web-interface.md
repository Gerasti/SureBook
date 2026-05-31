
#### Установка пакетов <!-- NAME -->

```CODE
apt-get install zabbix-phpfrontend-apache2 zabbix-phpfrontend-php8.2                     
 
```

> zabbix-phpfrontend-apache2(веб-интерфейс для Apache2); zabbix-phpfrontend-php8.2(поддержка PHP 8.2)

#### Включение конфигурации Apache2 <!-- NAME -->

```CODE
ln -s /etc/httpd2/conf/addon.d/A.zabbix.conf /etc/httpd2/conf/extra-enabled/
 
```

> создает символическую ссылку для активации конфигурации Zabbix

#### Перезапуск Apache2 <!-- NAME -->

```CODE
systemctl restart httpd2                                                                 
                                                                                              
 
```

#### Изменение владельца для веб-установщика <!-- NAME -->

```CODE
chown apache2:apache2 /var/www/webapps/zabbix/ui/conf                                    
 
```

> необходимо для записи конфигурации при установке

### Настройка через веб-интерфейс <!-- HEAD -->

#### Открытие веб-установщика <!-- NAME -->

```CODE
http://<ip сервера>/zabbix
 
```

> открыть в браузере

#### Параметры подключения к базе данных <!-- LIST -->
- type database: PostgreSQL{MySQL}
- host: localhost
- port: 0
- name: zabbix
- scheme: public
- user: zabbix
- password: zabbixpwd

> port 0(автоматически использует порт по умолчанию: PostgreSQL 5432, MySQL 3306); scheme(схема базы данных)

### Проверка <!-- HEAD -->

#### Вход в веб-интерфейс <!-- NAME -->

```CODE
http://<ip сервера>/zabbix

 
```

> открыть страницу входа

#### Учетные данные по умолчанию <!-- NAME -->

```CODE
username: Admin                                                                          
  password: zabbix                                                                            
 
```

> Admin с заглавной буквы; рекомендуется сменить пароль после первого входа

#### Проверка статуса Apache2 <!-- NAME -->

```CODE
systemctl status httpd2                                                                  
 
```

> служба должна быть active (running)

#### Проверка прав на каталог конфигурации <!-- NAME -->

```CODE
ls -la /var/www/webapps/zabbix/ui/conf
```
