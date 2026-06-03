
### Импорт Docker-образов <!-- HEAD -->

#### Загрузка образа сайта <!-- NAME -->

```CODE
docker load < /mnt/docker/site_latest.tar                                                
```

> docker load(загрузка образа из tar-архива); <(перенаправление содержимого файла)

#### Загрузка образа MariaDB <!-- NAME -->

```CODE
docker load < /mnt/docker/mariadb_latest.tar                                             
```

> Загружает заранее подготовленный образ базы данных

#### Просмотр списка загруженных образов <!-- NAME -->

```CODE
docker image ls                                                                          
```

> Показывает все локально доступные Docker-образы с их тегами и ID

### Создание Docker Compose файла <!-- HEAD -->

#### Создание файла конфигурации <!-- NAME -->

```CODE
vim docker-compose.yml                                                                   
```

> docker-compose.yml(стандартное имя файла конфигурации для Docker Compose)

#### Конфигурация Docker Compose <!-- NAME -->

```CODE
 services:
  database:
    container_name: db
    image: mariadb:10.11
    restart: always

    ports:
      - "3306:3306"

    environment:
      MARIADB_DATABASE: "testdb"
      MARIADB_USER: "testc"
      MARIADB_PASSWORD: "P@ssw0rd"
      MARIADB_ROOT_PASSWORD: "toor"

  app:
    container_name: testapp
    image: site:latest
    restart: always

    ports:
      - "8080:8000"

    environment:
      DB_TYPE: "maria"
      DB_HOST: "192.168.122.97"
      DB_PORT: "3306"
      DB_NAME: "testdb"
      DB_USER: "testc"
      DB_PASS: "P@ssw0rd"

    depends_on:
      - database                                                                          
```

> services(определение сервисов для запуска); container_name(имя контейнера); image(используемый Docker-образ); restart(политика перезапуска: {always, unless-stopped, on-failure, no}); ports(проброс портов в формате "внешний:внутренний"); environment(переменные окружения для контейнера); depends_on(зависимости между контейнерами, определяет порядок запуска)

> MARIADB_DATABASE(создаёт базу данных при первом запуске); MARIADB_USER(создаёт пользователя БД); MARIADB_PASSWORD(пароль пользователя); MARIADB_ROOT_PASSWORD(пароль root-пользователя MariaDB)

> DB_TYPE(тип СУБД для подключения); DB_HOST(IP-адрес сервера базы данных); DB_PORT(порт для подключения к БД); DB_NAME(имя базы данных); DB_USER(пользователь для подключения); DB_PASS(пароль пользователя)

### Управление контейнерами <!-- HEAD -->

#### Запуск контейнеров <!-- NAME -->

```CODE
docker compose up -d                                                                     
```

> up(создать и запустить контейнеры); -d(detached mode, запуск в фоновом режиме)

#### Просмотр запущенных контейнеров <!-- NAME -->

```CODE
docker ps                                                                                
```

> Показывает список активных контейнеров с их статусом, портами и именами

#### Просмотр всех контейнеров включая остановленные <!-- NAME -->

```CODE
docker ps -a                                                                             
```

> -a(all, показать все контейнеры включая остановленные)

#### Остановка и удаление контейнеров <!-- NAME -->

```CODE
docker compose down                                                                      
```

> down(остановить и удалить контейнеры, сети, созданные через compose)

### Просмотр логов контейнеров <!-- HEAD -->

#### Логи контейнера приложения <!-- NAME -->

```CODE
docker logs testapp                                                                      
```

> Показывает все логи контейнера с момента его запуска

#### Логи контейнера базы данных <!-- NAME -->

```CODE
docker logs db                                                                           
```

> Показывает логи MariaDB для диагностики проблем с БД

#### Просмотр логов в реальном времени <!-- NAME -->

```CODE
docker logs -f testapp                                                                   
```

> -f(follow, следить за новыми записями в реальном времени)

#### Просмотр последних строк логов <!-- NAME -->

```CODE
docker logs --tail 50 testapp                                                            
```

> --tail(показать последние N строк логов)

### Проверка работы <!-- HEAD -->

#### Проверка открытых портов <!-- NAME -->

```CODE
ss -tulpn | grep -E '3306|8080'                                                          
```

> ss(socket statistics); -t(TCP-сокеты); -u(UDP-сокеты); -l(слушающие сокеты); -p(показать процессы); -n(не разрешать имена); grep(фильтр по портам 3306 и 8080)

#### Проверка сети Docker <!-- NAME -->

```CODE
docker network ls
```

> Показывает список Docker-сетей

#### Проверка доступности приложения <!-- NAME -->

```CODE
curl http://192.168.122.97:8080                                                          
```

> Проверяет HTTP-ответ от приложения

### Дополнительные команды Docker <!-- HEAD -->

#### Подключение к контейнеру <!-- NAME -->

```CODE
docker exec -it testapp bash                                                             
```

> exec(выполнить команду в контейнере); -it(интерактивный режим с TTY); bash(запустить оболочку)

#### Остановка контейнера <!-- NAME -->

```CODE
docker stop testapp
```

> Корректно останавливает контейнер с отправкой SIGTERM

#### Запуск остановленного контейнера <!-- NAME -->

```CODE
docker start testapp                                                                     
```

> Запускает ранее остановленный контейнер

#### Перезапуск контейнера <!-- NAME -->

```CODE
docker restart testapp                                                                   
```

> Перезапускает контейнер (остановка + запуск)

#### Удаление контейнера <!-- NAME -->

```CODE
docker rm testapp                                                                        
```

> Удаляет остановленный контейнер

#### Удаление образа <!-- NAME -->

```CODE
docker rmi site:latest                                                                   
```

> rmi(remove image, удалить образ); требуется отсутствие контейнеров на основе этого образа

#### Просмотр использования ресурсов <!-- NAME -->

```CODE
docker stats                                                                             
```

> Показывает использование CPU, памяти, сети и диска контейнерами в реальном времени

### Устранение типичных проблем <!-- HEAD -->

#### Проблема: контейнер не запускается <!-- NAME -->

```CODE
docker logs testapp                                                                      
docker inspect testapp                                                                      
```

> logs(просмотр логов для выявления ошибок); inspect(детальная информация о конфигурации и состоянии контейнера)

#### Проблема: порт уже занят <!-- NAME -->

```CODE
ss -tulpn | grep 8080
docker ps -a                                                                                
```

> Проверка, какой процесс занимает порт и наличие конфликтующих контейнеров

#### Проблема: приложение не подключается к БД <!-- NAME -->

```CODE
docker logs db                                                                           
docker exec -it testapp ping db                                                             
```

> Проверка логов базы данных и сетевой связности между контейнерами

#### Очистка неиспользуемых ресурсов <!-- NAME -->

```CODE
docker system prune -a                                                                   
```

> prune(удалить неиспользуемые данные); -a(all, включая неиспользуемые образы)
