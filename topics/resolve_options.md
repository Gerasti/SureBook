
### Настройка <!-- HEAD -->

#### Просмотр текущей конфигурации <!-- NAME -->

```CODE
cat /etc/resolv.conf                                                                     
```

> показывает текущие DNS-серверы

#### Добавление одного DNS-сервера <!-- NAME -->

```CODE
echo "nameserver 77.88.8.8" > /etc/resolv.conf                                           
```

> перезаписывает файл; 77.88.8.8(Яндекс DNS)

#### Добавление нескольких DNS-серверов <!-- NAME -->

```CODE
echo "nameserver 77.88.8.8" > /etc/resolv.conf                                           
echo "nameserver 8.8.8.8" >> /etc/resolv.conf                                               
```

> добавляет в конец файла; 8.8.8.8(Google DNS)

#### Настройка с доменом поиска <!-- NAME -->

```CODE
nameserver 192.168.1.1                                                                   
search example.local                                                                        
domain example.local                                                                        
```

> search(список доменов для поиска); domain(локальный домен)

#### Настройка с опциями <!-- NAME -->

```CODE
nameserver 77.88.8.8                                                                     
options timeout:2 attempts:3 rotate                                                         
```

> timeout(таймаут запроса в секундах); attempts(количество попыток); rotate(чередование серверов)

### Проверка DNS <!-- HEAD -->

#### Проверка разрешения имен <!-- NAME -->

```CODE
nslookup ya.ru
```

> должен вернуть IP-адрес

#### Проверка через dig(bind-utils) <!-- NAME -->

```CODE
dig ya.ru                                                                                
```

> показывает подробную информацию о DNS-запросе

#### Проверка через host <!-- NAME -->

```CODE
host ya.ru                                                                               
```

> простая проверка разрешения имени
