
### Установка DNS-сервера <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get install bind bind-utils


```

### Настройка options.conf <!-- HEAD -->

#### Базовые параметры в /etc/bind/options.conf <!-- NAME -->

```CODE
listen-on { any; };
 allow-query { any; };
 allow-recursion { any; };
 forwarders { 77.88.8.8; };
 recursion yes;

```

> listen-on(интерфейсы); allow-query(разрешение запросов); allow-recursion(рекурсивные запросы); forwarders(DNS для пересылки); recursion(включение рекурсии)

#### Опциональная настройка slave-сервера в /etc/bind/options.conf <!-- NAME -->

```CODE
allow-transfer { 192.168.33.67; };

```

> allow-transfer(разрешение передачи зон на slave-сервер) - опционально, только если используется slave

#### Отключение логирования lame-servers в /etc/bind/options.conf <!-- NAME -->

```CODE
logging {
     category lame-servers {null;};
 };


```

### Настройка local.conf <!-- HEAD -->

#### Шаблон зоны <!-- NAME -->

```CODE
zone "ZONE_NAME" {
     type TYPE;
     file "ZONE_FILE_PATH";
 };

```

> ZONE_NAME(имя DNS-зоны); TYPE(тип зоны) {master, slave}; ZONE_FILE_PATH(путь к файлу зоны относительно /etc/bind/)

> slave опционален - используется только для вторичных DNS-серверов

#### Пример прямой зоны в /etc/bind/local.conf <!-- NAME -->

```CODE
zone "bind.domain" {
     type master;
     file "bind.domain.db";
 };


```

#### Пример обратных зон в /etc/bind/local.conf <!-- NAME -->

```CODE
zone "11.168.192.in-addr.arpa" {
     type master;
     file "11.168.192.in-addr.arpa.db";
 };


```

### Создание файлов зон <!-- HEAD -->

#### Копирование шаблонов <!-- NAME -->

```CODE
cp /etc/bind/zone/{localhost,bind.domain.db}
 cp /etc/bind/zone/127.in-addr.arpa /etc/bind/zone/11.168.192.in-addr.arpa.db
 cp /etc/bind/zone/127.in-addr.arpa /etc/bind/zone/33.168.192.in-addr.arpa.db


```

#### Назначение прав <!-- NAME -->

```CODE
chown named:named /etc/bind/zone/bind.domain.db
 chown named:named /etc/bind/zone/11.168.192.in-addr.arpa.db
 chown named:named /etc/bind/zone/33.168.192.in-addr.arpa.db


```

### Настройка зон <!-- HEAD -->

#### Содержимое прямой зоны /etc/bind/zone/bind.domain.db <!-- NAME -->

```CODE
$TTL 1d

 @       IN SOA  bind.domain. root.bind.domain. (
                 2021102900
                 12h
                 1h
                 1w
                 1h
 )

         IN NS   srv-hq.bind.domain.
         IN NS   srv-dt.bind.domain.

         IN A    192.168.11.67
 srv  IN A    192.168.11.67
 rtr  IN A    192.168.11.81
 sw   IN A    192.168.11.82

```

> SOA(главная запись зоны); NS(DNS-сервер зоны); A(соответствие домена IPv4); MX(почтовый сервер); CNAME(псевдоним); TXT(текстовые записи)

#### Содержимое обратной зоны /etc/bind/zone/11.168.192.in-addr.arpa.db <!-- NAME -->

```CODE
$TTL 1d

 @       IN SOA  bind.domain. root.bind.domain. (
                 2021102900
                 12h
                 1h
                 1w
                 1h
 )

         IN NS   bind.domain.

 81      IN PTR  rtr.bind.domain.
 67      IN PTR  srv.bind.domain.
 82      IN PTR  sw.bind.domain.


```

### Настройка resolv.conf <!-- HEAD -->

#### Содержимое /etc/net/ifaces/ens33/resolv.conf <!-- NAME -->

```CODE
search bind.domain
 nameserver 192.168.11.67
 nameserver 192.168.33.67
 nameserver 8.8.8.8

```

> nameserver(DNS-сервер); search(домен поиска по умолчанию)

#### Перезапуск сети <!-- NAME -->

```CODE
systemctl restart network


```

### Проверка конфигурации <!-- HEAD -->

#### Проверка всех зон <!-- NAME -->

```CODE
named-checkconf -z


```

#### Проверка отдельной прямой зоны <!-- NAME -->

```CODE
named-checkzone bind.domain /etc/bind/zone/bind.domain.db


```

#### Проверка отдельной обратной зоны <!-- NAME -->

```CODE
named-checkzone 11.168.192.in-addr.arpa /etc/bind/zone/11.168.192.in-addr.arpa.db


```

### Запуск BIND <!-- HEAD -->

#### Включение и запуск сервиса <!-- NAME -->

```CODE
systemctl enable --now bind
```
