
### Установка <!-- HEAD -->

#### Установка пакета на клиенте <!-- NAME -->

```CODE
apt-get install zabbix-agent                                                             
   
 
```

### Настройка <!-- HEAD -->

#### Настройка в /etc/zabbix/zabbix_agentd.conf <!-- NAME -->

```CODE
Server=IP_ZABBIX_SERVER
  ServerActive=IP_ZABBIX_SERVER
  Hostname=HOST_CLIENT
 
```

> Server(IP или hostname сервера); ServerActive(IP для активных проверок); Hostname(имя хоста как в веб-интерфейсе)

#### Перезапуск и включение службы <!-- NAME -->

```CODE
systemctl restart zabbix-agentd
  systemctl enable zabbix-agentd                                                              
                                                                                              
 
```

### Добавление хоста в веб-интерфейсе <!-- HEAD -->

#### Действия <!-- LIST -->
- Monitoring -> Hosts
- Create host
- Host name: указать как в zabbix_agentd.conf
- Templates: в поиске найти Linux by Zabbix agent
- Host groups: выбрать Discovered hosts
- Add interface: Agent
    - IP address: IP-адрес агента
    - Port: 10050
- Сохранить

> После добавления хост можно добавить в Dashboards для мониторинга
