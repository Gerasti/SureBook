
### Базовые команды iptables <!-- HEAD -->

#### Очистка старых правил <!-- NAME -->

```CODE
iptables -F                                                                              
iptables -t nat -F                                                                          
```

> -F(flush, очистка всех правил в цепочках); -t(указание таблицы: {filter, nat, mangle, raw}); filter(таблица по умолчанию для фильтрации пакетов); nat(таблица для трансляции адресов)

#### Сохранение правил <!-- NAME -->

```CODE
iptables-save > /etc/sysconfig/iptables
systemctl enable iptables                                                                   
```

> Без сохранения правила будут потеряны после перезагрузки

### Включение IP Forwarding <!-- HEAD -->

#### Временное включение <!-- NAME -->

```CODE
echo 1 > /proc/sys/net/ipv4/ip_forward                                                   
```

> Действует до перезагрузки системы, значение {0=отключено, 1=включено}

#### Постоянное включение в /etc/sysctl.conf <!-- NAME -->

```CODE
net.ipv4.ip_forward = 1                                                                  
```

> Параметр применится после перезагрузки или выполнения sysctl -p

#### Применение изменений <!-- NAME -->

```CODE
sysctl -p                                                                                
```

> -p(load, загрузить параметры из /etc/sysctl.conf без перезагрузки системы)

### Настройка NAT <!-- HEAD -->

#### Базовая настройка маскарадинга <!-- NAME -->

```CODE
iptables -t nat -A POSTROUTING -o ИНТЕРФЕЙС_ИНТЕРНЕТ -j MASQUERADE                       
iptables -A FORWARD -i ИНТЕРФЕЙС_ИНТЕРНЕТ -o ИНТЕРФЕЙС_ЛОКАЛЬНЫЙ -j ACCEPT                  
iptables -A FORWARD -i ИНТЕРФЕЙС_ЛОКАЛЬНЫЙ -o ИНТЕРФЕЙС_ИНТЕРНЕТ -m state --state           
ESTABLISHED,RELATED -j ACCEPT                                                               
```

> -t nat(таблица для трансляции адресов); -A(append, добавить правило в конец цепочки); POSTROUTING(цепочка для изменения пакетов после маршрутизации); -o(output interface, исходящий интерфейс); -j(jump, действие над пакетом: {ACCEPT, DROP, REJECT, MASQUERADE, SNAT, DNAT})

> MASQUERADE(подменяет внутренние IP на внешний IP маршрутизатора); FORWARD(цепочка для пересылки пакетов между интерфейсами); -i(input interface, входящий интерфейс); -m state(модуль отслеживания состояния соединений); --state(состояние: {NEW, ESTABLISHED, RELATED, INVALID}); ESTABLISHED(пакеты установленных соединений); RELATED(пакеты, связанные с установленными соединениями)

#### Безопасная настройка NAT с ограничением по сети <!-- NAME -->

```CODE
iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o ens33 -j MASQUERADE
iptables -A FORWARD -i ens33 -o ens37 -s 192.168.1.0/24 -j ACCEPT                           
```

> -s(source, ограничение по исходной сети или IP-адресу); только указанная сеть получает доступ в интернет

### Проверка правил <!-- HEAD -->

#### Просмотр текущих правил <!-- NAME -->

```CODE
iptables -L -n -v                                                                        
```

> -L(list, показать все правила); -n(numeric, вывод IP без разрешения DNS-имён); -v(verbose, подробный вывод с счётчиками пакетов и байтов)

#### Просмотр NAT-таблицы <!-- NAME -->

```CODE
iptables -t nat -L -n -v
```

> Показывает правила трансляции адресов в таблице nat
