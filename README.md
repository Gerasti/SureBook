### Содержание <!-- HEAD -->

A) [alt_fail2ban](#alt_fail2ban); [alt_samba_ADMC](#alt_samba_ADMC); [ansible](#ansible); [ansible_NextCloud](#ansible_NextCloud); [ansible_OTRS](#ansible_OTRS); [ansible_OwnCloud](#ansible_OwnCloud); [apt](#apt); [attach_samba_reserve_domain_controller](#attach_samba_reserve_domain_controller); [auto_mounting_devices](#auto_mounting_devices)

B) [base_samba-command](#base_samba-command); [bash_script_for_samba](#bash_script_for_samba); [BIND9_DLZ_samba](#BIND9_DLZ_samba); [bind_DNS](#bind_DNS); [bind_slave_DNS](#bind_slave_DNS)

C) [chrony](#chrony); [cups-pdf](#cups-pdf)

D) [dhcpd](#dhcpd); [dhcpd_failover](#dhcpd_failover); [dnsmasq](#dnsmasq)

E) [encryption_devices](#encryption_devices); [etcnet_gre_tunnel](#etcnet_gre_tunnel); [etcnet_ip](#etcnet_ip); [etcnet_ip_forward](#etcnet_ip_forward); [etcnet_vlan](#etcnet_vlan)

F) [FreeIPA](#FreeIPA); [frr_and_quagga_OSPF](#frr_and_quagga_OSPF)

G) [GOST_OpenSSL](#GOST_OpenSSL)

H) [HAProxy_balance_of_servers](#HAProxy_balance_of_servers); [hostname](#hostname)

I) [install_MariaDB_Zabbix](#install_MariaDB_Zabbix); [install_PostgreSQL_Zabbix](#install_PostgreSQL_Zabbix); [install_SSL_certificate_RedHat-like](#install_SSL_certificate_RedHat-like); [iptables_NAT](#iptables_NAT); [iptables_port_forwarding](#iptables_port_forwarding); [iscsi](#iscsi); [iscsi_attach](#iscsi_attach)

L) [logrotate](#logrotate); [LVM](#LVM)

M) [mdadm_options](#mdadm_options); [moodle](#moodle)

N) [NextCloud](#NextCloud); [NFS](#NFS); [nftables_firewall](#nftables_firewall); [nftables_NAT](#nftables_NAT); [nftables_port_forwarding](#nftables_port_forwarding); [nginx_reverse_proxy](#nginx_reverse_proxy); [nginx_server_balance](#nginx_server_balance); [nginx_Web-based_authentication](#nginx_Web-based_authentication)

O) [open-vm-tools](#open-vm-tools); [OpenSSL_certificate_center](#OpenSSL_certificate_center); [OTRS](#OTRS); [OwnCloud](#OwnCloud)

P) [partitions_of_devices](#partitions_of_devices); [phpMyAdmin](#phpMyAdmin); [PostgreSQL_base-command](#PostgreSQL_base-command)

R) [RADIUS](#RADIUS); [replication_postgresql-server](#replication_postgresql-server); [resolve_options](#resolve_options); [rsyslog](#rsyslog)

S) [SAMBA_INTERNAL_samba](#SAMBA_INTERNAL_samba); [samba_share_folder](#samba_share_folder); [SQL_install_MariaDB](#SQL_install_MariaDB); [SQL_install_MySQL](#SQL_install_MySQL); [SQL_install_PostgreSQL](#SQL_install_PostgreSQL); [squid_base_options](#squid_base_options); [SSH](#SSH); [strongswan_ipsec](#strongswan_ipsec); [sudo](#sudo); [sudo-schema-samba](#sudo-schema-samba); [systemd-timesyncd](#systemd-timesyncd); [systemd_backup](#systemd_backup)

T) [timedatectl](#timedatectl)

W) [wireguard](#wireguard)

Z) [Zabbix_agent](#Zabbix_agent); [Zabbix_web-interface](#Zabbix_web-interface)



### alt_fail2ban <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Скачивание пакетов <!-- NAME -->

```CODE
apt-get install fail2ban
```

### Преднастройка ALT Linux <!-- HEAD -->

#### Скачивание модуля python <!-- NAME -->

```CODE
apt-get install python3-module-systemd
```

#### В /etc/fail2ban/jail.conf в секции INCLUDES <!-- NAME -->

```CODE
before = paths-altlinux-systemd.conf
```

> Замена before = paths-altlinux.conf

### Настройка <!-- HEAD -->

#### Содержимое файла /etc/fail2ban/jail.d/sshd.conf <!-- NAME -->

```CODE
[sshd]
enabled = true
port = 22
maxretry = 3
bantime = 10
findtime = 60
```

> enabled(отслеживание sshd); bantime(время бана); findtime(время запоминания)

#### Запуск systemd-сервиса <!-- NAME -->

```CODE
systemctl enable --now fail2ban
```

### Проверка <!-- HEAD -->

```CODE
sudo fail2ban-client status sshd
```

> выводит забанненые адреса

### alt_samba_ADMC <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

```CODE
apt-get install -y admc
```

### Запуск <!-- HEAD -->

```CODE
admc
```

> Перед запуском нужен билет Kerberos(kinit administrator); GUI-запуск(Системные -> ADMC)

#### Настройка <!-- LIST -->
- Создание подразделения
    - нажать на домен -> папка сверху
- Создание группы
    - нажать на подразделение -> круглый значок сверху

> Область группы: Глобальная
- Создание пользователя
    - нажать на подразделение -> значок человека сверху

> Заполнить Имя, Полное имя, Имя для входа (до Windows 2000), пароль, подтвердите пароль. Параметры: Пользователь не может изменить пароль; Учётная запись отключена
- Добавление пользователя в группу
    - нажать на подразделение -> группа -> участники

### Настройка групповых политик <!-- HEAD -->

#### Установка на клиентах <!-- NAME -->

```CODE
apt-get install -y gpupdate
```

#### Включение модуля <!-- NAME -->

```CODE
gpupdate-setup enable
```

#### Установка для редактирования <!-- NAME -->

```CODE
apt-get install -y gpui
```

#### Создание политики <!-- LIST -->
- Объекты групповой политики -> нажать на домен -> Создать политику и связать с этом подразделением
    - Задать имя
- нажать на политику
- Изменить...
    - Административные шаблоны -> Настройка GNOME -> Внешний вид -> Фон рабочего стола -> Включено
    - Административные шаблоны -> Настройка GNOME -> Внешний вид -> Фон рабочего стола -> Подгонка изображения рабочего стола -> Включено
    - Административные шаблоны -> Система ALT -> Правила Polkit -> Ограничения NetworkManager(все Включено, при варианте ограничений No выставить Блокировать)

> Указать путь(локальный или сетевая папка), блокировать настройку изображения; Способ подгонки: Wallpaper

### ansible <!-- HEAD -->

[Содержание](#Содержание)

### Установка пакетов <!-- HEAD -->

```CODE
apt-get install ansible sshpass                                                          
 
```

> ansible(система управления конфигурациями); sshpass(передача паролей SSH)

### Настройка Ansible <!-- HEAD -->

#### В /etc/ansible/ansible.cfg основные параметры <!-- NAME -->

```CODE
[defaults]                                                                               
  retries = 3                                                                                 
  timeout = 10                                                                                
  inventory = /etc/ansible/inventory                                                          
 
```

> retries(количество повторов); timeout(таймаут подключения); inventory(путь к файлу инвентаря)

#### Содержимое /etc/ansible/inventory <!-- NAME -->

```CODE
[Networking] 
  hq-rtr ansible_host=192.168.24.1                                                            
  br-rtr ansible_host=192.168.2.1                                                             
                                                                                              
  [Networking:vars]                                                                           
  ansible_user=net_admin                                                                      
  ansible_password="Password"                                                                 
                                                                                              
  [Branch]                                                                                    
  hq-srv ansible_host=192.168.24.2                                                            
  hq-cli ansible_host=192.168.24.43                                                           
                                                                                              
  [Branch:vars]                                                                               
  ansible_user=sshuser                                                                        
  ansible_port=2626                                                                           
  ansible_password="P@ssw0rd"                                                                 
                                                                                              
  [all:vars]                                                                                  
  ansible_python_interpreter=/usr/bin/python3                                                 
 
```

> ansible_host(IP адрес хоста); ansible_user(пользователь для подключения); ansible_port(порт SSH); ansible_password(пароль); ansible_python_interpreter(путь к Python); ansible_ssh_private_key_file(путь к приватному SSH-ключу для аутентификации по ключам вместо пароля)

### Преднастройка управляемых хостов <!-- HEAD -->

#### Установка необходимых пакетов <!-- NAME -->

```CODE
apt-get install sudo python3 openssh                                                     
 
```

> sudo(повышение привилегий); python3(интерпретатор для Ansible); openssh(SSH сервер)

#### В /etc/openssh/sshd_config настройка SSH <!-- NAME -->

```CODE
Port 2626                                                                                
  AllowUsers sshuser                                                                          
  MaxAuthTries 2                                                                              
  PasswordAuthentication yes                                                                  
  Banner /etc/openssh/banner                                                                  
 
```

> Port(порт SSH); AllowUsers(разрешенные пользователи); MaxAuthTries(попытки аутентификации); PasswordAuthentication(аутентификация по паролю)

#### Запуск SSH сервиса <!-- NAME -->

```CODE
systemctl enable --now sshd
                                                                                              
 
```

#### Проверка доступности всех хостов <!-- NAME -->

```CODE
ansible all -m ping
 
```

> -m(модуль); ping(модуль проверки доступности); SUCCESS(успешное подключение)

### Создание Ansible Playbook <!-- HEAD -->

#### Создание playbook для инвентаризации в /etc/ansible/playbook/inventory_pc.yml <!-- NAME -->

```CODE
- name: Inventory HQ                                                                     
    hosts: Branch                                                                             
    gather_facts: yes                                                                         
    tasks:                                                                                    
      - name: Create PC-INFO                                                                  
        local_action:                                                                         
          module: file                                                                        
          path: /etc/ansible/PC-INFO                                                          
          state: directory                                                                    
          mode: '0755'
        run_once: true                                                                        
                                                                                              
      - name: Save to YAML                                                                    
        local_action:                                                                         
          module: copy                                                                        
          dest: "/etc/ansible/PC-INFO/{{ ansible_hostname }}.yml"                             
          content: |                                                                          
            computer_name: {{ ansible_hostname }}                                             
            ip_address: {{ ansible_default_ipv4.address }}                                    
 
```

> name(название задачи); hosts(группа хостов); gather_facts(сбор информации о хостах); local_action(выполнение на управляющем хосте); run_once(выполнить один раз); ansible_hostname(имя хоста); ansible_default_ipv4.address(IP-адрес)

#### Запуск playbook <!-- NAME -->

```CODE
ansible-playbook playbook/inventory_pc.yml
                                                                                              
 
```

#### Проверка созданных файлов <!-- NAME -->

```CODE
ls /etc/ansible/PC-INFO                                                                  
  cat /etc/ansible/PC-INFO/hq-cli.yml                                                         
  cat /etc/ansible/PC-INFO/hq-srv.yml                                                         
 
```

> Файлы содержат имя компьютера и IP-адрес каждого хоста

### ansible_NextCloud <!-- HEAD -->

[Содержание](#Содержание)

### Установка Ansible <!-- HEAD -->

#### Обновление и установка пакетов <!-- NAME -->

```CODE
apt-get update && apt-get install -y ansible sshpass                                             
                                                                                                      
 
```

### Создание структуры проекта <!-- HEAD -->

#### Создание директории проекта <!-- NAME -->

```CODE
mkdir ansible                                                                                    
  cd ansible      
                                                                                                      
 
```

#### Создание инвентарного файла inventory <!-- NAME -->

```CODE
vim inventory                                                                                    
                                                                                                      
 
```

#### Содержимое inventory <!-- NAME -->

```CODE
all:                                                                                             
    hosts:                                                                                            
      localhost:                                                                                      
 
```

> формат YAML; хост localhost

#### Создание директории для переменных <!-- NAME -->

```CODE
mkdir host_vars                                                                                  
                                                                                                      
 
```

#### Создание файла переменных host_vars/localhost.yml <!-- NAME -->

```CODE
vim host_vars/localhost.yml                                                                      
                                                                                                      
 
```

#### Содержимое host_vars/localhost.yml <!-- NAME -->

```CODE
ansible_ssh_user: root                                                                           
  ansible_ssh_pass: toor                                                                              
  ansible_python_interpreter: /usr/bin/python3                                                        
 
```

> ansible_ssh_user(пользователь); ansible_ssh_pass(пароль); ansible_python_interpreter(путь к Python)

### Проверка работоспособности <!-- HEAD -->

#### Проверка подключения к localhost <!-- NAME -->

```CODE
ansible -i inventory -m ping all                                                                 
 
```

> -i(инвентарный файл); -m(модуль); all(все хосты)

### Создание playbook для Nextcloud <!-- HEAD -->

#### Создание файла playbook.yml <!-- NAME -->

```CODE
vim playbook.yml                                                                                 
                                                                                                      
 
```

#### Содержимое playbook.yml <!-- NAME -->

```CODE
---                                                                                              
  - name: Install Nextcloud on ALT Server 10.1 (10.2)                                                 
    hosts: localhost                                                                                  
    become: true
                                                                                                      
    vars:                                                                                             
      mariadb_database: nextcloud                                                                     
      mariadb_username: nextcloud                                                                     
      mariadb_password: nextcloud                                                                     
      url_download_nextcloud: https://download.nextcloud.com/server/releases/latest.zip               
      dir_download_nextcloud: /tmp                                                                    
      path_project_nextcloud: /var/www/html/                                                          
      virtualhost_servername: nextcloud.test.local                                                    
                                                                                                      
    tasks:                                                                                            
      - name: Install database MariaDB                                                                
        apt_rpm:                                                                                      
          name:
            - mariadb-server                                                                          
            - python3-module-mysqlclient                                                              
          state: present                                                                              
          update_cache: true                                                                          
                                                                                                      
      - name: Started and enabled mariadb-server                                                      
        systemd:                                                                                      
          name: mariadb                                                                               
          state: started                                                                              
          enabled: true                                                                               
                                                                                                      
      - name: "Creating a database {{ mariadb_database }} for Nextcloud"                              
        mysql_db:                                                                                     
          name: "{{ mariadb_database }}"                                                              
          encoding: utf8                                                                              
          collation: utf8_unicode_ci                                                                  
          state: present                                                                              
                  
      - name: "Creating a database user {{ mariadb_username }} for Nextcloud"                         
        mysql_user:
          name: "{{ mariadb_username }}"                                                              
          password: "{{ mariadb_password }}"                                                          
          priv: "{{ mariadb_database }}.*:ALL,GRANT"                                                  
          host: localhost                                                                             
          state: present                                                                              
                                                                                                      
      - name: Install web-server Apache2 and modules                                                  
        apt_rpm:                                                                                      
          name:                                                                                       
            - apache2                                                                                 
            - apache2-mod_ssl                                                                         
            - apache2-mod_php8.2                                                                      
            - tzdata                                                                                  
          state: present                                                                              
                                                                                                      
      - name: Install PHP8.2 and php modules                                                          
        apt_rpm:  
          name:                                                                                       
            - php8.2
            - php8.2-pdo_mysql                                                                        
            - php8.2-curl                                                                             
            - php8.2-dom                                                                              
            - php8.2-ldap                                                                             
            - php8.2-exif                                                                             
            - php8.2-fileinfo                                                                         
            - php8.2-gd2                                                                              
            - php8.2-gmp                                                                              
            - php8.2-imagick                                                                          
            - php8.2-intl                                                                             
            - php8.2-libs                                                                             
            - php8.2-mbstring                                                                         
            - php8.2-memcached                                                                        
            - php8.2-opcache                                                                          
            - php8.2-openssl                                                                          
            - php8.2-pcntl                                                                            
            - php8.2-pdo                                                                              
            - php8.2-xmlreader                                                                        
            - php8.2-zip                                                                              
                                                                                                      
      - name: Enable the Apache2 module                                                               
        apache2_module:                                                                               
          name: "{{ item }}"                                                                          
          state: present                                                                              
        with_items:                                                                                   
          - dir                                                                                       
          - env                                                                                       
          - headers                                                                                   
          - mime                                                                                      
          - rewrite
                                                                                                      
      - name: Started and enabled Apache2                                                             
        systemd:                                                                                      
          name: httpd2                                                                                
          state: started
          enabled: true                                                                               
                                                                                                      
      - name: Download Nextcloud project                                                              
        get_url:                                                                                      
          url: "{{ url_download_nextcloud }}"                                                         
          dest: "{{ dir_download_nextcloud }}"                                                        
                                                                                                      
      - name: Unarchive a file project Nextcloud                                                      
        unarchive:                                                                                    
          src: "{{ dir_download_nextcloud }}/latest.zip"                                              
          dest: "{{ path_project_nextcloud }}"                                                        
                                                                                                      
      - name: Create directory "data" for Nextcloud                                                   
        file:                                                                                         
          path: "{{ path_project_nextcloud }}/nextcloud/data"                                         
          state: directory                                                                            
                                                                                                      
      - name: Assigning rights to project Nextcloud                                                   
        file:                                                                                         
          path: "{{ path_project_nextcloud }}/nextcloud/"                                             
          recurse: yes                                                                                
          owner: root                                                                                 
                                                                                                      
      - name: Assigning rights to project Nextcloud                                                   
        file:                                                                                         
          path: "{{ path_project_nextcloud }}/nextcloud/{{ item }}"                                   
          recurse: yes                                                                                
          owner: apache2
        with_items:                                                                                   
          - apps                                                                                      
          - config                                                                                    
          - data                                                                                      
                  
      - name: Setting up a web server to work with Nextcloud                                          
        copy:     
          dest: /etc/httpd2/conf/sites-available/nextcloud.conf                                       
          content: |                                                                                  
            <VirtualHost *:80>                                                                        
              DocumentRoot {{ path_project_nextcloud }}/nextcloud/                                    
              ServerName {{ virtualhost_servername }}                                                 
                                                                                                      
              <Directory {{ path_project_nextcloud }}/nextcloud/>                                     
                Require all granted                                                                   
                AllowOverride All                                                                     
                Options FollowSymLinks MultiViews                                                     
                                                                                                      
                <IfModule mod_dav.c>                                                                  
                  Dav off
                </IfModule>                                                                           
              </Directory>                                                                            
            </VirtualHost>                                                                            
                                                                                                      
      - name: Adding a symbolic link                                                                  
        command:                                                                                      
          cmd: ln -s /etc/httpd2/conf/sites-available/nextcloud.conf /etc/httpd2/conf/sites-enabled/  
                                                                                                      
      - name: Restarted Apache2                                                                       
        systemd:                                                                                      
          name: httpd2                                                                                
          state: restarted
 
```

> become(повышение привилегий); vars(переменные); apt_rpm(управление пакетами); systemd(управление сервисами); mysql_db(модуль БД); mysql_user(модуль пользователя); apache2_module(модуль Apache); get_url(загрузка файлов); unarchive(распаковка); file(управление файлами); copy(копирование); command(выполнение команд); with_items(цикл)

### Установка коллекций Ansible <!-- HEAD -->

#### Установка community.general <!-- NAME -->

```CODE
ansible-galaxy collection install community.general                                              
                                                                                                      
 
```

#### Установка community.mysql <!-- NAME -->

```CODE
ansible-galaxy collection install community.mysql                                                
 
```

> ansible-galaxy(менеджер коллекций)

### Запуск playbook <!-- HEAD -->

#### Выполнение playbook-сценария <!-- NAME -->

```CODE
ansible-playbook -i inventory playbook.yml
```

### ansible_OTRS <!-- HEAD -->

[Содержание](#Содержание)

### Установка Ansible <!-- HEAD -->

#### Обновление и установка пакетов <!-- NAME -->

```CODE
apt-get update && apt-get install -y ansible sshpass                                                  
   
 
```

### Создание структуры проекта <!-- HEAD -->

#### Создание директории проекта <!-- NAME -->

```CODE
mkdir ansible                                                                                         
  cd ansible                                                                                               
  
 
```

#### Создание инвентарного файла inventory <!-- NAME -->

```CODE
vim inventory
                                                                                                           
 
```

#### Содержимое inventory <!-- NAME -->

```CODE
all:
    hosts:                                                                                                 
      localhost:  
 
```

> формат YAML; хост localhost

#### Создание директории для переменных <!-- NAME -->

```CODE
mkdir host_vars                                                                                       
                                                                                                           
 
```

#### Создание файла переменных host_vars/localhost.yml <!-- NAME -->

```CODE
vim host_vars/localhost.yml                                                                           
                                                                                                           
 
```

#### Содержимое host_vars/localhost.yml <!-- NAME -->

```CODE
ansible_ssh_user: root                                                                                
  ansible_ssh_pass: toor                                                                                   
  ansible_python_interpreter: /usr/bin/python3                                                             
 
```

> ansible_ssh_user(пользователь); ansible_ssh_pass(пароль); ansible_python_interpreter(путь к Python)

### Проверка работоспособности <!-- HEAD -->

#### Проверка подключения к localhost <!-- NAME -->

```CODE
ansible -i inventory -m ping all                                                                      
 
```

> -i(инвентарный файл); -m(модуль); all(все хосты)

### Создание playbook для OTRS <!-- HEAD -->

#### Создание файла playbook.yml <!-- NAME -->

```CODE
vim playbook.yml                                                                                      
                                                                                                           
 
```

#### Содержимое playbook.yml <!-- NAME -->

```CODE
---                                                                                                   
  - name: Deploy Help Desk system 'OTRS' on Alt Server 10.1                                                
    hosts: localhost                                                                                       
    become: true                                                                                           
                                                                                                           
    vars:                                                                                                  
      version_postgresql: '15'                                                                             
      postgresql_init_path: /etc/init.d/postgresql                                                         
      postgresql_data_dir: /var/lib/pgsql/data                                                             
      db_name: 'otrs'                                                                                      
      db_user: 'otrs'                                                                                      
      db_pass: 'otrs'                                                                                      
                                                                                                           
    tasks:                                                                                                 
      - name: Update the package database                                                                  
        apt_rpm:                                                                                           
          update_cache: true                                                                               
                                                                                                           
      - name: Installing the necessary packages                                                            
        apt_rpm:                                                                                           
          name:                                                                                            
            - postgresql{{ version_postgresql }}-server
            - otrs                                                                                         
            - otrs-apache2
            - python3-module-psycopg2                                                                      
            - postgresql{{ version_postgresql }}-perl                                                      
            - perl-DBD-Pg                                                                                  
            - apache2-httpd-prefork                                                                        
          state: present                                                                                   
                                                                                                           
      - name: Enable daemon 'httpd2'                                                                       
        systemd:  
          name: httpd2                                                                                     
          enabled: yes                                                                                     
                                                                                                           
      - name: Check system database postgresql                                                             
        stat:     
          path: '{{ postgresql_data_dir }}/pg_hba.conf'                                                    
        register: postgres_data                                                                            
                                                                                                           
      - name: Initialize system databases                                                                  
        command:                                                                                           
          cmd: '{{ postgresql_init_path }} initdb'                                                         
        when: not postgres_data.stat.exists                                                                
                                                                                                           
      - name: Started and enabled postgresql                                                               
        systemd:                                                                                           
          name: postgresql                                                                                 
          state: started                                                                                   
          enabled: yes                                                                                     
                                                                                                           
      - name: Create PostgreSQL database                                                                   
        postgresql_db:
          name: "{{ db_name }}"                                                                            
                                                                                                           
      - name: Create PostgreSQL user                                                                       
        postgresql_user:                                                                                   
          db: "{{ db_name }}"                                                                              
          name: "{{ db_user }}"                                                                            
          password: "{{ db_pass }}"                                                                        
          priv: ALL                                                                                        
          state: present                                                                                   
                                                                                                           
      - name: Grant privileges to PostgreSQL user                                                          
        postgresql_privs:                                                                                  
          db: "{{ db_name }}"                                                                              
          privs: ALL                                                                                       
          type: database                                                                                   
          role: "{{ db_user }}"                                                                            
          state: present                                                                                   
                                                                                                           
      - name: Assign a database owner                                                                      
        postgresql_db:                                                                                     
          name: "{{ db_name }}"                                                                            
          owner: "{{ db_user }}"                                                                           
                                                                                                           
      - name: Add httpd-addon.d=yes to 999-otrs.conf                                                       
        lineinfile:                                                                                        
          path: /etc/httpd2/conf/extra-start.d/999-otrs.conf                                               
          line: 'httpd-addon.d=yes'                                                                        
          create: yes                                                                                      
                                                                                                           
      - name: Configuration httpd2                                                                         
        shell: |                                                                                           
          alternatives-manual /usr/sbin/httpd2 /usr/sbin/httpd2.prefork                                    
          alternatives-update                                                                              
          a2enextra httpd-addon.d                                                                          
                                                                                                           
      - name: Restarted httpd2                                                                             
        systemd:                                                                                           
          name: httpd2                                                                                     
          state: restarted                                                                                 
 
```

> become(повышение привилегий); vars(переменные); apt_rpm(управление пакетами); systemd(управление сервисами); stat(проверка файла); register(сохранение результата); command(выполнение команды); when(условие); postgresql_db(модуль БД PostgreSQL); postgresql_user(модуль пользователя); postgresql_privs(модуль привилегий); lineinfile(добавление строки в файл); shell(выполнение shell команд)

### Установка коллекций Ansible <!-- HEAD -->

#### Установка community.general <!-- NAME -->

```CODE
ansible-galaxy collection install community.general                                                   
                                                                                                           
 
```

#### Установка community.postgresql <!-- NAME -->

```CODE
ansible-galaxy collection install community.postgresql                                                
 
```

> ansible-galaxy(менеджер коллекций)

### Запуск playbook <!-- HEAD -->

#### Выполнение playbook-сценария <!-- NAME -->

```CODE
ansible-playbook -i inventory playbook.yml
```

### ansible_OwnCloud <!-- HEAD -->

[Содержание](#Содержание)

### Установка Ansible <!-- HEAD -->

#### Обновление и установка пакетов <!-- NAME -->

```CODE
apt-get update && apt-get install -y ansible sshpass                                                  
                                                                                                           
 
```

### Создание структуры проекта <!-- HEAD -->

#### Создание директории проекта <!-- NAME -->

```CODE
mkdir ansible                                                                                         
  cd ansible                                                                                               
                                                                                                           
 
```

#### Создание инвентарного файла inventory <!-- NAME -->

```CODE
vim inventory
                                                                                                           
 
```

#### Содержимое inventory <!-- NAME -->

```CODE
all:
    hosts:                                                                                                 
      localhost:  
 
```

> формат YAML; хост localhost

#### Создание директории для переменных <!-- NAME -->

```CODE
mkdir host_vars                                                                                       
                                                                                                           
 
```

#### Создание файла переменных host_vars/localhost.yml <!-- NAME -->

```CODE
vim host_vars/localhost.yml                                                                           
                                                                                                           
 
```

#### Содержимое host_vars/localhost.yml <!-- NAME -->

```CODE
ansible_ssh_user: root                                                                                
  ansible_ssh_pass: toor                                                                                   
  ansible_python_interpreter: /usr/bin/python3                                                             
 
```

> ansible_ssh_user(пользователь); ansible_ssh_pass(пароль); ansible_python_interpreter(путь к Python)

### Проверка работоспособности <!-- HEAD -->

#### Проверка подключения к localhost <!-- NAME -->

```CODE
ansible -i inventory -m ping all                                                                      
 
```

> -i(инвентарный файл); -m(модуль); all(все хосты)

### Создание playbook для OwnCloud <!-- HEAD -->

#### Создание файла playbook.yml <!-- NAME -->

```CODE
vim playbook.yml                                                                                      
                                                                                                           
 
```

#### Содержимое playbook.yml <!-- NAME -->

```CODE
---                                                                                                   
  - name: Install OwnCloud on ALT Server 10.1 (10.2)                                                       
    hosts: localhost                                                                                       
    become: true                                                                                           
                                                                                                           
    vars:                                                                                                  
      mariadb_database: owncloud                                                                           
      mariadb_username: owncloud                                                                           
      mariadb_password: owncloud                                                                           
      url_download_owncloud: https://download.owncloud.com/server/stable/owncloud-complete-latest.tar.bz2  
      dir_download_owncloud: /tmp                                                                          
      path_project_owncloud: /var/www/html/                                                                
      virtualhost_servername: owncloud.test.local                                                          
                                                                                                           
    tasks:                                                                                                 
      - name: Install database Mariadb                                                                     
        apt_rpm:                                                                                           
          name:                                                                                            
            - mariadb-server                                                                               
            - python3-module-mysqlclient                                                                   
          state: present                                                                                   
          update_cache: true                                                                               
                                                                                                           
      - name: Started and enabled mariadb-server                                                           
        systemd:                                                                                           
          name: mariadb                                                                                    
          state: started                                                                                   
          enabled: true                                                                                    
                                                                                                           
      - name: "Create a database {{ mariadb_database }} for OwnCloud"                                      
        mysql_db:                                                                                          
          name: "{{ mariadb_database }}"                                                                   
          encoding: utf8                                                                                   
          collation: utf8_unicode_ci                                                                       
          state: present                                                                                   
                                                                                                           
      - name: "Creating a database user {{ mariadb_username }} for OwnCloud"                               
        mysql_user:                                                                                        
          name: "{{ mariadb_username }}"                                                                   
          password: "{{ mariadb_password }}"                                                               
          priv: "{{ mariadb_database }}.*:ALL,GRANT"                                                       
          host: localhost                                                                                  
          state: present                                                                                   
                                                                                                           
      - name: Install web-server Apache2 and modules                                                       
        apt_rpm:  
          name:                                                                                            
            - apache2
            - apache2-base                                                                                 
            - apache2-httpd-prefork                                                                        
            - apache2-mod_php7                                                                             
            - apache2-mod_ssl                                                                              
          state: present                                                                                   
                                                                                                           
      - name: Install PHP7.4 and php modules                                                               
        apt_rpm:                                                                                           
          name:                                                                                            
            - php7
            - php7-curl                                                                                    
            - php7-fileinfo                                                                                
            - php7-gd                                                                                      
            - php7-intl                                                                                    
            - php7-libs                                                                                    
            - php7-mbstring                                                                                
            - php7-pdo                                                                                     
            - php7-xmlreader                                                                               
            - php7-zip                                                                                     
            - php7-mysqli                                                                                  
            - php7-pdo_mysql                                                                               
          state: present                                                                                   
                                                                                                           
      - name: Enable the Apache2 module                                                                    
        apache2_module:
          name: "{{ item }}"                                                                               
          state: present                                                                                   
        with_items:
          - rewrite                                                                                        
          - headers                                                                                        
          - env                                                                                            
          - dir                                                                                            
          - mime  
          - unique_id                                                                                      
                  
      - name: Started and enabled Apache2                                                                  
        systemd:  
          name: httpd2                                                                                     
          state: started                                                                                   
          enabled: true                                                                                    
                                                                                                           
      - name: Download OwnCloud project                                                                    
        get_url:  
          url: "{{ url_download_owncloud }}"                                                               
          dest: "{{ dir_download_owncloud }}"                                                              
                                                                                                           
      - name: Unarchive a file project OwnCloud                                                            
        unarchive:                                                                                         
          src: "{{ dir_download_owncloud }}/owncloud-complete-latest.tar.bz2"                              
          dest: "{{ path_project_owncloud }}"                                                              
                                                                                                           
      - name: Assign rights to project OwnCloud                                                            
        file:                                                                                              
          path: "{{ path_project_owncloud }}/owncloud/"                                                    
          recurse: yes                                                                                     
          owner: apache2                                                                                   
          group: apache2                                                                                   
                                                                                                           
      - name: Setting up a web server to work with OwnCloud                                                
        copy:                                                                                              
          dest: /etc/httpd2/conf/sites-available/owncloud.conf                                             
          content: |                                                                                       
            <VirtualHost *:80>                                                                             
              DocumentRoot {{ path_project_owncloud }}/owncloud/                                           
              ServerName {{ virtualhost_servername }}                                                      
                                                                                                           
              <Directory {{ path_project_owncloud }}/owncloud/>                                            
                Require all granted                                                                        
                AllowOverride All                                                                          
                Options FollowSymLinks MultiViews                                                          
                                                                                                           
                <IfModule mod_dav.c>                                                                       
                  Dav off                                                                                  
                </IfModule>                                                                                
              </Directory>                                                                                 
            </VirtualHost>                                                                                 
                                                                                                           
      - name: Adding a symbolic link                                                                       
        command:                                                                                           
          cmd: ln -s /etc/httpd2/conf/sites-available/owncloud.conf /etc/httpd2/conf/sites-enabled/        
                                                                                                           
      - name: Restarted Apache2                                                                            
        systemd:                                                                                           
          name: httpd2                                                                                     
          state: restarted                                                                                 
 
```

> become(повышение привилегий); vars(переменные); apt_rpm(управление пакетами); systemd(управление сервисами); mysql_db(модуль БД); mysql_user(модуль пользователя); apache2_module(модуль Apache); get_url(загрузка файлов); unarchive(распаковка); file(управление файлами); copy(копирование); command(выполнение команд); with_items(цикл)

### Установка коллекций Ansible <!-- HEAD -->

#### Установка community.general <!-- NAME -->

```CODE
ansible-galaxy collection install community.general                                                   
                                                                                                           
 
```

#### Установка community.mysql <!-- NAME -->

```CODE
ansible-galaxy collection install community.mysql                                                     
 
```

> ansible-galaxy(менеджер коллекций)

### Запуск playbook <!-- HEAD -->

#### Выполнение playbook-сценария <!-- NAME -->

```CODE
ansible-playbook -i inventory playbook.yml
```

### apt <!-- HEAD -->

[Содержание](#Содержание)

### Настройка <!-- HEAD -->

#### Раскомментировать строки в /etc/apt/sources.list.d/yandex.list <!-- NAME -->

```CODE
rpm [alt] http://mirror.yandex.ru/altlinux Sisyphus/x86_64 classic
rpm [alt] http://mirror.yandex.ru/altlinux Sisyphus/i586 classic
rpm [alt] http://mirror.yandex.ru/altlinux Sisyphus/noarch classic
```

> alt.list желательно весь закомментировать

#### Обновление <!-- NAME -->

```CODE
apt-get update
```

> Должен работать DNS и возможно Интернет, NAT

### attach_samba_reserve_domain_controller <!-- HEAD -->

[Содержание](#Содержание)

### Установка Samba DC <!-- HEAD -->

#### Установка пакета task-samba-dc <!-- NAME -->

```CODE
apt-get install -y task-samba-dc                                                                      
                                                                                                           
 
```

### Настройка DNS <!-- HEAD -->

#### В /etc/resolv.conf <!-- NAME -->

```CODE
search ad.team                                                                                        
  nameserver 192.168.11.67                                                                                 
  nameserver 192.168.33.67                                                                                 
  nameserver 8.8.8.8                                                                                       
 
```

> search(домен поиска); nameserver(DNS серверы)

### Настройка Kerberos <!-- HEAD -->

#### В /etc/krb5.conf <!-- NAME -->

```CODE
[libdefaults]                                                                                         
  default_realm = AD.TEAM                                                                                  
  dns_lookup_kdc = true                                                                                    
  dns_lookup_realm = false                                                                                 
                                                                                                           
  [realms]                                                                                                 
  AD.TEAM = {                                                                                              
  kdc = srv-hq.ad.team                                                                                     
  default_domain = ad.team                                                                                 
  }                                                                                                        
                                                                                                           
  [domain_realm]                                                                                           
  .ad.team = AD.TEAM
  ad.team = AD.TEAM                                                                                        
 
```

> default_realm(область по умолчанию); dns_lookup_kdc(поиск KDC через DNS); kdc(контроллер домена); domain_realm(сопоставление доменов)

### Регистрация вторичного DC в DNS <!-- HEAD -->

#### Добавление A-записи в BIND9_DLZ <!-- NAME -->

```CODE
samba-tool dns add srv-hq ad.team srv-dt A 192.168.33.67 -Uadministrator                              
 
```

> samba-tool dns add(добавление DNS записи); A(тип записи); -U(пользователь)

### Проверка подключения <!-- HEAD -->

#### Проверка разрешения имени <!-- NAME -->

```CODE
host srv-hq                                                                                           
 
```

> должен вернуть srv-hq.ad.team has address 192.168.11.67

#### Получение Kerberos билета <!-- NAME -->

```CODE
kinit administrator                                                                                   
 
```

> вводится пароль administrator@AD.TEAM

#### Проверка полученных билетов <!-- NAME -->

```CODE
klist                                                                                                 
 
```

> показывает кэш билетов и срок действия

### Присоединение к домену <!-- HEAD -->

#### Подключение как контроллер домена <!-- NAME -->

```CODE
samba-tool domain join ad.team DC -Uadministrator --realm=ad.team --workgroup=ad                      
 
```

> domain join(присоединение к домену); DC(режим контроллера домена); --realm(область Kerberos); --workgroup(рабочая группа)

#### Запуск службы Samba <!-- NAME -->

```CODE
systemctl enable --now samba
```

### auto_mounting_devices <!-- HEAD -->

[Содержание](#Содержание)

### Форматирование диска <!-- HEAD -->

#### Создание файловой системы ext4 <!-- NAME -->

```CODE
mkfs.ext4 /dev/sda                                                                                    
 
```

> создает файловую систему ext4 на устройстве /dev/sda

### Подготовка точки монтирования <!-- HEAD -->

#### Создание директории <!-- NAME -->

```CODE
mkdir -p /opt/data                                                                                    
 
```

> -p(создание родительских директорий)

### Монтирование <!-- HEAD -->

#### Монтирование диска <!-- NAME -->

```CODE
mount /dev/sda /opt/data                                                                              
 
```

> временное монтирование до перезагрузки

### Автоматическое монтирование <!-- HEAD -->

#### Добавление записи в /etc/fstab <!-- NAME -->

```CODE
/dev/sda /opt/data ext4 defaults 0 2                                                                  
 
```

> /dev/sda(устройство); /opt/data(точка монтирования); ext4(тип ФС); defaults(опции монтирования); 0(резервное копирование dump); 2(порядок проверки fsck)

### Параметры /etc/fstab <!-- HEAD -->

#### Структура записи <!-- LIST -->
- /dev/sda: устройство
- /opt/data: точка монтирования
- ext4: тип файловой системы
- defaults: обобщенные опции
    - rw(чтение-запись), suid(SUID биты), dev(файлы устройств), exec(выполнение), auto(автомонтирование), nouser(только root), async(асинхронная запись)
- 0: управление резервным копированием (dump-flag)
    - 0(не создавать резервные копии), 1(обычно root /), 2(другие разделы /home, /opt, /var)
- 2: порядок проверки файловой системы (fsck)
    - 0(не проверять), 1(первым, обычно root), 2(после root для /home, /opt, /var)

#### Применение <!-- NAME -->

```CODE
mount -a
```

> -a(монтирование всего из fstab)

### Проверка монтирования <!-- HEAD -->

#### Просмотр смонтированных разделов <!-- NAME -->

```CODE
df -h                                                                                                 
 
```

> -h(человекочитаемый формат)

### base_samba-command <!-- HEAD -->

[Содержание](#Содержание)

### Управление пользователями и группами <!-- HEAD -->

#### Создание группы <!-- NAME -->

```CODE
samba-tool group add <имя_группы>                                                                     
                                                                                                           
 
```

#### Создание пользователя <!-- NAME -->

```CODE
samba-tool user create <имя_пользователя>                                                             
                                                                                                           
 
```

#### Добавление пользователя в группу <!-- NAME -->

```CODE
samba-tool group addmembers <имя_группы> <имя_пользователя>                                           
                                                                                                           
 
```

#### Список пользователей <!-- NAME -->

```CODE
samba-tool user list                                                                                  
                                                                                                           
 
```

#### Список участников группы <!-- NAME -->

```CODE
samba-tool group listmembers <имя_группы>                                                             
                                                                                                           
 
```

### Политика паролей <!-- HEAD -->

#### Настройка сложности и длины пароля <!-- NAME -->

```CODE
samba-tool domain passwordsettings set --complexity=off                                               
  samba-tool domain passwordsettings set --min-pwd-length=1                                                
  samba-tool domain passwordsettings set --max-pwd-age=0                                                   
  samba-tool domain passwordsettings set --min-pwd-age=0                                                   
  samba-tool domain passwordsettings set --pwd-history-length=0                                            
 
```

> --complexity(сложность паролей); --min-pwd-length(минимальная длина); --max-pwd-age(срок действия пароля); --min-pwd-age(минимальный возраст пароля); --pwd-history-length(история паролей)

### Политика блокировки <!-- HEAD -->

#### Настройка блокировки учетных записей <!-- NAME -->

```CODE
samba-tool domain passwordsettings set --lockout-threshold=0                                          
  samba-tool domain passwordsettings set --lockout-duration=30                                             
  samba-tool domain passwordsettings set --reset-count=30                                                  
 
```

> --lockout-threshold(порог блокировки); --lockout-duration(длительность блокировки); --reset-count(интервал сброса счетчика)

### Kerberos-политика <!-- HEAD -->

#### Настройка времени жизни билетов <!-- NAME -->

```CODE
samba-tool domain passwordsettings set --krb-ticket-lifetime=24                                       
  samba-tool domain passwordsettings set --krb-renewal-lifetime=168                                        
 
```

> --krb-ticket-lifetime(срок жизни билета в часах); --krb-renewal-lifetime(срок обновления билета)

### Параметры учетных записей <!-- HEAD -->

#### Хранение паролей в открытом виде <!-- NAME -->

```CODE
samba-tool domain passwordsettings set --store-plaintext-password=yes                                 
  samba-tool domain passwordsettings set --allow-plaintext-password=yes                                    
 
```

> только для тестовых стендов; не рекомендуется в продакшене

### Параметры безопасности домена <!-- HEAD -->

#### Настройка криптографии <!-- NAME -->

```CODE
samba-tool domain passwordsettings set --allow-microsecond-timestamps=yes                             
  samba-tool domain passwordsettings set --allow-weak-crypto=yes                                           
 
```

> снижает безопасность; для совместимости со старыми устройствами

### Политика времени Kerberos <!-- HEAD -->

#### Настройка флагов политики <!-- NAME -->

```CODE
samba-tool domain passwordsettings set --krb-policy-flags=0x00000000                                  
                                                                                                           
 
```

### Аудит и логирование <!-- HEAD -->

#### Просмотр уровня домена <!-- NAME -->

```CODE
samba-tool domain level show                                                                          
                                                                                                           
 
```

#### Увеличение детализации логов <!-- NAME -->

```CODE
smbcontrol all debug 3                                                                                
  smbcontrol all debug 10                                                                                  
 
```

> debug 3(средний уровень); debug 10(максимальная детализация)

### Уровень функциональности домена <!-- HEAD -->

#### Просмотр уровня домена <!-- NAME -->

```CODE
samba-tool domain level show                                                                          
                                                                                                           
 
```

#### Повышение уровня домена и леса <!-- NAME -->

```CODE
samba-tool domain level raise --domain-level=2008_R2                                                  
  samba-tool domain level raise --forest-level=2008_R2                                                     
 
```

> 2008_R2(Windows Server 2008 R2)

### Проверка политики <!-- HEAD -->

#### Просмотр всех настроек политики паролей <!-- NAME -->

```CODE
samba-tool domain passwordsettings show                                                               
                                                                                                           
 
```

### Управление DNS <!-- HEAD -->

#### Добавление A-записи в DNS <!-- NAME -->

```CODE
samba-tool dns add 127.0.0.1 <домен> <имя_устройства> A <ip_адрес> -U administrator                   
 
```

> пример: samba-tool dns add 127.0.0.1 office.ssa2026.region rtr-a A 172.20.10.254 -U administrator

### Создание организационных единиц <!-- HEAD -->

#### Создание OU <!-- NAME -->

```CODE
samba-tool ou create "OU=CLI,DC=ad-team,DC=info"                                                      
                                                                                                           
 
```

### Массовое создание пользователей <!-- HEAD -->

#### Создание нескольких пользователей циклом <!-- NAME -->

```CODE
for i in {1..5}; do samba-tool user create "hq$i" "P@ssw0rd"; done                                    
                                                                                                           
 
```

#### Создание группы <!-- NAME -->

```CODE
samba-tool group add hq                                                                               
                                                                                                           
 
```

#### Массовое добавление пользователей в группу <!-- NAME -->

```CODE
for i in {1..5}; do samba-tool group addmembers hq "hq$i"; done                                       
 
```

> цикл for создает пользователей hq1, hq2, hq3, hq4, hq5 и добавляет их в группу hq

### bash_script_for_samba <!-- HEAD -->

[Содержание](#Содержание)

### Массовый импорт пользователей в Samba AD <!-- HEAD -->

#### Подготовка CSV-файла <!-- NAME -->

```CODE
First Name;Last Name;Role;Phone;OU;Street;ZIP;City;Country;Password                      
  Ivan;Ivanov;Administrator;+79990000001;IT;Lenina 1;101000;Moscow;RU;P@ssw0rd1               
  Petr;Petrov;Manager;+79990000002;Sales;Mira 10;101001;Moscow;RU;P@ssw0rd1                   
 
```

> Разделитель - точка с запятой; First Name(имя); Last Name(фамилия); Role(должность); Phone(телефон); OU(подразделение); Street(улица); ZIP(индекс); City(город); Country(страна); Password(пароль)

#### Создание скрипта импорта <!-- NAME -->

```CODE
vim import_user.sh
                                                                                              
 
```

#### Содержимое /root/import_user.sh <!-- NAME -->

```CODE
#!/bin/bash                                                                              
                                                                                              
  csv_file="$1"                                                                               
                                                                                              
  # Create OU                                                                                 
  awk -F ';' 'NR>1 {print $5}' "$csv_file" | sort | uniq | while read ou;
  do                                                                                          
      samba-tool ou add OU="$ou",DC=domain,DC=example;                                          
  done                                                                                        
                                                                                              
  # Create Users                                                                              
  while IFS=";" read -r firstName lastName role phone ou street zip city country password;
  do                                                                                          
      if [ "$firstName" == "First Name" ];
      then                                                                                    
          continue
      fi                                                                                      
                  
      username=$(echo $firstName | tr '[:upper:]' '[:lower:]' | tr -d ' '),$(echo $lastName | 
  tr '[:upper:]' '[:lower:]' | tr -d ' ')
                                                                                              
      samba-tool user add "$username" P@ssw0rd1 \                                             
      --given-name="$firstName" \
      --surname="$lastName" \                                                                 
      --telephone-number="$phone" \                                                           
      --job-title="$role" \                                                                   
      --ou="OU=$ou" \                                                                         
      --userou="OU=$ou" --noexpiry                                                            
  done < "$csv_file"                                                                          
 
```

> Скрипт автоматически создаёт OU и пользователей; username формируется как ivan,ivanov; --noexpiry(пароль не истекает)

#### Выдача прав на запуск <!-- NAME -->

```CODE
chmod +x import_user.sh
                                                                                              
 
```

### Запуск импорта <!-- HEAD -->

#### Импорт пользователей из CSV <!-- NAME -->

```CODE
./import_user.sh /mnt/Users.csv                                                          
 
```

> Запускать от root или администратора домена

### Проверка <!-- HEAD -->

#### Проверка созданных OU <!-- NAME -->

```CODE
samba-tool ou list                                                                       
                                                                                              
 
```

#### Проверка объектов внутри OU <!-- NAME -->

```CODE
samba-tool ou listobjects OU=IT                                                          
 
```

> Можно проверять любые подразделения {OU=Sales, OU=IT}

### BIND9_DLZ_samba <!-- HEAD -->

[Содержание](#Содержание)

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

### bind_DNS <!-- HEAD -->

[Содержание](#Содержание)

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

### bind_slave_DNS <!-- HEAD -->

[Содержание](#Содержание)

### Настройка slave DNS-сервера <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get update && apt-get install -y bind bind-utils                                     
                                                                                              
 
```

#### Базовые параметры в /etc/bind/options.conf <!-- NAME -->

```CODE
listen-on { any; };                                                                      
  allow-query { any; };                                                                       
  allow-transfer { none; };                                                                   
                                                                                              
 
```

#### Настройка slave-зон в /etc/bind/local.conf <!-- NAME -->

```CODE
zone "bind.domain" {                                                                     
      type slave;                                                                             
      file "slave/bind.domain";                                                               
      masters { 192.168.11.67; };                                                             
  };                                                                                          
                                                                                              
  zone "11.168.192.in-addr.arpa" {                                                            
      type slave; 
      file "slave/11.168.192.in-addr.arpa.db";                                                
      masters { 192.168.11.67; };                                                             
  };                                                                                          
                                                                                              
  zone "33.168.192.in-addr.arpa" {                                                            
      type slave;                                                                             
      file "slave/33.168.192.in-addr.arpa.db";                                                
      masters { 192.168.11.67; };                                                             
  };                                                                                          
 
```

> type slave(вторичный сервер); masters(IP master-сервера для синхронизации)

#### Содержимое /etc/net/ifaces/ens33/resolv.conf <!-- NAME -->

```CODE
search bind.domain                                                                       
  nameserver 192.168.11.67                                                                    
  nameserver 192.168.33.67                                                                    
  nameserver 8.8.8.8                                                                          
                                                                                              
 
```

#### Перезапуск сети и запуск BIND <!-- NAME -->

```CODE
systemctl restart network                                                                
  systemctl enable --now bind                                                                 
                                                                                              
 
```

#### Включение slave-режима <!-- NAME -->

```CODE
control bind-slave enabled                                                               
                                                                                              
 
```

### Проверка slave-режима <!-- HEAD -->

#### Проверка синхронизированных зон <!-- NAME -->

```CODE
ls -l /etc/bind/zone/slave/                                                              
 
```

> Должны появиться файлы зон, скопированные с master-сервера

### chrony <!-- HEAD -->

[Содержание](#Содержание)

### Установка и настройка Chrony NTP-сервера <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install -y chrony

 
```

#### Запуск службы <!-- NAME -->

```CODE
systemctl enable --now chronyd

 
```

### Настройка NTP-сервера <!-- HEAD -->

> Сервер получает время от внешнего NTP и раздаёт время клиентам

#### Отключение стандартных pool в /etc/chrony.conf <!-- NAME -->

```CODE
sed -i 's/^pool/#pool/' /etc/chrony.conf                                                 
                                                                                              
 
```

#### Добавление внешнего NTP-сервера в /etc/chrony.conf <!-- NAME -->

```CODE
server ntp2.vniiftri.ru iburst prefer minstratum 4                                       
  local stratum 5                                                                             
  allow 192.168.11.0/26                                                                       
  allow 192.168.11.64/28                                                                      
  allow 192.168.11.80/29                                                                      
  makestep 1.0 3                                                                              
 
```

> server(внешний NTP-сервер); iburst(быстрая синхронизация); prefer(предпочтительный сервер); minstratum 4(минимальный уровень источника); local stratum 5(локальный уровень сервера); allow(разрешить клиентам подключаться); makestep 1.0 3(корректировать время скачком, если расхождение больше 1 секунды, в первые 3 обновления)

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart chronyd
                                                                                              
 
```

### Разрешение NTP в firewall <!-- HEAD -->

#### Разрешение UDP 123 в iptables <!-- NAME -->

```CODE
iptables -A INPUT -p udp --dport 123 -j ACCEPT
  iptables -A OUTPUT -p udp --sport 123 -j ACCEPT                                             
 
```

> UDP порт 123 используется для NTP

#### Разрешение UDP 123 в nftables <!-- NAME -->

```CODE
nft add rule inet filter input udp dport 123 accept                                      
  nft add rule inet filter output udp sport 123 accept                                        
                                                                                              
 
```

### Проверка NTP-сервера <!-- HEAD -->

#### Проверка синхронизации <!-- NAME -->

```CODE
chronyc tracking
 
```

> Показывает текущий источник времени, stratum, смещение, стабильность

#### Проверка источников <!-- NAME -->

```CODE
chronyc sources                                                                          
 
```

> Показывает список NTP-серверов и их статус

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status chronyd                                                                 
                                                                                              
 
```

#### Проверка открытого UDP-порта 123 <!-- NAME -->

```CODE
ss -ulnp | grep 123
                                                                                              
 
```

### Настройка NTP-клиента <!-- HEAD -->

> Клиент синхронизирует время с локальным NTP-сервером

#### Установка пакета <!-- NAME -->

```CODE
apt-get install -y chrony                                                                
                                                                                              
 
```

#### Отключение стандартных pool <!-- NAME -->

```CODE
sed -i 's/^pool/#pool/' /etc/chrony.conf                                                 
                                                                                              
 
```

#### Добавление локального NTP-сервера в /etc/chrony.conf <!-- NAME -->

```CODE
echo "server 192.168.11.67 iburst" >> /etc/chrony.conf                                   
                                                                                              
 
```

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart chronyd                                                                
                                                                                              
 
```

### Проверка NTP-клиента <!-- HEAD -->

#### Проверка источников синхронизации <!-- NAME -->

```CODE
chronyc sources
 
```

> ^* означает текущий активный сервер

#### Проверка текущего времени <!-- NAME -->

```CODE
timedatectl                                                                              
                                                                                              
 
```

#### Принудительная синхронизация <!-- NAME -->

```CODE
chronyc makestep                                                                         
                                                                                              
 
```

#### Подробная статистика <!-- NAME -->

```CODE
chronyc sourcestats
```

### cups-pdf <!-- HEAD -->

[Содержание](#Содержание)

### Установка и настройка CUPS <!-- HEAD -->

#### Установка пакетов на сервере <!-- NAME -->

```CODE
apt-get install cups cups-pdf                                                            
   
 
```

### Настройка CUPS-сервера <!-- HEAD -->

#### Изменение конфигурации в /etc/cups/cupsd.conf <!-- NAME -->

```CODE
Listen *:631                                                                             
                                                                                              
  <Location />                                                                                
  Order allow,deny                                                                            
  Allow all                                                                                   
  </Location>                                                                                 
   
  <Location /admin>                                                                           
  Order allow,deny
  Allow all                                                                                   
  </Location>     
 
```

> Listen *:631(слушать порт 631 на всех интерфейсах); <Location />(доступ к основной странице); <Location /admin>(доступ к панели администратора); Allow all(разрешить всем клиентам)

> Для ограничения доступа по подсетям замените Allow all на Allow from 192.168.1.0/24

#### Запуск и включение службы <!-- NAME -->

```CODE
systemctl enable cups                                                                    
  systemctl restart cups                                                                      
                                                                                              
 
```

#### Проверка доступных принтеров <!-- NAME -->

```CODE
lpstat -p                                                                                
 
```

> Показывает список принтеров и их статус

### Подключение клиента к CUPS <!-- HEAD -->

#### Установка пакетов на клиенте <!-- NAME -->

```CODE
apt-get install cups                                                                     
                  
 
```

#### Подключение сетевого принтера <!-- NAME -->

```CODE
lpadmin -p PDF -E -v ipp://192.168.1.10:631/printers/PDF -m everywhere
 
```

> -p(имя принтера); -E(включить принтер); -v(URI принтера); -m everywhere(автоматический драйвер)

> Формат URI: ipp://IP_СЕРВЕРА:631/printers/ИМЯ_ПРИНТЕРА

#### Назначение принтера по умолчанию <!-- NAME -->

```CODE
lpoptions -d PDF                                                                         
                                                                                              
 
```

#### Проверка подключения <!-- NAME -->

```CODE
lpstat -t                                                                                
 
```

> Показывает список принтеров, очередь печати, принтер по умолчанию, состояние службы

### Работа с CUPS <!-- HEAD -->

#### Печать документа <!-- NAME -->

```CODE
echo "Тест печати" | lp -t "Example"                                                     
 
```

> lp(команда печати); -t(название задания)

#### Проверка PDF-файлов на сервере <!-- NAME -->

```CODE
ls -l /home/USERNAME/                                                                    
 
```

> При использовании cups-pdf документы сохраняются в домашнем каталоге пользователя клиента

#### Web-интерфейс <!-- NAME -->

```CODE
http://IP_СЕРВЕРА:631                                                                    
 
```

> Управление принтерами, очередью и заданиями

### Полезные команды <!-- HEAD -->

#### Просмотр очереди печати <!-- NAME -->

```CODE
lpq                                                                                      
                                                                                              
 
```

#### Отмена задания <!-- NAME -->

```CODE
cancel ID_ЗАДАНИЯ                                                                        
                                                                                              
 
```

#### Список устройств <!-- NAME -->

```CODE
lpinfo -v
```

### dhcpd <!-- HEAD -->

[Содержание](#Содержание)

### Установка DHCP-сервера <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install dhcp-server                                                              
                                                                                              
 
```

#### Определение сетевого интерфейса <!-- NAME -->

```CODE
ip a -c                                                                                  
                                                                                              
 
```

#### Настройка интерфейса в /etc/sysconfig/dhcpd <!-- NAME -->

```CODE
DHCPDARGS=ens34                                                                          
 
```

> Указывает интерфейс, который будет раздавать IP-адреса

### Настройка DHCP-сервера <!-- HEAD -->

#### Основная конфигурация в /etc/dhcp/dhcpd.conf <!-- NAME -->

```CODE
ddns-update-style none;                                                                  
                                                                                              
  subnet 192.168.11.0 netmask 255.255.255.192 {                                               
          option routers                  192.168.11.1;                                       
          option domain-name              "bind.domain";                                      
          option domain-name-servers      77.88.8.8,192.168.11.1;                             
                                                                                              
          range dynamic-bootp 192.168.11.2 192.168.11.63;                                     
          default-lease-time 21600;                                                           
          max-lease-time 43200;                                                               
                                                                                              
  host R-HQ {                                                                                 
          hardware ethernet 00:0c:29:41:f2:9f;                                                
          fixed-address 192.168.11.1;                                                         
  }                                                                                           
  }                                                                                           
 
```

> subnet(определение подсети); range(диапазон выдаваемых адресов); option routers(шлюз по умолчанию); option domain-name-servers(DNS-серверы); default-lease-time(время аренды по умолчанию в секундах); max-lease-time(максимальное время аренды); host(резервирование IP по MAC-адресу)

#### Проверка конфигурации <!-- NAME -->

```CODE
dhcpd -t -cf /etc/dhcp/dhcpd.conf
                                                                                              
 
```

#### Запуск и включение службы <!-- NAME -->

```CODE
systemctl enable --now dhcpd                                                             
                                                                                              
 
```

### Проверка DHCP-сервера <!-- HEAD -->

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status dhcpd                                                                   
                                                                                              
 
```

### Настройка DHCP-клиента <!-- HEAD -->

#### Получение IP-адреса от DHCP-сервера <!-- NAME -->

```CODE
dhcpcd                                                                                   
 
```

> Клиент получит IP-адрес, шлюз и DNS-серверы из конфигурации сервера

### dhcpd_failover <!-- HEAD -->

[Содержание](#Содержание)

### Настройка DHCP failover <!-- HEAD -->

> Failover обеспечивает отказоустойчивость DHCP: если один сервер выходит из строя, второй продолжает выдавать IP-адреса

> Общие настройки (subnets, options) выносятся в отдельные файлы и копируются на оба сервера, специфичные настройки (primary/secondary) остаются в основном файле dhcpd.conf

#### Создание директории для конфигураций на primary <!-- NAME -->

```CODE
mkdir /etc/dhcp/dhcpd.conf.d
  cat /etc/dhcp/dhcpd.conf > /etc/dhcp/dhcpd.conf.d/subnets.conf                              
                                                                                              
 
```

#### Настройка include в /etc/dhcp/dhcpd.conf на primary <!-- NAME -->

```CODE
echo include \"/etc/dhcp/dhcpd.conf.d/subnets.conf\"\; > /etc/dhcp/dhcpd.conf            
                                                                                              
 
```

#### Настройка failover primary в /etc/dhcp/dhcpd.conf <!-- NAME -->

```CODE
failover peer "dhcp-failover" {                                                          
       primary;                                                                               
       address 10.10.10.101;                                                                  
       port 519;                                                                              
       peer address 10.10.10.102;                                                             
       peer port 520;                                                                         
       max-response-delay 60;                                                                 
       max-unacked-updates 10;                                                                
       mclt 3600;                                                                             
       split 128;                                                                             
       load balance max seconds 3;                                                            
  }                                                                                           
                                                                                              
  include "/etc/dhcp/dhcpd.conf.d/subnets.conf";                                              
 
```

> primary(основной сервер); address(адрес текущего сервера); port(порт текущего сервера); peer address(адрес secondary); peer port(порт secondary); max-response-delay(секунд до признания второго сервера недоступным); max-unacked-updates(максимум пакетов bind-update); mclt(максимальное время lease без уведомления второго сервера, только на primary); split 128(распределение адресов 50/50%, только на primary); load balance max seconds(секунд ожидания ответа второго сервера)

#### Добавление failover peer в /etc/dhcp/dhcpd.conf.d/subnets.conf <!-- NAME -->

```CODE
subnet 10.10.20.0 netmask 255.255.255.0 {
    option routers 10.10.20.1;                                                                
    pool {                                                                                    
      failover peer "dhcp-failover";                                                          
      range 10.10.20.50 10.10.20.200;                                                         
    }                                                                                         
  }                                                                                           
 
```

> pool(пул адресов с failover); failover peer(указание пира для отказоустойчивости)

#### Проверка и перезапуск на primary <!-- NAME -->

```CODE
dhcpd -t -cf /etc/dhcp/dhcpd.conf                                                        
  systemctl restart dhcpd                                                                     
                                                                                              
 
```

#### Копирование конфигурации на secondary <!-- NAME -->

```CODE
scp -r /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.d root@10.10.10.102:/etc/dhcp/          
 
```

> При изменении конфигурации необходимо копировать файлы на второй сервер

#### Настройка failover secondary в /etc/dhcp/dhcpd.conf <!-- NAME -->

```CODE
failover peer "dhcp-failover" {                                                          
      secondary;                                                                              
      address 10.10.10.102;                                                                   
      port 520;                                                                               
      peer address 10.10.10.101;                                                              
      peer port 519;                                                                          
      max-response-delay 60;                                                                  
      max-unacked-updates 10;                                                                 
      load balance max seconds 3;                                                             
  }                                                                                           
                                                                                              
  include "/etc/dhcp/dhcpd.conf.d/subnets.conf";                                              
 
```

> secondary(вторичный сервер); без параметров mclt и split так как они только на primary

#### Проверка и перезапуск на secondary <!-- NAME -->

```CODE
dhcpd -t -cf /etc/dhcp/dhcpd.conf                                                        
  systemctl restart dhcpd
```

### dnsmasq <!-- HEAD -->

[Содержание](#Содержание)

### Установка и настройка dnsmasq <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install dnsmasq

 
```

#### Включение автозапуска <!-- NAME -->

```CODE
systemctl enable --now dnsmasq

 
```

### Настройка DNS в dnsmasq <!-- HEAD -->

#### Конфигурация DNS в /etc/dnsmasq.conf <!-- NAME -->

```CODE
domain=domain.example

server=/domain.example/192.168.5.2
server=77.88.8.8

interface=*

address=/hq-rtr.domain.example/192.168.1.1
ptr-record=1.1.168.192.in-addr.arpa,hq-rtr.domain.example

address=/docker.domain.example/172.16.1.1
address=/web.domain.example/172.16.2.1

address=/br-rtr.domain.example/192.168.5.1

address=/hq-srv.domain.example/192.168.1.2
ptr-record=2.1.168.192.in-addr.arpa,hq-srv.domain.example

address=/hq-cli.domain.example/192.168.5.3
ptr-record=3.5.168.192.in-addr.arpa,hq-cli.domain.example

address=/br-srv.domain.example/192.168.5.2 
 
 
```

> listen-address(IP-адреса для приёма DNS-запросов); domain(локальный домен сети); local(запрет пересылки локальной зоны во внешний DNS); cache-size(размер DNS-кэша); server(внешний DNS-сервер для пересылки); expand-hosts(использовать /etc/hosts); log-queries(логирование DNS-запросов); log-facility(файл логов)

### Типы DNS-записей в dnsmasq <!-- HEAD -->

#### A-запись в /etc/dnsmasq.conf <!-- NAME -->

```CODE
address=/host.example.com/192.168.0.10
 
```

> Соответствие доменного имени IPv4-адресу

#### AAAA-запись в /etc/dnsmasq.conf <!-- NAME -->

```CODE
address=/host.example.com/2001:db8::1
 
```

> Соответствие доменного имени IPv6-адресу

#### CNAME-запись в /etc/dnsmasq.conf <!-- NAME -->

```CODE
cname=alias.example.com,host.example.com
 
```

> Псевдоним для существующего доменного имени

#### MX-запись в /etc/dnsmasq.conf <!-- NAME -->

```CODE
mx-host=example.com,mail.example.com,10
 
```

> Почтовый сервер для домена, цифра указывает приоритет

#### TXT-запись в /etc/dnsmasq.conf <!-- NAME -->

```CODE
txt-record=example.com,"v=spf1 mx a -all"
 
```

> Текстовые записи для SPF, DMARC, верификации

#### SRV-запись в /etc/dnsmasq.conf <!-- NAME -->

```CODE
srv-host=_service._tcp.example.com,target.example.com,443,10,10
 
```

> Указание сервиса, порта и приоритета

#### PTR-запись в /etc/dnsmasq.conf <!-- NAME -->

```CODE
ptr-record=10.0.168.192.in-addr.arpa,host.example.com
 
```

> Обратное преобразование IP-адреса в доменное имя

### Настройка DHCP в dnsmasq <!-- HEAD -->

#### Конфигурация DHCP в /etc/dnsmasq.conf <!-- NAME -->

```CODE
interface=ens3
  bind-interfaces
  no-resolv
  dhcp-range=192.168.0.50,192.168.0.150,12h
  dhcp-host=ignored,192.168.1.50,ignore
  dhcp-host=aa:bb:cc:dd:ee:ff,192.168.1.51

  dhcp-option=3,192.168.0.1
  dhcp-option=6,192.168.0.1
  dhcp-option=15,no.do
 
```

> interface(интерфейс для работы DHCP); bind-interfaces(работать только на указанном интерфейсе); dhcp-range(диапазон IP-адресов и время аренды); dhcp-option=3(шлюз по умолчанию); dhcp-option=6(DNS-сервер); dhcp-option=15(доменное имя сети)

#### Дополнительные параметры в /etc/dnsmasq.conf <!-- NAME -->

```CODE
user=nobody
  group=nogroup
 
```

> user(пользователь процесса); group(группа процесса); except-interface(исключить интерфейс из работы dnsmasq); no-resolv(запрещает использовать /etc/resolv.conf); dhcp-host(исключить адрес из выдачи)

#### Применение конфигурации <!-- NAME -->

```CODE
systemctl restart dnsmasq

 
```

### Проверка dnsmasq <!-- HEAD -->

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status dnsmasq
```

### encryption_devices <!-- HEAD -->

[Содержание](#Содержание)

### Шифрование раздела с LUKS <!-- HEAD -->

#### Создание ключа шифрования <!-- NAME -->

```CODE
dd if=/dev/urandom of=/root/ext4.key bs=1024 count=4                                     
 
```

> Генерация случайного ключа размером 4 КБ

#### Шифрование раздела с указанным ключом <!-- NAME -->

```CODE
cryptsetup luksFormat /dev/data_striped/lv_data /root/ext4.key                           
 
```

> Инициализация LUKS-шифрования на разделе

#### Открытие зашифрованного раздела <!-- NAME -->

```CODE
cryptsetup luksOpen /dev/data_striped/lv_data data_crypt --key-file /root/ext4.key       
 
```

> Открывает зашифрованный раздел как /dev/mapper/data_crypt

#### Форматирование раздела <!-- NAME -->

```CODE
mkfs.ext4 /dev/mapper/data_crypt                                                         
                                                                                              
 
```

### Автоматическая разблокировка при загрузке <!-- HEAD -->

#### Настройка автоматической разблокировки в /etc/crypttab <!-- NAME -->

```CODE
data_crypt /dev/data_striped/lv_data /root/ext4.key luks                                 
 
```

> Формат: имя устройство ключ тип

#### Проверка синтаксиса <!-- NAME -->

```CODE
systemctl daemon-reexec                                                                  
  systemctl restart systemd-cryptsetup@data_crypt                                             
                                                                                              
 
```

### Монтирование раздела <!-- HEAD -->

#### Настройка автомонтирования в /etc/fstab <!-- NAME -->

```CODE
/dev/mapper/data_crypt /opt/data ext4 defaults 0 2                                       
 
```

> Формат: устройство точка_монтирования файловая_система опции dump fsck

### Защита ключа шифрования <!-- HEAD -->

#### Установка прав доступа на ключ <!-- NAME -->

```CODE
chmod 600 /root/ext4.key                                                                 
  chown root:root /root/ext4.key                                                              
 
```

> Только root может читать и записывать ключ

### Применение настроек <!-- HEAD -->

#### Перезагрузка системы <!-- NAME -->

```CODE
reboot                                                                                   
                                                                                              
 
```

#### Проверка монтирования <!-- NAME -->

```CODE
df -h                                                                                    
 
```

> Проверка, что зашифрованный раздел смонтирован

### etcnet_gre_tunnel <!-- HEAD -->

[Содержание](#Содержание)

### Настройка GRE-туннеля <!-- HEAD -->

#### Включение IP-forwarding в /etc/net/sysctl.conf <!-- NAME -->

```CODE
net.ipv4.ip_forward=1                                                                    
 
```

> Разрешает маршрутизацию пакетов между интерфейсами

#### Применение настроек sysctl <!-- NAME -->

```CODE
sysctl -p                                                                                
                                                                                              
 
```

#### Создание каталога для туннельного интерфейса <!-- NAME -->

```CODE
mkdir -p /etc/net/ifaces/tun                                                             
                                                                                              
 
```

#### Настройка параметров туннеля в /etc/net/ifaces/tun/options <!-- NAME -->

```CODE
TYPE=iptun                                                                               
  TUNTYPE=gre                                                                                 
  TUNLOCAL=172.16.4.1
  TUNREMOTE=172.16.5.1                                                                        
  TUNOPTIONS='ttl 64'                                                                         
  TUNTTL=64                                                                                   
  TUNMTU=1476                                                                                 
 
```

> TYPE=iptun(тип интерфейса - IP-туннель); TUNTYPE=gre(протокол туннелирования GRE); TUNLOCAL(локальный IP внешнего интерфейса); TUNREMOTE(удалённый IP внешнего интерфейса); TUNTTL(время жизни пакета); TUNMTU(максимальный размер пакета)

#### Настройка IP-адреса туннеля в /etc/net/ifaces/tun/ipv4address <!-- NAME -->

```CODE
10.10.10.2/30
 
```

> Внутренний IP-адрес туннеля с маской /30

#### Перезапуск сети <!-- NAME -->

```CODE
systemctl restart network                                                                
                                                                                              
 
```

> Аналогичную настройку необходимо выполнить на втором роутере с зеркальными параметрами TUNLOCAL и TUNREMOTE

### etcnet_ip <!-- HEAD -->

[Содержание](#Содержание)

### Настройка сетевых интерфейсов в ALT Linux <!-- HEAD -->

> Конфигурация интерфейсов хранится в /etc/net/ifaces/

> Рекомендуется добавлять интерфейсы по одному, чтобы избежать изменения имён

### Создание конфигурации интерфейса <!-- HEAD -->

#### Создание каталога интерфейса <!-- NAME -->

```CODE
mkdir -p /etc/net/ifaces/ens32                                                           
                                                                                              
 
```

#### Копирование конфигурации существующего интерфейса <!-- NAME -->

```CODE
cp /etc/net/ifaces/ens33/options /etc/net/ifaces/ens32/                                  
 
```

> Опционально, если уже есть настроенный интерфейс

### Настройка параметров интерфейса <!-- HEAD -->

#### Базовая конфигурация в /etc/net/ifaces/ens32/options <!-- NAME -->

```CODE
TYPE=eth                                                                                 
  BOOTPROTO=static                                                                            
  CONFIG_IPV4=yes                                                                             
 
```

> TYPE=eth(тип интерфейса Ethernet); BOOTPROTO(протокол получения IP) {static, dhcp}; CONFIG_IPV4=yes(включение IPv4)

#### Настройка IP-адреса в /etc/net/ifaces/ens32/ipv4address <!-- NAME -->

```CODE
192.168.11.67/28
  192.168.33.67/32                                                                            
 
```

> IP-адрес обязательно указывается с маской сети, можно указать несколько адресов

#### Настройка шлюза в /etc/net/ifaces/ens32/ipv4route <!-- NAME -->

```CODE
default via 192.168.11.1                                                                 
 
```

> default(маршрут по умолчанию); via(IP-адрес маршрутизатора)

#### Применение изменений <!-- NAME -->

```CODE
systemctl restart network                                                                
                                                                                              
 
```

### Ручное управление интерфейсами <!-- HEAD -->

#### Запуск интерфейса <!-- NAME -->

```CODE
ifup ens32                                                                               
                                                                                              
 
```

#### Остановка интерфейса <!-- NAME -->

```CODE
ifdown ens32                                                                             
                                                                                              
 
```

### Ручное управление маршрутами <!-- HEAD -->

#### Добавление шлюза <!-- NAME -->

```CODE
ip route add default via 192.168.11.1                                                    
                                                                                              
 
```

#### Удаление шлюза <!-- NAME -->

```CODE
ip route del default via 192.168.11.1                                                    
                                                                                              
 
```

#### Проверка маршрутов <!-- NAME -->

```CODE
ip route                                                                                 
                                                                                              
 
```

### Проверка интерфейсов <!-- HEAD -->

#### Просмотр интерфейсов <!-- NAME -->

```CODE
ip a
```

### etcnet_ip_forward <!-- HEAD -->

[Содержание](#Содержание)

### Настройка <!-- HEAD -->

#### Изменение параметра в /etc/net/sysctl.conf <!-- NAME -->

```CODE
net.ipv4.ip_forward=1                                                                    
 
```

> Разрешает маршрутизацию пакетов между интерфейсами

#### Применение изменений из файла <!-- NAME -->

```CODE
sysctl -p                                                                                
                                                                                              
 
```

#### Временное включение до перезагрузки <!-- NAME -->

```CODE
echo 1 > /proc/sys/net/ipv4/ip_forward                                                   
                                                                                              
 
```

#### Включение через sysctl напрямую <!-- NAME -->

```CODE
sysctl -w net.ipv4.ip_forward=1                                                          
 
```

> Изменения через echo и sysctl -w не сохраняются после перезагрузки

#### Проверка текущего значения <!-- NAME -->

```CODE
cat /proc/sys/net/ipv4/ip_forward                                                        
  sysctl net.ipv4.ip_forward                                                                  
 
```

> Должно вернуть 1 если включено, 0 если выключено

### etcnet_vlan <!-- HEAD -->

[Содержание](#Содержание)

### Настройка VLAN-интерфейсов <!-- HEAD -->

### Создание VLAN-интерфейса <!-- HEAD -->

#### Создание каталога VLAN-интерфейса <!-- NAME -->

```CODE
mkdir -p /etc/net/ifaces/ens32.100                                                       
 
```

> Формат: физический_интерфейс.номер_VLAN

#### Настройка параметров в /etc/net/ifaces/ens32.100/options <!-- NAME -->

```CODE
TYPE=vlan                                                                                
  CONFIG_IPV4=yes                                                                             
  BOOTPROTO=static                                                                            
  VID=100                                                                                     
  HOST=ens32                                                                                  
 
```

> TYPE=vlan(тип интерфейса VLAN); VID(идентификатор VLAN); HOST(физический интерфейс); BOOTPROTO(протокол получения IP) {static, dhcp}; HOST(для нескольких интерфейсов) 'ens32 ens33'

#### Настройка IP-адреса в /etc/net/ifaces/ens32.100/ipv4address <!-- NAME -->

```CODE
192.168.11.67/24
                                                                                              
 
```

#### Применение изменений <!-- NAME -->

```CODE
systemctl restart network                                                                
                                                                                              
 
```

### Ручное управление VLAN <!-- HEAD -->

#### Запуск VLAN-интерфейса <!-- NAME -->

```CODE
ifup ens32.100                                                                           
                                                                                              
 
```

#### Остановка VLAN-интерфейса <!-- NAME -->

```CODE
ifdown ens32.100                                                                         
                                                                                              
 
```

### Проверка VLAN <!-- HEAD -->

#### Просмотр интерфейсов <!-- NAME -->

```CODE
ip a
```

### FreeIPA <!-- HEAD -->

[Содержание](#Содержание)

### Установка FreeIPA-сервера <!-- HEAD -->

#### Установка генератора энтропии <!-- NAME -->

```CODE
apt-get update && apt-get install -y haveged                                             
                                                                                              
 
```

#### Включение и запуск haveged <!-- NAME -->

```CODE
systemctl enable --now haveged                                                           
                                                                                              
 
```

#### Установка пакета FreeIPA <!-- NAME -->

```CODE
apt-get install -y freeipa-server                                                        
                                                                                              
 
```

#### Запуск интерактивной установки <!-- NAME -->

```CODE
ipa-server-install --setup-dns                                                           
 
```

> --setup-dns опционально, если нужна интеграция с DNS

#### Параметры установки <!-- LIST -->
- Server host name: имя узла FreeIPA-сервера
- Domain name: доменное имя
- Realm name: пространство Kerberos (обычно домен в верхнем регистре)
- Directory Manager password: пароль для LDAP-администратора (минимум 8 символов)
- IPA admin password: пароль администратора FreeIPA
- NetBIOS name: имя NetBIOS
- DNS forwarders: внешние DNS-серверы (например 8.8.8.8)
- Reverse DNS zone: обратная DNS-зона

> Имена узла, домена и realm нельзя изменить после установки

### Создание пользователей и групп <!-- HEAD -->

#### Получение билета Kerberos <!-- NAME -->

```CODE
kinit admin                                                                              
 
```

> Ввести пароль администратора FreeIPA

#### Создание 30 пользователей с паролем <!-- NAME -->

```CODE
for i in {1..30}; do                                                                     
      echo "P@ssw0rd" | ipa user-add user$i --first=User --last=$i --password;                
      ipa user-mod user$i --setattr=krbPasswordExpiration=20251225011529Z;                    
  done                                                                                        
 
```

> Устанавливает срок действия пароля до 2025 года, чтобы не требовалась смена при первом входе

#### Создание групп <!-- NAME -->

```CODE
for i in {1..3}; do
      ipa group-add group$i;                                                                  
  done                                                                                        
                                                                                              
 
```

#### Добавление пользователей в группы <!-- NAME -->

```CODE
for i in {1..10}; do                                                                     
      ipa group-add-member group1 --users=user$i;                                             
  done                                                                                        
                                                                                              
  for i in {11..20}; do                                                                       
      ipa group-add-member group2 --users=user$i;
  done                                                                                        
                  
  for i in {21..30}; do                                                                       
      ipa group-add-member group3 --users=user$i;
  done                                                                                        
                                                                                              
 
```

### Подключение клиента к FreeIPA <!-- HEAD -->

#### Установка пакетов на клиенте <!-- NAME -->

```CODE
apt-get update && apt-get install -y freeipa-client zip                                  
                                                                                              
 
```

#### Запуск настройки клиента <!-- NAME -->

```CODE
ipa-client-install --server=srv-hq.your.domain --domain=your.domain --mkhomedir          
 
```

> --mkhomedir автоматически создаёт домашние каталоги для доменных пользователей

> Скрипт автоматически найдёт настройки FreeIPA-сервера и запросит имя пользователя с правом ввода машин в домен

#### Перезагрузка клиента <!-- NAME -->

```CODE
reboot       
                                                                                              
 
```

### Установка CA-сертификата на клиенте <!-- HEAD -->

#### Копирование сертификата с сервера <!-- NAME -->

```CODE
scp /etc/ipa/ca.crt root@CLI-HQ:/etc/pki/ca-trust/source/anchors/                        
 
```

> Выполняется на FreeIPA-сервере

#### Обновление доверенных сертификатов на клиенте <!-- NAME -->

```CODE
update-ca-trust                                                                          
                                                                                              
 
```

### Проверка FreeIPA <!-- HEAD -->

#### Проверка пользователя <!-- NAME -->

```CODE
ipa user-find admin                                                                      
                                                                                              
 
```

#### Проверка HTTPS-соединения <!-- NAME -->

```CODE
curl https://srv-hq.your.domain                                                          
                                                                                              
 
```

#### Проверка запущенных служб <!-- NAME -->

```CODE
ipactl status
```

### frr_and_quagga_OSPF <!-- HEAD -->

[Содержание](#Содержание)

### Установка FRR <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install frr                                                                      
   
 
```

#### Включение OSPF в /etc/frr/daemons <!-- NAME -->

```CODE
ospfd=yes    

 
```

#### Добавление в автозагрузку и запуск <!-- NAME -->

```CODE
systemctl enable --now frr
 
```

> FRR (Free Range Routing) - пакет протоколов маршрутизации; необходимо включить только нужные протоколы маршрутизации

### Установка Quagga (старая версия для ALT Linux) <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install quagga                                                                   
                                                                                              
 
```

#### Назначение прав <!-- NAME -->

```CODE
chown -R quagga:quagga /etc/quagga                                                       
                                                                                              
 
```

#### Включение и запуск служб <!-- NAME -->

```CODE
systemctl enable zebra ospfd                                                             
  systemctl start zebra ospfd                                                                 
 
```

> Важно включать и запускать службы отдельно

### Настройка OSPF <!-- HEAD -->

> Перед настройкой OSPF маршрутизаторы должны иметь IP-связность через GRE-туннели, VLAN, выделенные каналы или VPN

#### Полная конфигурация OSPF в vtysh <!-- NAME -->

```CODE
vtysh
  conf t       
  ip forwarding                                                                               
  router ospf     
      ospf router-id 1.1.1.1                                                                  
      network 10.10.10.0/30 area 0                                                            
      network 192.168.11.0/26 area 0                                                          
      network 192.168.11.65/28 area 0                                                         
      network 192.168.11.81/29 area 0                                                         
      passive-interface default                                                               
      area 0 authentication message-digest                                                    
  int tun                                                                                     
      no ip ospf passive                                                                      
      ip ospf message-digest-key 1 md5 P@ssw0rd                                               
      ip ospf network point-to-point                                                          
  int ens35                                                                                   
      no ip ospf passive                                                                      
  do wr mem                                                                                   
 
```

> router ospf(включение процесса OSPF); ospf router-id(уникальный идентификатор маршрутизатора); network(сети участвующие в OSPF); area 0(backbone area, центральная область OSPF); passive-interface default(все интерфейсы пассивны по умолчанию); no ip ospf passive(отключить пассивный режим); area 0 authentication message-digest(MD5-аутентификация для area); ip ospf message-digest-key(номер ключа, тип хеширования, пароль); ip ospf network(тип сети OSPF); do wr mem(сохранение конфигурации); пароли на обеих сторонах должны совпадать

### Типы сетей OSPF <!-- HEAD -->

> point-to-point(для 2 узлов, экономит трафик, multicast 224.0.0.5)

> broadcast(для >2 узлов, поддерживает DR/BDR, multicast 224.0.0.5 и 224.0.0.6)

### Проверка OSPF <!-- HEAD -->

#### Проверка соседей <!-- NAME -->

```CODE
show ip ospf neighbor                                                                    
 
```

> Показывает соседние маршрутизаторы, состояние соседства, Router ID

#### Проверка маршрутов <!-- NAME -->

```CODE
ip route show                                                                            
 
```

> Маршруты OSPF помечаются буквой O

#### Просмотр интерфейсов OSPF <!-- NAME -->

```CODE
show ip ospf interface                                                                   
                                                                                              
 
```

#### Просмотр конфигурации <!-- NAME -->

```CODE
show running-config
```

### GOST_OpenSSL <!-- HEAD -->

[Содержание](#Содержание)

### Настройка HTTPS с ГОСТ-сертификатами <!-- HEAD -->

> Создание собственного удостоверяющего центра (УЦ), выпуск ГОСТ-сертификатов для веб-ресурсов, настройка доверия

### Установка поддержки ГОСТ <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install -y openssl-gost-engine                                                   
                                                                                              
 
```

#### Включение поддержки ГОСТ <!-- NAME -->

```CODE
control openssl-gost enabled                                                             
                                                                                              
 
```

#### Подключение GOST к OpenSSL в /etc/openssl/openssl.cnf <!-- NAME -->

```CODE
openssl_conf = openssl_def                                                               
                                                                                              
  [openssl_def]                                                                               
  engines = engine_section                                                                    
                                                                                              
  [engine_section]                                                                            
  gost = gost_section                                                                         
                                                                                              
  [gost_section]  
  engine_id = gost                                                                            
  dynamic_path = /usr/lib64/openssl/engines-1.1/gost.so                                       
  default_algorithms = ALL                                                                    
 
```

> Необходимо для создания ключей по алгоритмам ГОСТ, выпуска сертификатов с ГОСТ-подписью, корректной работы Nginx с ГОСТ-криптографией

### Создание корневого сертификата УЦ <!-- HEAD -->

#### Создание закрытого ключа УЦ <!-- NAME -->

```CODE
openssl genpkey -algorithm gost2012_256 -pkeyopt paramset:A -out ca.key                  
                                                                                              
 
```

#### Создание самоподписанного сертификата УЦ <!-- NAME -->

```CODE
openssl req -x509 -new -key ca.key -days 365 -out ca.cer -engine gost -md_gost12_256     
 
```

> В Common Name указать IP сервера или имя корневого сервера; ca.key(закрытый ключ УЦ); ca.cer(корневой сертификат УЦ)

### Создание сертификатов для доменов <!-- HEAD -->

#### Создание закрытого ключа для домена <!-- NAME -->

```CODE
openssl genpkey -algorithm gost2012_256 -pkeyopt paramset:A -out web.some.domain.key     
  openssl genpkey -algorithm gost2012_256 -pkeyopt paramset:A -out docker.some.domain.key     
                                                                                              
 
```

#### Создание запроса на подпись (CSR) <!-- NAME -->

```CODE
openssl req -new -key web.some.domain.key -out web.some.domain.csr -engine gost          
  -md_gost12_256                                                                              
  openssl req -new -key docker.some.domain.key -out docker.some.domain.csr -engine gost
  -md_gost12_256                                                                              
 
```

> В Common Name указать IP или домен(ы), например *.some.domain

#### Подпись сертификатов УЦ <!-- NAME -->

```CODE
openssl x509 -req -in web.some.domain.csr -CA ca.cer -CAkey ca.key -CAcreateserial -out  
  web.some.domain.cer -days 365 -engine gost -md_gost12_256                                   
  openssl x509 -req -in docker.some.domain.csr -CA ca.cer -CAkey ca.key -CAcreateserial -out
  docker.some.domain.cer -days 365 -engine gost -md_gost12_256                                
                  
 
```

#### Проверка сертификата <!-- NAME -->

```CODE
openssl x509 -in web.some.domain.cer -text -noout
                                                                                              
 
```

### Установка сертификатов в систему <!-- HEAD -->

#### Копирование сертификатов в доверенные <!-- NAME -->

```CODE
cp ca.cer /etc/pki/ca-trust/source/anchors/                                              
  cp web.some.domain.cer /etc/pki/ca-trust/source/anchors/                                    
  cp docker.some.domain.cer /etc/pki/ca-trust/source/anchors/                                 
                                                                                              
 
```

#### Обновление доверенных сертификатов <!-- NAME -->

```CODE
update-ca-trust
```

### HAProxy_balance_of_servers <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install haproxy                                                                  
   
 
```

#### Включение и запуск службы <!-- NAME -->

```CODE
systemctl enable --now haproxy

 
```

### Настройка HAProxy <!-- HEAD -->

#### Конфигурация в /etc/haproxy/haproxy.cfg <!-- NAME -->

```CODE
global                                                                                   
      log /dev/log daemon                                                                     
      chroot /var/lib/haproxy                                                                 
      maxconn 4000                                                                            
      user _haproxy                                                                           
      group _haproxy                                                                          
      daemon                                                                                  
      stats socket /var/lib/haproxy/stats                                                     
                                                                                              
  defaults                                                                                    
      mode http                                                                               
      log global                                                                              
      timeout connect 10s                                                                     
      timeout client 1m                                                                       
      timeout server 1m                                                                       
                                                                                              
  listen stats                                                                                
      bind 0.0.0.0:8989
      mode http                                                                               
      stats enable
      stats uri /haproxy_stats                                                                
      stats realm HAProxy\ Statistics                                                         
      stats auth admin:toor                                                                   
      stats admin if TRUE                                                                     
                                                                                              
  frontend postgre                                                                            
      bind 0.0.0.0:5432                                                                       
      default_backend POSTGRE                                                                 
                                                                                              
  backend POSTGRE                                                                             
      balance roundrobin                                                                      
      server srv-hq 192.168.11.65:5432 check                                                  
      server srv-br 192.168.33.67:5432 check                                                  
 
```

> global(глобальные параметры); log(логирование); chroot(изоляция процесса); maxconn(максимум соединений); user/group(пользователь процесса); stats socket(сокет для статистики); defaults(параметры по умолчанию); mode(режим работы) {http, tcp}; timeout(таймауты подключения); listen stats(веб-интерфейс статистики); stats auth(логин:пароль для доступа); frontend(входящие подключения); backend(серверы назначения); balance(метод балансировки); server(адрес сервера); check(проверка доступности)

### Методы балансировки <!-- HEAD -->

> roundrobin(циклическое распределение запросов, все серверы равны)

> leastconn(запросы на сервер с наименьшим количеством соединений, для долгих соединений)

> source(один IP клиента всегда на один сервер)

> uri(одинаковые URI на один сервер, для статики и API)

> url_param(балансировка по параметру URL, например ?session_id=123)

> hdr(одинаковые HTTP-заголовки на один сервер, например User-Agent или Cookie)

> rdp-cookie(балансировка по RDP Cookie для RDP-серверов)

> random(случайный сервер, приоритет настраивается через random[start_weight])

> first(всегда первый доступный сервер, для failover)

### Проверка HAProxy <!-- HEAD -->

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status haproxy                                                                 
                                                                                              
 
```

#### Доступ к веб-статистике <!-- NAME -->

```CODE
http://IP_СЕРВЕРА:8989/haproxy_stats                                                     
 
```

> Логин и пароль из параметра stats auth

### hostname <!-- HEAD -->

[Содержание](#Содержание)

### Настройка hostname <!-- HEAD -->

#### Просмотр текущего hostname <!-- NAME -->

```CODE
hostname                                                                                 
  hostnamectl
                                                                                              
 
```

#### Временное изменение hostname до перезагрузки <!-- NAME -->

```CODE
hostname new-hostname
 
```

> Изменения не сохраняются после перезагрузки

#### Постоянное изменение hostname <!-- NAME -->

```CODE
hostnamectl set-hostname new-hostname
 
```

> Изменения сохраняются после перезагрузки

#### Изменение hostname с обновлением текущей сессии <!-- NAME -->

```CODE
hostnamectl set-hostname new-hostname; exec bash
 
```

> exec bash перезапускает оболочку без login shell

#### Изменение hostname с обновлением login shell <!-- NAME -->

```CODE
hostnamectl set-hostname new-hostname; exec bash -l                                      
 
```

> exec bash -l перезапускает оболочку как login shell, загружает профили пользователя

#### Изменение hostname в /etc/hostname <!-- NAME -->

```CODE
echo "new-hostname" > /etc/hostname                                                      
 
```

> Альтернативный способ, требует перезагрузки или применения изменений

#### Изменение hostname в /etc/hosts <!-- NAME -->

```CODE
nano /etc/hosts                                                                          
 
```

> Добавить или изменить строку

```CODE
127.0.0.1   localhost                                                                    
  127.0.1.1   new-hostname                                                                    
  192.168.1.10   new-hostname.some.domain new-hostname                                        
 
```

> Рекомендуется синхронизировать с /etc/hostname для корректной работы DNS

#### Применение изменений без перезагрузки <!-- NAME -->

```CODE
systemctl restart systemd-hostnamed                                                      
                                                                                              
 
```

### Проверка hostname <!-- HEAD -->

#### Проверка полного имени хоста <!-- NAME -->

```CODE
hostname -f                                                                              
 
```

> Показывает FQDN (Fully Qualified Domain Name)

#### Проверка короткого имени <!-- NAME -->

```CODE
hostname -s                                                                              
 
```

> Показывает короткое имя без домена

#### Проверка всех параметров <!-- NAME -->

```CODE
hostnamectl status                                                                       
 
```

> Показывает Static hostname, Icon name, Chassis, Machine ID, Boot ID, Operating System, Kernel, Architecture

### install_MariaDB_Zabbix <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get install mariadb-server zabbix-server-mysql fping                                 
   
 
```

#### Включение и запуск службы <!-- NAME -->

```CODE
systemctl enable --now mysqld

 
```

### Настройка БД <!-- HEAD -->

#### Создание базы данных и пользователя <!-- NAME -->

```CODE
mysql -uroot -p
  CREATE DATABASE zabbix CHARACTER SET utf8 COLLATE utf8_bin;
  GRANT ALL PRIVILEGES ON zabbix.* TO zabbix@localhost IDENTIFIED BY 'P@ssw0rd';              
  QUIT;                                                                                       
 
```

> Пароль можно пропустить при первом входе

#### Импорт данных в БД <!-- NAME -->

```CODE
mysql -uzabbix -pP@ssw0rd zabbix <                                                       
  /usr/share/doc/zabbix-common-database-mysql-*/schema.sql                                    
  mysql -uzabbix -pP@ssw0rd zabbix < /usr/share/doc/zabbix-common-database-mysql-*/images.sql
  mysql -uzabbix -pP@ssw0rd zabbix < /usr/share/doc/zabbix-common-database-mysql-*/data.sql   
 
```

> Важно соблюдать порядок ввода команд

### Установка веб-сервера <!-- HEAD -->

#### Установка Apache и PHP <!-- NAME -->

```CODE
apt-get install apache2 apache2-mod_php8.2                                               
  systemctl enable --now httpd2                                                               
  apt-get install php8.2 php8.2-mbstring php8.2-sockets php8.2-gd php8.2-xmlreader            
  php8.2-mysqlnd-mysqli php8.2-ldap php8.2-openssl                                            
                                                                                              
 
```

#### Настройка PHP в /etc/php/8.2/apache2-mod_php/php.ini <!-- NAME -->

```CODE
memory_limit = 256M
  post_max_size = 32M                                                                         
  max_execution_time = 600                                                                    
  max_input_time = 600                                                                        
  date.timezone = Europe/Moscow                                                               
  always_populate_raw_post_data = -1                                                          
 
```

> date.timezone указать свой регион

#### Перезапуск веб-сервера <!-- NAME -->

```CODE
systemctl restart httpd2                                                                 
                                                                                              
 
```

### Настройка сервера <!-- HEAD -->

#### В /etc/zabbix/zabbix_server.conf <!-- NAME -->

```CODE
DBHost=localhost                                                                         
  DBName=zabbix                                                                               
  DBUser=zabbix                                                                               
  DBPassword=P@ssw0rd                                                                         
                                                                                              
 
```

#### Включение и запуск службы <!-- NAME -->

```CODE
systemctl enable --now zabbix_mysql                                                      
                                                                                              
 
```

### Установка веб-интерфейса <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get install zabbix-phpfrontend-apache2 zabbix-phpfrontend-php8.2                     
                                                                                              
 
```

#### Создание символической ссылки <!-- NAME -->

```CODE
ln -s /etc/httpd2/conf/addon.d/A.zabbix.conf /etc/httpd2/conf/extra-enabled/             
                                                                                              
 
```

#### Перезапуск веб-сервера <!-- NAME -->

```CODE
systemctl restart httpd2                                                                 
                                                                                              
 
```

#### Назначение прав <!-- NAME -->

```CODE
chown apache2:apache2 /var/www/webapps/zabbix/ui/conf                                    
                                                                                              
 
```

### Доступ к веб-интерфейсу <!-- HEAD -->

#### Открыть в браузере <!-- NAME -->

```CODE
http://IP_СЕРВЕРА/zabbix                                                                 
 
```

> Подключиться к БД, ввести пароль от БД

#### Вход по умолчанию <!-- NAME -->

> Логин: Admin; Пароль: zabbix

### install_PostgreSQL_Zabbix <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get install postgresql16-server zabbix-server-pgsql fping                            
   
 
```

#### Создание системных БД и включение в автозапуск <!-- NAME -->

```CODE
/etc/init.d/postgresql initdb
  systemctl enable --now postgresql

 
```

### Настройка БД <!-- HEAD -->

#### Создание пользователя <!-- NAME -->

```CODE
su - postgres -s /bin/sh -c 'createuser --no-superuser --no-createdb --no-createrole
  --encrypted --pwprompt zabbix'                                                              
 
```

> Ввести пароль для новой роли и повторить его

#### Создание базы данных <!-- NAME -->

```CODE
su - postgres -s /bin/sh -c 'createdb -O zabbix zabbix'                                  
                                                                                              
 
```

#### Импорт данных в БД <!-- NAME -->

```CODE
su - postgres -s /bin/sh -c 'psql -U zabbix -f                                           
  /usr/share/doc/zabbix-common-database-pgsql-*/schema.sql zabbix'                            
  su - postgres -s /bin/sh -c 'psql -U zabbix -f
  /usr/share/doc/zabbix-common-database-pgsql-*/images.sql zabbix'                            
  su - postgres -s /bin/sh -c 'psql -U zabbix -f
  /usr/share/doc/zabbix-common-database-pgsql-*/data.sql zabbix'                              
 
```

> Важно соблюдать порядок ввода команд

### Установка веб-сервера <!-- HEAD -->

#### Установка Apache и PHP <!-- NAME -->

```CODE
apt-get install apache2 apache2-mod_php8.2                                               
  systemctl enable --now httpd2                                                               
  apt-get install php8.2 php8.2-mbstring php8.2-sockets php8.2-gd php8.2-xmlreader            
  php8.2-pgsql php8.2-ldap php8.2-openssl                                                     
                                                                                              
 
```

#### Настройка PHP в /etc/php/8.2/apache2-mod_php/php.ini <!-- NAME -->

```CODE
memory_limit = 256M
  post_max_size = 32M                                                                         
  max_execution_time = 600                                                                    
  max_input_time = 600                                                                        
  date.timezone = Europe/Moscow                                                               
  always_populate_raw_post_data = -1                                                          
 
```

> date.timezone указать свой регион

#### Перезапуск веб-сервера <!-- NAME -->

```CODE
systemctl restart httpd2                                                                 
                                                                                              
 
```

### Настройка сервера <!-- HEAD -->

#### В /etc/zabbix/zabbix_server.conf <!-- NAME -->

```CODE
DBHost=localhost                                                                         
  DBName=zabbix                                                                               
  DBUser=zabbix                                                                               
  DBPassword=P@ssw0rd                                                                         
                                                                                              
 
```

#### Включение и запуск службы <!-- NAME -->

```CODE
systemctl enable --now zabbix_pgsql                                                      
                                                                                              
 
```

### Установка веб-интерфейса <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get install zabbix-phpfrontend-apache2 zabbix-phpfrontend-php8.2                     
                                                                                              
 
```

#### Создание символической ссылки <!-- NAME -->

```CODE
ln -s /etc/httpd2/conf/addon.d/A.zabbix.conf /etc/httpd2/conf/extra-enabled/             
                                                                                              
 
```

#### Перезапуск веб-сервера <!-- NAME -->

```CODE
systemctl restart httpd2                                                                 
                                                                                              
 
```

#### Назначение прав <!-- NAME -->

```CODE
chown apache2:apache2 /var/www/webapps/zabbix/ui/conf                                    
                                                                                              
 
```

### Доступ к веб-интерфейсу <!-- HEAD -->

#### Открыть в браузере <!-- NAME -->

```CODE
http://IP_СЕРВЕРА/zabbix                                                                 
 
```

> Подключиться к БД, ввести пароль от БД

#### Вход по умолчанию <!-- NAME -->

> Логин: Admin; Пароль: zabbix

### install_SSL_certificate_RedHat-like <!-- HEAD -->

[Содержание](#Содержание)

### Передача сертификатов на удаленный сервер <!-- HEAD -->

#### Передача через rsync <!-- NAME -->

```CODE
rsync -avz ./ca.crt ./router.crt ./router.key USERNAME@IP_RTR:/etc/nginx/ssl/WEB.com/    
 
```

> -a(архивный режим); -v(подробный вывод); -z(сжатие при передаче)

#### Передача через scp <!-- NAME -->

```CODE
scp -P 2222 ca.crt router.crt router.key USERNAME@IP_RTR:/etc/nginx/ssl/WEB.com/         
 
```

> -P(указание порта SSH)

#### Передача через sftp <!-- NAME -->

```CODE
sftp USERNAME@IP_RTR                                                                     
  put ca.crt /etc/nginx/ssl/WEB.com/                                                          
  put router.crt /etc/nginx/ssl/WEB.com/                                                      
  put router.key /etc/nginx/ssl/WEB.com/                                                      
  exit                                                                                        
 
```

> Интерактивная передача файлов

### Установка сертификатов в систему <!-- HEAD -->

#### Переход в каталог <!-- NAME -->

```CODE
cd /etc/nginx/ssl/WEB.com/                                                               
                                                                                              
 
```

#### Копирование в доверенные сертификаты <!-- NAME -->

```CODE
cp ./* /etc/pki/ca-trust/source/anchors/                                                 
                                                                                              
 
```

#### Обновление доверенных сертификатов <!-- NAME -->

```CODE
update-ca-trust
```

### iptables_NAT <!-- HEAD -->

[Содержание](#Содержание)

### Базовые команды <!-- HEAD -->

#### Очистка старых правил <!-- NAME -->

```CODE
iptables -F                                                                              
  iptables -t nat -F                                                                          
 
```

> iptables -F(очистка таблицы filter); iptables -t nat -F(очистка таблицы nat)

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

#### Постоянное включение в /etc/sysctl.conf <!-- NAME -->

```CODE
net.ipv4.ip_forward = 1                                                                  
                                                                                              
 
```

#### Применение изменений <!-- NAME -->

```CODE
sysctl -p                                                                                
                                                                                              
 
```

### Настройка NAT <!-- HEAD -->

#### Базовая настройка маскарадинга <!-- NAME -->

```CODE
iptables -t nat -A POSTROUTING -o ИНТЕРФЕЙС_ИНТЕРНЕТ -j MASQUERADE                       
  iptables -A FORWARD -i ИНТЕРФЕЙС_ИНТЕРНЕТ -o ИНТЕРФЕЙС_ЛОКАЛЬНЫЙ -j ACCEPT                  
  iptables -A FORWARD -i ИНТЕРФЕЙС_ЛОКАЛЬНЫЙ -o ИНТЕРФЕЙС_ИНТЕРНЕТ -m state --state           
  ESTABLISHED,RELATED -j ACCEPT                                                               
 
```

> MASQUERADE(подменяет внутренние IP внешним IP маршрутизатора); FORWARD(разрешает пересылку трафика); state ESTABLISHED,RELATED(разрешает только ответы на установленные соединения)

#### Безопасная настройка NAT с ограничением по сети <!-- NAME -->

```CODE
iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o ens33 -j MASQUERADE
  iptables -A FORWARD -i ens33 -o ens37 -s 192.168.1.0/24 -j ACCEPT                           
 
```

> -s(ограничение по исходной сети); только указанная сеть получает доступ в интернет

### Проверка правил <!-- HEAD -->

#### Просмотр текущих правил <!-- NAME -->

```CODE
iptables -L -n -v                                                                        
 
```

> -L(показать правила); -n(вывод IP без DNS); -v(подробный вывод)

#### Просмотр NAT-таблицы <!-- NAME -->

```CODE
iptables -t nat -L -n -v
```

### iptables_port_forwarding <!-- HEAD -->

[Содержание](#Содержание)

### Проброс портов (Port Forwarding) <!-- HEAD -->

#### Перенаправление порта на внутренний сервер <!-- NAME -->

```CODE
iptables -t nat -A PREROUTING -p tcp -i ВНЕШНИЙ_ИНТЕРФЕЙС --dport ПОРТ_ВНЕШНИЙ -j DNAT   
  --to-destination IP_СЕРВЕРА:ПОРТ_ВНУТРЕННИЙ
  iptables -A FORWARD -p tcp -d IP_СЕРВЕРА --dport ПОРТ_ВНУТРЕННИЙ -j ACCEPT                  
 
```

> PREROUTING(обработка до маршрутизации); DNAT(изменение адреса назначения); --dport(внешний порт); --to-destination(внутренний IP:порт); FORWARD(разрешение пересылки)

#### Пример проброса SSH <!-- NAME -->

```CODE
iptables -t nat -A PREROUTING -p tcp -i ens33 --dport 2222 -j DNAT --to-destination
  192.168.1.10:22                                                                             
  iptables -A FORWARD -p tcp -d 192.168.1.10 --dport 22 -j ACCEPT
                                                                                              
 
```

#### Пример проброса HTTP <!-- NAME -->

```CODE
iptables -t nat -A PREROUTING -p tcp -i ens33 --dport 80 -j DNAT --to-destination        
  192.168.1.20:80                                                                             
  iptables -A FORWARD -p tcp -d 192.168.1.20 --dport 80 -j ACCEPT
```

### iscsi <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка пакета scsitarget-utils <!-- NAME -->

```CODE
apt-get update && apt-get install -y scsitarget-utils               
 
```

#### Включение службы tgt <!-- NAME -->

```CODE
systemctl enable --now tgt                                          
 
```

#### Просмотр списка блочных устройств <!-- NAME -->

```CODE
lsblk                                                               
 
```

> Определить диск для использования (в примере sda)

### Настройка <!-- HEAD -->

#### В /etc/tgt/targets.conf добавить в конец файла <!-- NAME -->

```CODE
<target iqn.2026-05.ru.example:storage.disk1>                       
      backing-store /dev/sda                                             
      initiator-address 192.168.20.0/24                                  
  </target>                                                              
 
```

> iqn.2026-05.ru.example:storage.disk1 - уникальный идентификатор target; backing-store - путь к диску; initiator-address - разрешенная подсеть клиентов

#### Перезапуск службы tgt <!-- NAME -->

```CODE
systemctl restart tgt                                               
                                                                         
 
```

### Проверка <!-- HEAD -->

#### Проверка target-ов <!-- NAME -->

```CODE
tgtadm --lld iscsi --op show --mode target                          
 
```

> Показывает список доступных target-ов и их параметры

### Настройка LVM <!-- HEAD -->

#### В /etc/lvm/lvm.conf в блоке devices <!-- NAME -->

```CODE
filter = [ "r|/dev/sd.*|" ]                                         
 
```

> Исключает iSCSI-диски из сканирования LVM

### Установка на клиенте <!-- HEAD -->

#### Установка пакета open-iscsi <!-- NAME -->

```CODE
apt-get update && apt-get install -y open-iscsi                     
 
```

#### Включение службы iscsid <!-- NAME -->

```CODE
systemctl enable --now iscsid                                       
                                                                         
 
```

### Настройка на клиенте <!-- HEAD -->

#### Поиск доступных target-ов <!-- NAME -->

```CODE
iscsiadm -m discovery -t sendtargets -p 192.168.20.2                
 
```

> 192.168.20.2 - IP-адрес сервера iSCSI

#### Подключение target-ов <!-- NAME -->

```CODE
iscsiadm -m node --login                                            
 
```

#### В /etc/iscsi/iscsid.conf <!-- NAME -->

```CODE
node.startup = automatic                                            
 
```

> Закомментировать node.startup = manual, раскомментировать node.startup = automatic

#### В /var/lib/iscsi/send_targets/<TargetServer>,<Port>/st_config <!-- NAME -->

```CODE
discovery.sendtargets.use_discoveryd = Yes                          
 
```

> Изменить с No на Yes

#### Перезагрузка системы <!-- NAME -->

```CODE
reboot                                                              
                                                                         
 
```

### Проверка на клиенте <!-- HEAD -->

#### Проверка подключенного диска <!-- NAME -->

```CODE
lsblk                                                               
 
```

> Должен появиться новый блочный диск (в примере 5 ГБ)

### iscsi_attach <!-- HEAD -->

[Содержание](#Содержание)

### Установка LVM <!-- HEAD -->

#### Определение диска для LVM <!-- NAME -->

```CODE
lsblk
 
```

> Определить диск для использования (в примере sdb - диск по iSCSI)

#### Пометка диска для LVM <!-- NAME -->

```CODE
pvcreate /dev/sdb                                                                 
 
```

> Инициализирует физический том для использования в LVM

#### Создание группы логических томов <!-- NAME -->

```CODE
vgcreate VG /dev/sdb                                                              
 
```

> VG - имя группы томов; /dev/sdb - физический том

### Настройка <!-- HEAD -->

#### Создание логического тома <!-- NAME -->

```CODE
lvcreate -l 100%FREE -n DATA VG                                                   
 
```

> -l 100%FREE (использовать всё свободное место); -n DATA (имя тома); VG (группа томов)

#### Форматирование в XFS <!-- NAME -->

```CODE
mkfs.xfs /dev/VG/DATA                                                             
 
```

> Создание файловой системы XFS на логическом томе

#### Создание точки монтирования <!-- NAME -->

```CODE
mkdir /opt/data                                                                   
 
```

#### В /etc/fstab добавить строку <!-- NAME -->

```CODE
/dev/VG/DATA /opt/data xfs defaults 0 0                                           
 
```

> Альтернатива: UUID=<uuid> /opt/data xfs defaults 0 0

#### Монтирование тома <!-- NAME -->

```CODE
mount -av                                                                         
 
```

> -a (монтировать всё из fstab); -v (подробный вывод)

### Проверка <!-- HEAD -->

#### Проверка логических томов <!-- NAME -->

```CODE
lvdisplay                                                                         
 
```

> Показывает информацию о логических томах

#### Проверка монтирования <!-- NAME -->

```CODE
lsblk                                                                             
 
```

> Или команда df -h для просмотра смонтированных файловых систем

### logrotate <!-- HEAD -->

[Содержание](#Содержание)

### Настройка <!-- HEAD -->

#### Содержимое файла /etc/logrotate.d/rsyslog-opt <!-- NAME -->

```CODE
/opt/*/*.log {                                                                    
      weekly                                                                           
      size 10M                                                                         
      rotate 4                                                                         
      compress                                                                         
      missingok                                                                        
      notifempty                                                                       
      create 0640 root root                                                            
      sharedscripts                                                                    
      postrotate                                                                       
          systemctl reload rsyslog > /dev/null 2>&1 || true                            
      endscript                                                                        
  }                                                                                    
 
```

> /opt/*/*.log (логи в поддиректориях /opt); weekly (ротация раз в неделю); size 10M (или при 10 МБ); rotate 4 (хранить 4 копии); compress (сжимать gzip); missingok (игнорировать отсутствие файлов); notifempty (не ротировать пустые); create 0640 root root (права нового файла); sharedscripts (скрипты один раз для группы); postrotate (команды после ротации)

#### Включение служб <!-- NAME -->

```CODE
systemctl enable --now rsyslog logrotate                                          
                                                                                       
 
```

### Настройка клиента <!-- HEAD -->

#### В /etc/rsyslog.conf добавить <!-- NAME -->

```CODE
*.warning action(type="omfwd"                                                     
      target="10.21.12.50"                                                             
      port="514"                                                                       
      protocol="tcp"                                                                   
      action.resumeRetryCount="-1"                                                     
      queue.type="linkedList"                                                          
      queue.size="10000")                                                              
 
```

> *.warning (уровень warning и выше); target (адрес syslog-сервера); port 514 (порт отправки); protocol tcp (использовать TCP); action.resumeRetryCount=-1 (бесконечные попытки переподключения); queue.type linkedList (тип очереди); queue.size 10000 (размер очереди)

#### Включение службы на клиенте <!-- NAME -->

```CODE
systemctl enable --now rsyslog
```

### LVM <!-- HEAD -->

[Содержание](#Содержание)

### Основы LVM <!-- HEAD -->

> LVM(Logical Volume Manager) - система управления логическими томами

> Основа LVM: абстракция физических дисков для гибкого управления хранилищем

> Зачем LVM: изменение размера разделов без перезагрузки, создание снапшотов, объединение дисков, миграция данных

> Преимущества: динамическое изменение размера, перемещение данных между дисками, создание резервных копий на лету

> LVM vs mdadm: LVM для гибкого управления томами, mdadm для отказоустойчивости

> LVM может striping и mirroring, но mdadm лучше для RAID (производительность, надёжность)

> Часто используют вместе: mdadm для RAID массива, затем LVM поверх для управления томами

#### Компоненты LVM <!-- LIST -->
- Physical Volume (PV)
- физический том, диск или раздел
- Volume Group (VG)
- группа томов, объединяет несколько PV
- Logical Volume (LV)
- логический том, используется как обычный раздел
- Physical Extent (PE)
- минимальная единица данных для распределения

### Установка <!-- HEAD -->

#### Установка пакета LVM <!-- NAME -->

```CODE
apt-get install -y lvm2                                                                  
 
```

> lvm2(пакет для работы с LVM)

#### Создание разметки на дисках <!-- NAME -->

```CODE
parted /dev/sda                                                                          
  mklabel gpt                                                                                 
  mkpart primary 0% 100%
  set 1 lvm on                                                                                
 
```

> set 1 lvm on(установка флага LVM на раздел)

#### Создание разметки на втором диске <!-- NAME -->

```CODE
parted /dev/sdb                                                                          
  mklabel gpt                                                                                 
  mkpart primary 0% 100%                                                                      
  set 1 lvm on                                                                                
                                                                                              
 
```

#### Создание Physical Volume <!-- NAME -->

```CODE
pvcreate /dev/sda1 /dev/sdb1                                                             
 
```

> pvcreate(инициализация физических томов для LVM)

#### Создание Volume Group <!-- NAME -->

```CODE
vgcreate vg01 /dev/sda1 /dev/sdb1                                                        
 
```

> vgcreate(создание группы томов) vg01(имя группы)

> Объединяет несколько физических томов в один пул

#### Создание Logical Volume <!-- NAME -->

```CODE
lvcreate -L 10G -n lv_data vg01                                                          
 
```

> lvcreate(создание логического тома) -L(размер) -n(имя тома)

> Альтернатива: -l 100%FREE(использовать всё свободное место)

#### Создание LV с использованием всего пространства <!-- NAME -->

```CODE
lvcreate -l 100%FREE -n lv_data vg01                                                     
 
```

> -l 100%FREE(использовать 100% свободного места в VG)

#### Создание файловой системы на LV <!-- NAME -->

```CODE
mkfs.ext4 /dev/vg01/lv_data                                                              
 
```

> Форматирование логического тома {ext4, xfs, btrfs}

#### Создание точки монтирования <!-- NAME -->

```CODE
mkdir /mnt/data                                                                          
                                                                                              
 
```

#### Монтирование LV <!-- NAME -->

```CODE
mount /dev/vg01/lv_data /mnt/data                                                        
                                                                                              
 
```

### Настройка striped (RAID 0) <!-- HEAD -->

> striped(чередование) - данные распределяются по дискам для увеличения скорости

> Требуется минимум 2 диска

#### Создание PV для striped <!-- NAME -->

```CODE
pvcreate /dev/sda1 /dev/sdb1                                                             
                                                                                              
 
```

#### Создание VG для striped <!-- NAME -->

```CODE
vgcreate vg01 /dev/sda1 /dev/sdb1                                                        
                                                                                              
 
```

#### Создание striped LV <!-- NAME -->

```CODE
lvcreate -l 100%FREE -n lv_data -i2 vg01                                                 
 
```

> -i2(количество дисков для striping, страйпинг по 2 дискам)

> Увеличивает скорость чтения/записи, но нет отказоустойчивости

#### Создание файловой системы <!-- NAME -->

```CODE
mkfs.ext4 /dev/vg01/lv_data                                                              
                                                                                              
 
```

#### Монтирование <!-- NAME -->

```CODE
mkdir /mnt/data                                                                          
  mount /dev/vg01/lv_data /mnt/data                                                           
                                                                                              
 
```

### Настройка mirroring (RAID 1) <!-- HEAD -->

> mirroring(зеркалирование) - данные дублируются на несколько дисков для отказоустойчивости

> Требуется минимум 2 диска

#### Создание PV для mirroring <!-- NAME -->

```CODE
pvcreate /dev/sda1 /dev/sdb1                                                             
                                                                                              
 
```

#### Создание VG для mirroring <!-- NAME -->

```CODE
vgcreate vg01 /dev/sda1 /dev/sdb1                                                        
                                                                                              
 
```

#### Создание mirrored LV <!-- NAME -->

```CODE
lvcreate -l 100%FREE -n lvmirror -m1 vg01                                                
 
```

> -m1(количество копий минус одна, одно зеркало = 2 копии)

> Обеспечивает отказоустойчивость, выдерживает отказ одного диска

#### Создание файловой системы <!-- NAME -->

```CODE
mkfs.ext4 /dev/vg01/lvmirror                                                             
                                                                                              
 
```

#### Монтирование <!-- NAME -->

```CODE
mkdir /mnt/mirror                                                                        
  mount /dev/vg01/lvmirror /mnt/mirror                                                        
                                                                                              
 
```

### Управление LVM <!-- HEAD -->

#### Увеличение размера LV <!-- NAME -->

```CODE
lvextend -L +5G /dev/vg01/lv_data                                                        
 
```

> -L +5G(добавить 5GB к текущему размеру)

> Изменение размера без перезагрузки и размонтирования

#### Увеличение размера файловой системы <!-- NAME -->

```CODE
resize2fs /dev/vg01/lv_data                                                              
 
```

> resize2fs(для ext4); xfs_growfs(для xfs)

> Расширяет файловую систему на весь размер LV

#### Уменьшение размера LV <!-- NAME -->

```CODE
umount /mnt/data                                                                         
  e2fsck -f /dev/vg01/lv_data                                                                 
  resize2fs /dev/vg01/lv_data 5G                                                              
  lvreduce -L 5G /dev/vg01/lv_data                                                            
  mount /dev/vg01/lv_data /mnt/data                                                           
 
```

> Сначала уменьшить ФС, потом LV; требует размонтирования

#### Добавление диска в VG <!-- NAME -->

```CODE
pvcreate /dev/sdc1                                                                       
  vgextend vg01 /dev/sdc1                                                                     
 
```

> vgextend(расширение группы томов новым диском)

#### Удаление диска из VG <!-- NAME -->

```CODE
pvmove /dev/sda1                                                                         
  vgreduce vg01 /dev/sda1                                                                     
 
```

> pvmove(перемещение данных с диска); vgreduce(удаление диска из VG)

#### Создание снапшота LV <!-- NAME -->

```CODE
lvcreate -L 1G -s -n lv_data_snap /dev/vg01/lv_data                                      
 
```

> -s(создание снапшота); -L 1G(размер для хранения изменений)

> Снапшот для резервного копирования без остановки системы

#### Восстановление из снапшота <!-- NAME -->

```CODE
lvconvert --merge /dev/vg01/lv_data_snap                                                 
 
```

> Откат LV к состоянию снапшота; требует перезагрузки или размонтирования

#### Удаление снапшота <!-- NAME -->

```CODE
lvremove /dev/vg01/lv_data_snap                                                          
                                                                                              
 
```

#### Удаление LV <!-- NAME -->

```CODE
umount /mnt/data                                                                         
  lvremove /dev/vg01/lv_data                                                                  
                                                                                              
 
```

#### Удаление VG <!-- NAME -->

```CODE
vgremove vg01                                                                            
                                                                                              
 
```

#### Удаление PV <!-- NAME -->

```CODE
pvremove /dev/sda1                                                                       
                                                                                              
 
```

### Автомонтирование <!-- HEAD -->

#### В /etc/fstab добавить строку <!-- NAME -->

```CODE
/dev/vg01/lv_data   /mnt/data   ext4   defaults   0 0                                    
 
```

> Автоматическое монтирование при загрузке

#### Применение изменений fstab без перезагрузки <!-- NAME -->

```CODE
mount -a                                                                                 
 
```

> mount -a(монтирует все из /etc/fstab, что ещё не смонтировано)

### Проверка <!-- HEAD -->

#### Просмотр Physical Volumes <!-- NAME -->

```CODE
pvdisplay                                                                                
  pvs
 
```

> pvdisplay(детальная информация); pvs(краткая таблица)

#### Просмотр Volume Groups <!-- NAME -->

```CODE
vgdisplay                                                                                
  vgs                                                                                         
 
```

> Показывает размер VG, свободное место, количество PV

#### Просмотр Logical Volumes <!-- NAME -->

```CODE
lvdisplay                                                                                
  lvs                                                                                         
 
```

> Показывает размер LV, VG, состояние

#### Просмотр всех компонентов LVM <!-- NAME -->

```CODE
lsblk                                                                                    
 
```

> Показывает иерархию дисков, разделов и LVM томов

#### Проверка монтирования <!-- NAME -->

```CODE
df -h                                                                                    
 
```

> Показывает смонтированные файловые системы и использование

#### Проверка автомонтирования после перезагрузки <!-- NAME -->

```CODE
reboot                                                                                   
  df -h                                                                                       
 
```

> Опционально, только для проверки автомонтирования после перезагрузки

> Вместо перезагрузки можно использовать mount -a

#### Проверка состояния mirrored LV <!-- NAME -->

```CODE
lvs -a -o +devices                                                                       
 
```

> Показывает устройства и состояние зеркал

#### Проверка снапшотов <!-- NAME -->

```CODE
lvs -a -o +snap_percent                                                                  
 
```

> Показывает процент использования снапшота

### mdadm_options <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка утилиты mdadm <!-- NAME -->

```CODE
apt-get install -y mdadm                                                                 
 
```

> mdadm(утилита для управления программными RAID)

> Программный RAID(реализован на уровне ОС) vs Аппаратный RAID(реализован контроллером)

> Программный RAID использует CPU, аппаратный имеет собственный процессор

#### Создание RAID 0 массива <!-- NAME -->

```CODE
mdadm --create --verbose /dev/md0 --level=0 --raid-devices=2 /dev/sdb /dev/sdc
 
```

> RAID 0(striping, чередование) - данные распределяются по дискам

> Преимущества: высокая скорость чтения/записи, полное использование объёма

> Недостатки: нет отказоустойчивости, при отказе одного диска теряются все данные

> Минимум дисков: 2; Полезный объём: сумма всех дисков

#### Создание RAID 1 массива <!-- NAME -->

```CODE
mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 /dev/sdb /dev/sdc           
 
```

> RAID 1(mirroring, зеркалирование) - данные дублируются на все диски

> Преимущества: высокая отказоустойчивость, быстрое чтение

> Недостатки: половина объёма теряется, медленная запись

> Минимум дисков: 2; Полезный объём: размер одного диска

> Выдерживает отказ N-1 дисков

#### Создание RAID 4 массива <!-- NAME -->

```CODE
mdadm --create --verbose /dev/md0 --level=4 --raid-devices=3 /dev/sdb /dev/sdc /dev/sdd  
 
```

> RAID 4(striping with dedicated parity) - выделенный диск для чётности

> Преимущества: простая реализация

> Недостатки: диск чётности - узкое место, устарел

> Минимум дисков: 3; Полезный объём: (N-1) × размер диска

> Редко используется, заменён на RAID 5

> RAID 2(bit-level striping with Hamming code) и RAID 3(byte-level striping) устарели, не поддерживаются mdadm

#### Создание RAID 5 массива <!-- NAME -->

```CODE
mdadm --create --verbose /dev/md0 --level=5 --raid-devices=3 /dev/sdb /dev/sdc /dev/sdd
 
```

> RAID 5(striping with parity) - данные и контрольные суммы распределены по дискам

> Преимущества: баланс скорости и отказоустойчивости, экономия места

> Недостатки: медленная запись из-за вычисления чётности, долгое восстановление

> Минимум дисков: 3; Полезный объём: (N-1) × размер диска

> Выдерживает отказ 1 диска

#### Создание RAID 6 массива <!-- NAME -->

```CODE
mdadm --create --verbose /dev/md0 --level=6 --raid-devices=4 /dev/sdb /dev/sdc /dev/sdd  
  /dev/sde                                                                                    
 
```

> RAID 6(striping with double parity) - двойная контрольная сумма

> Преимущества: выдерживает отказ 2 дисков одновременно

> Недостатки: ещё медленнее запись, больше потерь объёма

> Минимум дисков: 4; Полезный объём: (N-2) × размер диска

> Выдерживает отказ 2 дисков

#### Создание RAID 10 массива <!-- NAME -->

```CODE
mdadm --create --verbose /dev/md0 --level=10 --raid-devices=4 /dev/sdb /dev/sdc /dev/sdd 
  /dev/sde                                                                                    
 
```

> RAID 10(1+0, зеркалирование + чередование) - комбинация RAID 1 и RAID 0

> Преимущества: высокая скорость и отказоустойчивость

> Недостатки: половина объёма теряется, дорого

> Минимум дисков: 4; Полезный объём: 50% от суммы дисков

> Выдерживает отказ нескольких дисков (не из одной зеркальной пары)

#### Создание файловой системы на массиве <!-- NAME -->

```CODE
mkfs.ext4 /dev/md0                                                                       
 
```

> Форматирование массива {ext4, xfs, btrfs}

#### Создание точки монтирования <!-- NAME -->

```CODE
mkdir /mnt/raid                                                                          
                                                                                              
 
```

#### Монтирование массива <!-- NAME -->

```CODE
mount /dev/md0 /mnt/raid                                                                 
                                                                                              
 
```

### Настройка <!-- HEAD -->

#### В /etc/fstab добавить строку для автомонтирования <!-- NAME -->

```CODE
/dev/md0   /mnt/raid   ext4   defaults   0 0                                             
 
```

> Автоматическое монтирование при загрузке

#### Сохранение конфигурации mdadm <!-- NAME -->

```CODE
mdadm --detail --scan >> /etc/mdadm.conf                                                 
 
```

> Сохраняет информацию о массиве для автосборки при загрузке

#### Добавление spare диска в массив <!-- NAME -->

```CODE
mdadm --add /dev/md0 /dev/sde                                                            
 
```

> spare(горячий резерв) - диск автоматически заменит отказавший

#### Создание массива с spare диском <!-- NAME -->

```CODE
mdadm --create --verbose /dev/md0 --level=5 --raid-devices=3 --spare-devices=1 /dev/sdb  
  /dev/sdc /dev/sdd /dev/sde                                                                  
 
```

> --spare-devices=1(количество резервных дисков)

### Управление массивом <!-- HEAD -->

#### Остановка массива <!-- NAME -->

```CODE
mdadm --stop /dev/md0                                                                    
 
```

> Размонтировать перед остановкой

#### Запуск массива <!-- NAME -->

```CODE
mdadm --assemble /dev/md0 /dev/sdb /dev/sdc /dev/sdd                                     
                                                                                              
 
```

#### Удаление диска из массива <!-- NAME -->

```CODE
mdadm --remove /dev/md0 /dev/sdc                                                         
 
```

> Диск должен быть помечен как failed

#### Пометка диска как отказавшего <!-- NAME -->

```CODE
mdadm --fail /dev/md0 /dev/sdc                                                           
 
```

> Имитация отказа диска для тестирования

#### Добавление нового диска взамен отказавшего <!-- NAME -->

```CODE
mdadm --add /dev/md0 /dev/sde
 
```

> Автоматически начнётся rebuild (восстановление)

#### Увеличение количества дисков в массиве <!-- NAME -->

```CODE
mdadm --grow /dev/md0 --raid-devices=4 --add /dev/sde                                    
 
```

> Расширение массива с пересчётом данных

#### Изменение уровня RAID <!-- NAME -->

```CODE
mdadm --grow /dev/md0 --level=6                                                          
 
```

> Преобразование RAID 5 в RAID 6 (требует время)

### Проверка <!-- HEAD -->

#### Проверка состояния всех RAID массивов <!-- NAME -->

```CODE
cat /proc/mdstat                                                                         
 
```

> Краткая информация: состояние, прогресс rebuild/resync

#### Детальная информация о массиве <!-- NAME -->

```CODE
mdadm --detail /dev/md0                                                                  
 
```

> Показывает уровень RAID, состояние дисков, размер, UUID

#### Проверка информации о диске в массиве <!-- NAME -->

```CODE
mdadm --examine /dev/sdb                                                                 
 
```

> Показывает метаданные RAID на конкретном диске

#### Мониторинг состояния массива <!-- NAME -->

```CODE
mdadm --monitor --scan --daemonise                                                       
 
```

> Запуск демона мониторинга для уведомлений об ошибках

#### Проверка скорости rebuild <!-- NAME -->

```CODE
cat /proc/sys/dev/raid/speed_limit_min                                                   
  cat /proc/sys/dev/raid/speed_limit_max                                                      
 
```

> Показывает минимальную и максимальную скорость восстановления

#### Изменение скорости rebuild <!-- NAME -->

```CODE
echo 50000 > /proc/sys/dev/raid/speed_limit_min                                          
  echo 200000 > /proc/sys/dev/raid/speed_limit_max                                            
 
```

> Значения в KB/s, влияет на производительность системы

#### Проверка целостности массива <!-- NAME -->

```CODE
echo check > /sys/block/md0/md/sync_action                                               
 
```

> Запуск проверки без исправления ошибок

#### Восстановление с исправлением ошибок <!-- NAME -->

```CODE
echo repair > /sys/block/md0/md/sync_action                                              
 
```

> Проверка и исправление несоответствий

#### Просмотр прогресса проверки <!-- NAME -->

```CODE
cat /proc/mdstat                                                                         
 
```

> Показывает прогресс операции check/repair

### Удаление <!-- HEAD -->

#### Размонтирование массива <!-- NAME -->

```CODE
umount /mnt/raid                                                                         
                                                                                              
 
```

#### Остановка массива <!-- NAME -->

```CODE
mdadm --stop /dev/md0                                                                    
                                                                                              
 
```

#### Удаление метаданных RAID с дисков <!-- NAME -->

```CODE
mdadm --zero-superblock /dev/sdb /dev/sdc /dev/sdd                                       
 
```

> Полное удаление информации о RAID с дисков

#### Удаление записи из /etc/fstab <!-- NAME -->

```CODE
sed -i '/\/dev\/md0/d' /etc/fstab                                                        
 
```

> Удаление строки автомонтирования

#### Удаление записи из /etc/mdadm.conf <!-- NAME -->

```CODE
sed -i '/\/dev\/md0/d' /etc/mdadm.conf                                                   
 
```

> Удаление конфигурации массива

### moodle <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка MariaDB <!-- NAME -->

```CODE
apt-get update && apt-get install -y mariadb-server                               
 
```

#### Включение службы MariaDB <!-- NAME -->

```CODE
systemctl enable --now mariadb                                                    
 
```

#### Создание базы данных и пользователя <!-- NAME -->

```CODE
mariadb                                                                           
  CREATE DATABASE moodle;                                                              
  CREATE USER 'moodle'@'localhost' IDENTIFIED BY 'moodle';                             
  GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,CREATE TEMPORARY TABLES,DROP,INDEX,ALTER ON 
  moodle.* TO 'moodle'@'localhost';                                                    
 
```

> Создание БД moodle, пользователя moodle с паролем moodle и выдача необходимых прав

#### Установка Apache2 <!-- NAME -->

```CODE
apt-get install -y apache2 apache2-{base,httpd-prefork,mod_php8.0,mods}           
 
```

#### Установка PHP и модулей <!-- NAME -->

```CODE
apt-get install -y php8.0 php8.0-{curl,fileinfo,fpm-fcgi,gd,intl,ldap,mbstring,mys
  qlnd,mysqlnd-mysqli,opcache,soap,sodium,xmlreader,xmlrpc,zip,openssl}                
 
```

#### Запуск веб-сервера <!-- NAME -->

```CODE
systemctl enable --now httpd2                                                     
 
```

#### Установка git <!-- NAME -->

```CODE
apt-get install -y git                                                            
 
```

#### Загрузка Moodle <!-- NAME -->

```CODE
git clone git://git.moodle.org/moodle.git                                         
  cd moodle                                                                            
 
```

#### Просмотр доступных веток <!-- NAME -->

```CODE
git branch -a                                                                     
 
```

#### Выбор версии Moodle <!-- NAME -->

```CODE
git branch --track MOODLE_403_STABLE origin/MOODLE_403_STABLE                     
  git checkout MOODLE_403_STABLE                                                       
 
```

> Переключение на стабильную ветку 4.03

#### Копирование в веб-каталог <!-- NAME -->

```CODE
cd ../                                                                            
  cp -R moodle /var/www/html/                                                          
 
```

#### Создание каталога данных <!-- NAME -->

```CODE
mkdir /var/moodledata                                                             
  chown -R apache2 /var/moodledata                                                     
  chmod -R 777 /var/moodledata                                                         
  chmod -R 0755 /var/www/html/moodle                                                   
  chown -R apache2:apache2 /var/www/html/moodle                                        
                                                                                       
 
```

### Настройка <!-- HEAD -->

#### Содержимое файла /etc/httpd2/conf/sites-available/moodle.conf <!-- NAME -->

```CODE
<VirtualHost *:80>                                                                
      ServerName moodle.champ.first                                                    
      DocumentRoot /var/www/html/moodle                                                
      <Directory "/var/www/html/moodle">                                               
          AllowOverride All                                                            
          Options -Indexes +FollowSymLinks                                             
      </Directory>                                                                     
  </VirtualHost>                                                                       
 
```

> ServerName (доменное имя); DocumentRoot (путь к Moodle)

#### Активация конфигурации <!-- NAME -->

```CODE
ln -s /etc/httpd2/conf/sites-available/moodle.conf /etc/httpd2/conf/sites-enabled/
 
```

#### Настройка PHP <!-- NAME -->

```CODE
sed -i "s/; max_input_vars = 1000/max_input_vars = 5000/g"                        
  /etc/php/8.0/apache2-mod_php/php.ini                                                 
 
```

> Увеличение max_input_vars до 5000

#### Перезапуск Apache <!-- NAME -->

```CODE
systemctl restart httpd2                                                          
                                                                                       
 
```

### Веб-установщик <!-- HEAD -->

#### Параметры установки <!-- LIST -->
- Язык: Русский
- Каталог данных: /var/moodledata
- Тип БД: MariaDB (родной/mariadb)
- Сервер БД: localhost
- Название БД: moodle
- Пользователь БД: moodle
- Пароль БД: moodle
- Префикс таблиц: mdl_
- Порт БД: 3306
- Логин администратора: admin
- Пароль, имя, фамилия: указать свои
- Электронная почта: любая
- Страна: выбрать
- Самостоятельная регистрация: Отключить

### NextCloud <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка MariaDB <!-- NAME -->

```CODE
apt-get update && apt-get install -y mariadb-server                                      
 
```

#### Включение службы MariaDB <!-- NAME -->

```CODE
systemctl enable --now mariadb                                                           
 
```

#### Создание базы данных и пользователя <!-- NAME -->

```CODE
mariadb                                                                                  
  CREATE USER 'nextcloud'@'localhost' IDENTIFIED BY 'P@ssw0rd';                               
  CREATE DATABASE nextcloud DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;               
  GRANT ALL PRIVILEGES ON nextcloud.* to nextcloud@localhost;                                 
  EXIT;                                                                                       
 
```

> Создание БД nextcloud, пользователя nextcloud с паролем P@ssw0rd

#### Установка Apache2 <!-- NAME -->

```CODE
apt-get install -y apache2 apache2-mod_{ssl,php8.2} tzdata                               
 
```

#### Установка PHP8.2 и модулей <!-- NAME -->

```CODE
apt-get install -y php8.2 php8.2-{pdo_mysql,curl,dom,exif,fileinfo,gd2,gmp,imagick,intl,l
  ibs,mbstring,memcached,opcache,openssl,pcntl,pdo,xmlreader,zip}                             
 
```

#### Включение модулей Apache2 <!-- NAME -->

```CODE
for i in dir env headers mime rewrite;do a2enmod $i;done                                 
 
```

#### Запуск веб-сервера <!-- NAME -->

```CODE
systemctl enable --now httpd2                                                            
 
```

#### Установка wget <!-- NAME -->

```CODE
apt-get install -y wget                                                                  
 
```

#### Загрузка Nextcloud <!-- NAME -->

```CODE
wget https://download.nextcloud.com/server/releases/latest.zip                           
 
```

#### Распаковка и перемещение <!-- NAME -->

```CODE
unzip latest.zip; rm -f latest.zip                                                       
  cp -r nextcloud /var/www/html; rm -rf nextcloud                                             
 
```

#### Настройка прав доступа <!-- NAME -->

```CODE
chown -R root /var/www/html/nextcloud                                                    
  mkdir /var/www/html/nextcloud/data                                                          
  chown -R apache2 /var/www/html/nextcloud/{apps,config,data}/                                
                                                                                              
 
```

### Настройка <!-- HEAD -->

#### Содержимое файла /etc/httpd2/conf/sites-available/nextcloud.conf <!-- NAME -->

```CODE
<VirtualHost *:80>                                                                       
    DocumentRoot /var/www/html/nextcloud/                                                     
    ServerName  nextcloud.champ.first                                                         
                                                                                              
    <Directory /var/www/html/nextcloud/>                                                      
      Require all granted                                                                     
      AllowOverride All                                                                       
      Options FollowSymLinks MultiViews                                                       
                                                                                              
      <IfModule mod_dav.c>                                                                    
        Dav off                                                                               
      </IfModule>                                                                             
    </Directory>                                                                              
  </VirtualHost>                                                                              
 
```

> ServerName (доменное имя); DocumentRoot (путь к Nextcloud)

#### Активация конфигурации и перезапуск <!-- NAME -->

```CODE
ln -s /etc/httpd2/conf/sites-available/nextcloud.conf /etc/httpd2/conf/sites-enabled/    
  systemctl restart httpd2                                                                    
                                                                                              
 
```

### Веб-установщик <!-- HEAD -->

#### Параметры установки <!-- LIST -->
- Создать учётную запись администратора
- Пользователь БД: nextcloud
- Пароль БД: P@ssw0rd
- Название БД: nextcloud
- Сервер БД: localhost

### NFS <!-- HEAD -->

[Содержание](#Содержание)

### Установка на сервере <!-- HEAD -->

#### Установка NFS-сервера <!-- NAME -->

```CODE
apt-get install nfs-server                                                               
 
```

#### Создание каталога для экспорта chown 777 /nfs <!-- NAME -->

#### Содержимое файла /etc/exports <!-- NAME -->

```CODE
/nfs 192.168.20.0/26(rw,sync,no_subtree_check)                                           
 
```

> /nfs (экспортируемый каталог); 192.168.20.0/26 (разрешенная подсеть); rw (чтение-запись); sync (синхронная запись); no_subtree_check (отключить проверку подкаталогов)

#### Применение изменений <!-- NAME -->

```CODE
exportfs -ra                                                                             
 
```

> Перечитывает /etc/exports и применяет изменения

### Установка на клиенте <!-- HEAD -->

#### Установка NFS-клиента <!-- NAME -->

```CODE
apt-get install nfs-clients                                                              
 
```

#### В /etc/fstab добавить строку <!-- NAME -->

```CODE
192.168.30.3:/nfs /mnt/nfs nfs defaults 0 0                                              
 
```

> 192.168.30.3:/nfs (удаленный каталог); /mnt/nfs (точка монтирования); nfs (тип ФС)

#### Монтирование <!-- NAME -->

```CODE
mount -a                                                                                 
                                                                                              
 
```

### Проверка <!-- HEAD -->

#### Создание тестового файла на клиенте <!-- NAME -->

```CODE
cd /mnt/nfs                                                                              
  touch txt                                                                                   
  ls                                                                                          
 
```

#### Проверка на сервере <!-- NAME -->

```CODE
ls -l /nfs                                                                               
 
```

> Файл txt должен быть виден с владельцем nobody:nobody [](#Установка на сервере)

### nftables_firewall <!-- HEAD -->

[Содержание](#Содержание)

### Настройка <!-- HEAD -->

#### Содержимое файла /etc/nftables/nftables.nft <!-- NAME -->

```CODE
table inet filter {                                                                      
    chain input {                                                                             
      type filter hook input priority filter; policy drop;                                    
      ct state established,related accept                                                     
      iif lo accept                                                                           
      icmp type { echo-request, echo-reply } accept                                           
      tcp dport { 80, 443 } accept                                                            
      udp dport { 53, 123 } accept                                                            
      udp dport { 67 } accept                                                                 
      ip saddr { 192.168.2.0/24, 192.168.24.0/24, 10.10.10.0/30 } accept                      
    }                                                                                         
    chain forward {                                                                           
      type filter hook forward priority filter; policy drop;                                  
      ct state established,related accept                                                     
      ip saddr { 192.168.2.0/24, 192.168.24.0/24, 10.10.10.0/30 } accept                      
    }                                                                                         
    chain output {                                                                            
      type filter hook output priority filter; policy accept;                                 
      ct state established,related accept                                                     
      udp sport 67 udp dport 68 accept                                                        
      ip protocol ospf accept                                                                 
      ip daddr { 224.0.0.5, 224.0.0.6 } accept                                                
      udp dport { 53, 123 } accept                                                            
      udp dport { 514 } accept                                                                
      tcp dport { 514 } accept                                                                
      tcp dport { 80 } accept                                                                 
      icmp type { echo-request, echo-reply } accept                                           
      ip saddr { 192.168.2.0/24 } accept                                                      
    }                                                                                         
  }                                                                                           
 
```

> chain input (входящий); policy drop (запретить по умолчанию);

> state established,related (разрешить установленные); iif lo (loopback); icmp type (ping); tcp dport 80,443 (HTTP/HTTPS); udp dport 53,123 (DNS/NTP); udp dport 67 (DHCP); ip saddr (разрешенные подсети 192.168.2.0/24, 192.168.24.0/24, 10.10.10.0/30); chain forward (транзит); chain output (исходящий); udp sport 67 dport 68 (DHCP-клиент); ip protocol ospf (маршрутизация); ip daddr 224.0.0.5,224.0.0.6 (multicast OSPF)

### Проверка <!-- HEAD -->

#### Проверка маршрута по умолчанию <!-- NAME -->

```CODE
ip route                                                                                 
 
```

> Проверить наличие default via 192.168.24.1 dev ens3.100

#### Проверка доступности подсети 192.168.2.0/24 <!-- NAME -->

```CODE
ping 192.168.2.1                                                                         
 
```

> Проверить получение ответа от 192.168.2.1

#### Проверка доступности подсети 192.168.24.0/24 <!-- NAME -->

```CODE
ping 192.168.24.1                                                                        
 
```

> Проверить получение ответа от 192.168.24.1

#### Проверка доступа в интернет <!-- NAME -->

```CODE
ping 77.88.8.8
```

### nftables_NAT <!-- HEAD -->

[Содержание](#Содержание)

### Настройка <!-- HEAD -->

#### В /etc/net/sysctl.conf изменить строку <!-- NAME -->

```CODE
net.ipv4.ip_forward = 1                                                                  
 
```

> Включение пересылки пакетов между интерфейсами

#### Применение изменений <!-- NAME -->

```CODE
sysctl -p                                                                                
 
```

#### В /etc/nftables/nftables.nft добавить таблицу NAT <!-- NAME -->

```CODE
table ip nat {                                                                           
      chain postrouting {                                                                     
          type nat hook postrouting priority 100; policy accept;                              
          oif "ens32" masquerade                                                              
      }                                                                                       
  }                                                                                           
 
```

> table ip nat (таблица NAT); chain postrouting (обработка после маршрутизации); oif ens32 (исходящий интерфейс); masquerade (подмена адреса источника на адрес интерфейса)

#### Применение конфигурации nftables <!-- NAME -->

```CODE
nft -f /etc/nftables/nftables.nft                                                        
 
```

> Загрузка правил из файла

#### Включение службы nftables <!-- NAME -->

```CODE
systemctl enable nftables                                                                
  systemctl restart nftables
```

### nftables_port_forwarding <!-- HEAD -->

[Содержание](#Содержание)

### Проброс портов в nftables <!-- HEAD -->

#### Перенаправление порта на внутренний сервер <!-- NAME -->

```CODE
nft add rule ip nat PREROUTING iifname "ВНЕШНИЙ_ИНТЕРФЕЙС" tcp dport ПОРТ_ВНЕШНИЙ dnat to
   IP_СЕРВЕРА:ПОРТ_ВНУТРЕННИЙ                                                                 
  nft add rule ip filter FORWARD ip daddr IP_СЕРВЕРА tcp dport ПОРТ_ВНУТРЕННИЙ accept         
 
```

> PREROUTING(обработка до маршрутизации); dnat to(изменение адреса назначения); iifname(входящий интерфейс); FORWARD(разрешение пересылки)

#### Пример проброса SSH <!-- NAME -->

```CODE
nft add rule ip nat PREROUTING iifname "ens33" tcp dport 2222 dnat to 192.168.1.10:22
  nft add rule ip filter FORWARD ip daddr 192.168.1.10 tcp dport 22 accept                    
                                                                                              
 
```

#### Пример проброса HTTP <!-- NAME -->

```CODE
nft add rule ip nat PREROUTING iifname "ens33" tcp dport 80 dnat to 192.168.1.20:80      
  nft add rule ip filter FORWARD ip daddr 192.168.1.20 tcp dport 80 accept
```

### nginx_reverse_proxy <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка nginx <!-- NAME -->

```CODE
apt-get install nginx                                                                    
 
```

#### Включение автозапуска <!-- NAME -->

```CODE
systemctl enable --now nginx                                                             
                                                                                              
 
```

### Настройка обратного прокси <!-- HEAD -->

> Для настройки необходима ip-адресация и работа DNS(или hosts)

#### Создание файла конфигурации <!-- NAME -->

```CODE
nano /etc/nginx/sites-available.d/some.domain.conf                                       
                                                                                              
 
```

#### Базовая конфигурация обратного прокси <!-- NAME -->

```CODE
server {                                                                                 
      listen 80;                                                                              
      server_name some.domain;                                                                
                                                                                              
  location / {                                                                                
      proxy_pass http://10.0.0.10:8080;                                                       
      proxy_http_version 1.1;                                                                 
                                                                                              
      proxy_set_header Host $host;                                                            
      proxy_set_header X-Real-IP $remote_addr;                                                
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                            
      proxy_set_header X-Forwarded-Proto $scheme;                                             
      proxy_set_header Connection "";                                                         
  }                                                                                           
  }                                                                                           
 
```

> listen(порт прослушивания); server_name(имя виртуального хоста); location(обработка запросов к корню)

> proxy_pass(адрес внутреннего веб-приложения); proxy_http_version(версия HTTP-протокола)

> proxy_set_header Host(передача оригинального заголовка Host); X-Real-IP(реальный IP клиента)

> X-Forwarded-For(цепочка IP-адресов); X-Forwarded-Proto(протокол http или https); Connection(управление соединением)

#### Конфигурация для нескольких приложений <!-- NAME -->

```CODE
server {                                                                                 
      listen 80;  
      server_name app1.some.domain;                                                           
                                                                                              
  location / {                                                                                
      proxy_pass http://10.0.0.10:8080;                                                       
      proxy_http_version 1.1;                                                                 
                                                                                              
      proxy_set_header Host $host;                                                            
      proxy_set_header X-Real-IP $remote_addr;                                                
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                            
      proxy_set_header X-Forwarded-Proto $scheme;                                             
  }                                                                                           
  }                                                                                           
                                                                                              
  server {        
      listen 80;                                                                              
      server_name app2.some.domain;                                                           
                                                                                              
  location / {                                                                                
      proxy_pass http://10.0.0.20:8080;                                                       
      proxy_http_version 1.1;                                                                 
                                                                                              
      proxy_set_header Host $host;                                                            
      proxy_set_header X-Real-IP $remote_addr;                                                
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                            
      proxy_set_header X-Forwarded-Proto $scheme;                                             
  }                                                                                           
  }                                                                                           
 
```

> app1.some.domain перенаправляет на 10.0.0.10:8080; app2.some.domain перенаправляет на 10.0.0.20:8080

#### Конфигурация с SSL-сертификатом <!-- NAME -->

```CODE
server {                                                                                 
      listen 443 ssl;
      server_name some.domain;                                                                
                                                                                              
  ssl_certificate /etc/letsencrypt/some.domain/cert.cer;                                      
  ssl_certificate_key /etc/letsencrypt/some.domain/cert.key;                                  
  ssl_protocols TLSv1.2 TLSv1.3;                                                              
  ssl_prefer_server_ciphers on;                                                               
                                                                                              
  location / {                                                                                
      proxy_pass http://10.0.0.10:8080;                                                       
      proxy_set_header Host $host;                                                            
      proxy_set_header X-Real-IP $remote_addr;                                                
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                            
      proxy_set_header X-Forwarded-Proto $scheme;                                             
  }                                                                                           
  }                                                                                           
 
```

> listen 443 ssl(прослушивание порта 443 с поддержкой SSL/TLS)

> ssl_certificate(путь к SSL-сертификату); ssl_certificate_key(путь к приватному ключу)

> ssl_protocols(разрешенные версии TLS); ssl_prefer_server_ciphers(приоритет шифров сервера)

#### Конфигурация с таймаутами <!-- NAME -->

```CODE
server {                                                                                 
      listen 80;  
      server_name some.domain;                                                                
                                                                                              
  location / {                                                                                
      proxy_pass http://10.0.0.10:8080;                                                       
      proxy_http_version 1.1;                                                                 
                                                                                              
      proxy_set_header Host $host;                                                            
      proxy_set_header X-Real-IP $remote_addr;                                                
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                            
      proxy_set_header X-Forwarded-Proto $scheme;                                             
                                                                                              
      proxy_connect_timeout 5s;                                                               
      proxy_send_timeout 30s;                                                                 
      proxy_read_timeout 30s;                                                                 
  }                                                                                           
  }                                                                                           
 
```

> proxy_connect_timeout(время ожидания подключения к backend); proxy_send_timeout(время отправки запроса)

> proxy_read_timeout(время ожидания ответа от backend)

#### Создание символической ссылки <!-- NAME -->

```CODE
ln -s /etc/nginx/sites-available.d/some.domain.conf /etc/nginx/sites-enabled.d/          
 
```

### Проверка <!-- HEAD -->

#### Проверка синтаксиса конфигурации <!-- NAME -->

```CODE
nginx -t                                                                                 
                                                                                              
 
```

#### Применение настроек <!-- NAME -->

```CODE
systemctl restart nginx                                                                  
 
```

> можно использовать systemctl reload nginx

#### Проверка открытых портов <!-- NAME -->

```CODE
ss -tulpn | grep nginx                                                                   
                                                                                              
 
```

#### Проверка доступности backend-сервера <!-- NAME -->

```CODE
curl -I http://10.0.0.10:8080                                                            
                                                                                              
 
```

#### Просмотр логов nginx <!-- NAME -->

```CODE
journalctl -u nginx --no-pager
```

### nginx_server_balance <!-- HEAD -->

[Содержание](#Содержание)

### Балансировка нагрузки <!-- HEAD -->

#### Добавление блока upstream в конфигурацию сайта <!-- NAME -->

```CODE
upstream backend_site1 {
      server 192.168.1.101;                                                                   
      server 192.168.1.102;                                                                   
  }                                                                                           
                                                                                              
  server {                                                                                    
      listen 80;                                                                              
      server_name some.domain;                                                                
                                                                                              
  location / {                                                                                
      proxy_pass http://backend_site1;                                                        
      proxy_set_header Host $host;                                                            
      proxy_set_header X-Real-IP $remote_addr;                                                
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                            
      proxy_set_header X-Forwarded-Proto $scheme;                                             
  }                                                                                           
  }                                                                                           
 
```

> upstream(группа backend-серверов); backend_site1(имя группы); proxy_pass использует имя upstream

#### Метод round-robin с весами <!-- NAME -->

```CODE
upstream backend_site1 {                                                                 
      server 192.168.1.101 weight=3;                                                          
      server 192.168.1.102 weight=1;                                                          
  }                                                                                           
 
```

> weight(вес сервера, по умолчанию 1); сервер с weight=3 получит в 3 раза больше запросов

#### Метод least_conn <!-- NAME -->

```CODE
upstream backend_site1 {                                                                 
      least_conn;                                                                             
      server 192.168.1.101;                                                                   
      server 192.168.1.102;                                                                   
  }                                                                                           
 
```

> least_conn(запросы направляются на сервер с минимальным количеством активных соединений)

#### Метод ip_hash <!-- NAME -->

```CODE
upstream backend_site1 {                                                                 
      ip_hash;                                                                                
      server 192.168.1.101;                                                                   
      server 192.168.1.102;                                                                   
  }                                                                                           
 
```

> ip_hash(клиент всегда направляется на один и тот же сервер по IP-адресу)

#### Настройка keepalive соединений <!-- NAME -->

```CODE
upstream backend_site1 {                                                                 
      server 192.168.1.101;                                                                   
      server 192.168.1.102;                                                                   
      keepalive 32;                                                                           
  }                                                                                           
 
```

> keepalive(количество постоянных соединений к backend-серверам)

#### Настройка таймаутов и проверки доступности <!-- NAME -->

```CODE
upstream backend_site1 {                                                                 
      server 192.168.1.101 max_fails=3 fail_timeout=30s;                                      
      server 192.168.1.102 max_fails=3 fail_timeout=30s;                                      
  }                                                                                           
 
```

> max_fails(количество неудачных попыток); fail_timeout(время, на которое сервер считается недоступным)

#### Комбинированная конфигурация <!-- NAME -->

```CODE
upstream backend_site1 {
      least_conn;                                                                             
      server 192.168.1.101 weight=2 max_fails=3 fail_timeout=30s;                             
      server 192.168.1.102 weight=1 max_fails=3 fail_timeout=30s;                             
      keepalive 32;                                                                           
  }                                                                                           
                                                                                              
  server {                                                                                    
      listen 80;                                                                              
      server_name some.domain;                                                                
                                                                                              
  location / {                                                                                
      proxy_pass http://backend_site1;                                                        
      proxy_http_version 1.1;                                                                 
      proxy_set_header Connection "";                                                         
      proxy_set_header Host $host;                                                            
      proxy_set_header X-Real-IP $remote_addr;                                                
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                            
      proxy_set_header X-Forwarded-Proto $scheme;                                             
  }                                                                                           
  }                                                                                           
 
```

> least_conn с весами и проверкой доступности; proxy_http_version 1.1 и Connection "" для keepalive

### nginx_Web-based_authentication <!-- HEAD -->

[Содержание](#Содержание)

### Настройка базовой HTTP-аутентификации <!-- HEAD -->

> Для ограничения доступа к веб-приложению через встроенную HTTP-аутентификацию nginx

#### Установка утилиты для создания файла паролей <!-- NAME -->

```CODE
apt-get install apache2-utils                                                            
                                                                                              
 
```

#### Создание файла с учётными записями <!-- NAME -->

```CODE
htpasswd -c /etc/nginx/.htpasswd WEB                                                     
 
```

> Потребуется ввести пароль: P@ssw0rd

> WEB(имя пользователя); P@ssw0rd(пароль); /etc/nginx/.htpasswd(файл хранения учётных записей)

#### В блок location добавить параметры аутентификации <!-- NAME -->

```CODE
location / { 
      auth_basic "Restricted Area";                                                           
      auth_basic_user_file /etc/nginx/.htpasswd;                                              
                                                                                              
      proxy_pass http://10.0.0.10:8080;                                                       
                                                                                              
      proxy_http_version 1.1;                                                                 
                  
      proxy_set_header Host $host;                                                            
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;                            
      proxy_set_header X-Forwarded-Proto $scheme;                                             
  }                                                                                           
                                                                                              
 
```

### Проверка <!-- HEAD -->

#### Проверка корректности настроек <!-- NAME -->

```CODE
nginx -t                                                                                 
                                                                                              
 
```

#### Применение изменений <!-- NAME -->

```CODE
systemctl reload nginx
```

### open-vm-tools <!-- HEAD -->

[Содержание](#Содержание)

### Установка VMware Tools <!-- HEAD -->

#### Установка пакетов open-vm-tools <!-- NAME -->

```CODE
apt-get install open-vm-tools open-vm-tools-desktop xrandr
 
```

> open-vm-tools(базовые функции: общая папка, синхронизация времени, буфер обмена); open-vm-tools-desktop(автоматическое разрешение экрана, интеграция мыши, графика); xrandr(утилита для управления разрешением экрана)

#### Включение службы в автозагрузку <!-- NAME -->

```CODE
systemctl enable vmtoolsd
                                                                                  
 
```

#### Запуск службы <!-- NAME -->

```CODE
systemctl start vmtoolsd                                                     
                                                                                  
 
```

### Проверка <!-- HEAD -->

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status vmtoolsd
                                                                                  
 
```

#### Проверка версии VMware Tools <!-- NAME -->

```CODE
vmware-toolbox-cmd -v                                                        
                                                                                  
 
```

#### Проверка работы буфера обмена <!-- NAME -->

```CODE
vmware-toolbox-cmd stat clipboard                                            
                                                                                  
 
```

#### Проверка синхронизации времени <!-- NAME -->

```CODE
vmware-toolbox-cmd timesync status                                           
                                                                                  
 
```

### Настройка <!-- HEAD -->

#### Включение синхронизации времени с хостом <!-- NAME -->

```CODE
vmware-toolbox-cmd timesync enable
                                                                                  
 
```

#### Отключение синхронизации времени с хостом <!-- NAME -->

```CODE
vmware-toolbox-cmd timesync disable                                          
                                                                                  
 
```

#### Ручная настройка разрешения экрана <!-- NAME -->

```CODE
xrandr --output Virtual1 --mode 1920x1080                                    
 
```

> Virtual1(имя дисплея, может быть Virtual-1, HDMI-1); --mode(разрешение экрана)

#### Просмотр доступных разрешений <!-- NAME -->

```CODE
xrandr
```

### OpenSSL_certificate_center <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка OpenSSL <!-- NAME -->

```CODE
apt-get install openssl
 
```

> Обычно уже установлен в системе

### Настройка сервера CA <!-- HEAD -->

#### Создание корневой директории CA <!-- NAME -->

```CODE
mkdir /ca    
                                                                                              
 
```

#### Поиск конфигурационного файла OpenSSL <!-- NAME -->

```CODE
openssl ca                                                                               
 
```

> Команда выдаст ошибку с путём к конфигурационному файлу (/var/lib/ssl/openssl.cnf, /etc/ssl/openssl.cnf)

#### Резервная копия конфигурационного файла <!-- NAME -->

```CODE
cp /var/lib/ssl/openssl.cnf /var/lib/ssl/openssl.cnf.backup
                                                                                              
 
```

#### В /var/lib/ssl/openssl.cnf в секции [ CA_default ] <!-- NAME -->

```CODE
dir = /ca                                                                                
 
```

> Изменение корневой директории CA с ./demoCA на /ca

#### Создание структуры директорий CA <!-- NAME -->

```CODE
cd /ca                                                                                   
  mkdir certs newcerts crl private                                                            
  touch index.txt                                                                             
  echo -n '00' > serial                                                                       
 
```

> certs(выпущенные сертификаты); newcerts(новые сертификаты); crl(списки отзыва); private(приватные ключи); index.txt(база данных сертификатов); serial(серийный номер); -n(без пробела и перевода строки)

#### В /var/lib/ssl/openssl.cnf в секции [ CA_default ] <!-- NAME -->

```CODE
policy = policy_anything
 
```

> Принимаем любые значения, требуем только CN (Common Name)

#### В /var/lib/ssl/openssl.cnf в секции [ policy_anything ] <!-- NAME -->

```CODE
commonName = supplied                                                                    
 
```

> CN обязателен для заполнения

#### В /var/lib/ssl/openssl.cnf в секции [ req_distinguished_name ] <!-- NAME -->

```CODE
countryName_default = RU                                                                 
  0.organizationName_default = domain.sample                                                  
 
```

> Значения по умолчанию для CA: C=RU, O=domain.sample, CN указывается при генерации

#### В /var/lib/ssl/openssl.cnf в секции [ v3_ca ] <!-- NAME -->

```CODE
basicConstraints = CA:true                                                               
 
```

> Сертификат может быть корневым CA

#### Генерация ключей и запроса на сертификат CA <!-- NAME -->

```CODE
openssl req -nodes -new -out cacert.csr -keyout private/cakey.pem -extensions v3_ca      
 
```

> -nodes(без пароля на ключ); -new(новый запрос); -out(файл запроса); -keyout(приватный ключ); -extensions v3_ca(расширения CA). При заполнении: C=RU и O=domain.sample подставятся автоматически, CN указать вручную (например domain.sample RootCA), пустые поля заполнить точкой

#### Самоподписание сертификата CA <!-- NAME -->

```CODE
openssl ca -selfsign -in cacert.csr -out cacert.pem -extensions v3_ca
 
```

> -selfsign(самоподписание); подтвердить y на вопросы

#### Просмотр содержимого сертификата <!-- NAME -->

```CODE
openssl x509 -text -noout -in cacert.pem | less                                          
 
```

> Необязательно, для проверки содержимого сертификата

### Настройка клиента <!-- HEAD -->

#### Подготовка сертификата для клиента <!-- NAME -->

```CODE
mv cacert.pem cacert.crt
 
```

> Сертификаты должны иметь расширение .crt

#### Копирование сертификата на клиент Debian/Ubuntu <!-- NAME -->

```CODE
cp cacert.crt /usr/local/share/ca-certificates/                                          
  update-ca-certificates                                                                      
 
```

> Для дистрибутивов на базе deb

#### Копирование сертификата на клиент ALT/RHEL/CentOS <!-- NAME -->

```CODE
cp cacert.crt /etc/pki/ca-trust/source/anchors/                                          
  update-ca-trust                                                                      
 
```

> Для дистрибутивов на базе rpm

### Проверка <!-- HEAD -->

#### Проверка доверия к сертификату <!-- NAME -->

```CODE
openssl verify cacert.crt
 
```

> Должен вывести: cacert.crt: OK

### OTRS <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get update && apt-get install -y postgresql15-server otrs otrs-apache2               
                                                                                              
 
```

#### Запуск Apache <!-- NAME -->

```CODE
systemctl enable --now httpd2                                                            
                                                                                              
 
```

#### Создание системных баз данных PostgreSQL <!-- NAME -->

```CODE
/etc/init.d/postgresql initdb                                                            
                                                                                              
 
```

#### Запуск PostgreSQL <!-- NAME -->

```CODE
systemctl enable --now postgresql                                                        
                                                                                              
 
```

#### Создание пользователя и базы данных для OTRS <!-- NAME -->

```CODE
psql -U postgres                                                                         
  create database otrs;                                                                       
  create user otrs with encrypted password 'P@ssw0rd';                                        
  grant all privileges on database otrs to otrs;                                              
  alter database otrs owner to otrs;                                                          
 
```

> P@ssw0rd(пароль для пользователя otrs)

### Настройка <!-- HEAD -->

#### Настройка otrs-apache2 <!-- NAME -->

```CODE
apt-get install -y apache2-httpd-prefork                                                 
  a2enextra httpd-addon.d                                                                     
  echo "httpd-addon.d=yes" >> /etc/httpd2/conf/extra-start.d/999-otrs.conf                    
                                                                                              
 
```

#### Перезагрузка Apache <!-- NAME -->

```CODE
systemctl restart httpd2                                                                 
                                                                                              
 
```

#### Веб-установщик <!-- NAME -->

> Открыть в браузере http://IP_адрес_сервера/otrs/installer.pl

#### Действия в веб-установщике <!-- LIST -->
- Принять лицензию
- Настроить базу данных
    - type database: PostgreSQL
    - host: localhost
    - database: otrs
    - user: otrs
    - password: P@ssw0rd
- Запомнить пароль администратора
- Перейти по ссылке для входа в админскую учётную запись

#### Установка модулей PostgreSQL <!-- NAME -->

```CODE
apt-get install -y postgresql15-perl perl-DBD-Pg                                         
                                                                                              
 
```

#### Запуск OTRS <!-- NAME -->

```CODE
rm /var/www/webapps/otrs/var/cron/otrs_daemin dist                                       
  /var/www/webapps/otrs/bin/Cron.sh start otrs                                                
 
```

> Устранение ошибок

### Проверка <!-- HEAD -->

> Доступ администратора: http://IP_адрес_сервера/otrs/index.pl

> Доступ пользователей: http://IP_адрес_сервера/otrs/customer.pl

### OwnCloud <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка MariaDB <!-- NAME -->

```CODE
apt-get update && apt-get install -y mariadb-server                                      
                                                                                              
 
```

#### Запуск MariaDB <!-- NAME -->

```CODE
systemctl enable --now mariadb                                                           
                                                                                              
 
```

#### Создание базы данных и пользователя <!-- NAME -->

```CODE
mysql -uroot                                                                             
  CREATE DATABASE owncloud DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;        
  GRANT ALL PRIVILEGES ON owncloud.* TO owncloud@'%' IDENTIFIED BY 'owncloud';                
  EXIT;                                                                                       
 
```

> owncloud(имя базы данных, пользователя и пароль)

#### Установка пакетов PHP <!-- NAME -->

```CODE
apt-get install php7                                                                     
  php7-{fpm-fcgi,pdo,zip,dom,intl,gd,mysqli,pdo_mysql,mbstring,json,xmlreader,curl,fileinfo}  
                  
 
```

#### Запуск php-fpm <!-- NAME -->

```CODE
systemctl enable --now php7-fpm.service
                                                                                              
 
```

#### Установка веб-сервера <!-- NAME -->

```CODE
apt-get install -y nginx                                                                 
                                                                                              
 
```

#### Установка утилит для загрузки архива <!-- NAME -->

```CODE
apt-get install -y wget bzip2                                                            
                                                                                              
 
```

#### Загрузка OwnCloud <!-- NAME -->

```CODE
cd /tmp                                                                                  
  wget https://download.owncloud.com/server/stable/owncloud-complete-latest.tar.bz2           
 
```

> Ссылку на последнюю версию копировать со страницы https://owncloud.com/download-server/#edition

#### Создание директории для файлов OwnCloud <!-- NAME -->

```CODE
mkdir -p /var/www/webapps/owncloud                                                       
                                                                                              
 
```

#### Распаковка архива <!-- NAME -->

```CODE
tar -xvjf owncloud-*.tar.bz2 -C /var/www/webapps/owncloud                                
  mv /var/www/webapps/owncloud/owncloud/* /var/www/webapps/owncloud/                          
  rm -rf /var/www/webapps/owncloud/owncloud/*                                                 
                                                                                              
 
```

### Настройка <!-- HEAD -->

#### Содержимое файла /etc/nginx/sites-available.d/owncloud.conf <!-- NAME -->

```CODE
upstream php-handler {                                                                   
      server unix:/var/run/php7-fpm/php7-fpm.sock;                                            
  }                                                                                           
                                                                                              
  server {                                                                                    
      listen 80;  
      server_name cloud.example.com;                                                          
      return 301 https://$server_name$request_uri;                                            
  }                                                                                           
                                                                                              
  server {                                                                                    
      listen 443 ssl;
      server_name cloud.example.com;                                                          
                                                                                              
      ssl_certificate /var/lib/ssl/certs/owncloud.pem;                                        
      ssl_certificate_key /var/lib/ssl/private/owncloud.key;                                  
                                                                                              
      add_header Strict-Transport-Security "max-age=15552000; includeSubDomains";             
      add_header X-Content-Type-Options nosniff;                                              
      add_header X-Frame-Options "SAMEORIGIN";                                                
      add_header X-XSS-Protection "1; mode=block";                                            
      add_header X-Robots-Tag none;                                                           
      add_header X-Download-Options noopen;                                                   
      add_header X-Permitted-Cross-Domain-Policies none;                                      
                                                                                              
      root /var/www/webapps/owncloud;                                                         
                                                                                              
      location = /robots.txt {                                                                
          allow all;
          log_not_found off;                                                                  
          access_log off;                                                                     
      }                                                                                       
                                                                                              
      location = /.well-known/carddav {                                                       
          return 301 $scheme://$host/remote.php/dav;
      }                                                                                       
      location = /.well-known/caldav {
          return 301 $scheme://$host/remote.php/dav;                                          
      }                                                                                       
                                                                                              
      location /.well-known/acme-challenge { }                                                
                                                                                              
      client_max_body_size 512M;                                                              
      fastcgi_buffers 64 4K;
                                                                                              
      gzip off;                                                                               
                                                                                              
      error_page 403 /core/templates/403.php;                                                 
      error_page 404 /core/templates/404.php;
                                                                                              
      location / {                                                                            
          rewrite ^ /index.php$uri;                                                           
      }                                                                                       
                                                                                              
      location ~ ^/(?:build|tests|config|lib|3rdparty|templates|data)/ {                      
          return 404;                                                                         
      }                                                                                       
      location ~ ^/(?:\.|autotest|occ|issue|indie|db_|console) {
          return 404;                                                                         
      }                                                                                       
                                                                                              
      location ~ ^/(?:index|remote|public|cron|core/ajax/update|status|ocs/v[12]|updater/.+|oc
  s-provider/.+|core/templates/40[34])\.php(?:$|/) {
          fastcgi_split_path_info ^(.+\.php)(/.*)$;                                           
          include fastcgi_params;                                                             
          fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;                   
          fastcgi_param PATH_INFO $fastcgi_path_info;                                         
          fastcgi_param HTTPS on;                                                             
          fastcgi_param modHeadersAvailable true;                                             
          fastcgi_param front_controller_active true;                                         
          fastcgi_pass php-handler;                                                           
          fastcgi_intercept_errors on;                                                        
          fastcgi_request_buffering off;                                                      
      }                                                                                       
                                                                                              
      location ~ ^/(?:updater|ocs-provider)(?:$|/) {                                          
          try_files $uri $uri/ =404;
          index index.php;                                                                    
      }                                                                                       
                                                                                              
      location ~* \.(?:css|js)$ {                                                             
          try_files $uri /index.php$uri$is_args$args;
          add_header Cache-Control "public, max-age=7200";                                    
                                                                                              
          add_header X-Content-Type-Options nosniff;                                          
          add_header X-Frame-Options "SAMEORIGIN";                                            
          add_header X-XSS-Protection "1; mode=block";                                        
          add_header X-Robots-Tag none;                                                       
          add_header X-Download-Options noopen;                                               
          add_header X-Permitted-Cross-Domain-Policies none;                                  
                                                                                              
          access_log off;                                                                     
      }                                                                                       
                                                                                              
      location ~* \.(?:svg|gif|png|html|ttf|woff|ico|jpg|jpeg)$ {                             
          try_files $uri /index.php$uri$is_args$args;                                         
                                                                                              
          access_log off;                                                                     
      }                                                                                       
  }                                                                                           
                                                                                              
 
```

#### Создание символической ссылки <!-- NAME -->

```CODE
ln -s /etc/nginx/sites-available.d/owncloud.conf /etc/nginx/sites-enabled.d/             
                                                                                              
 
```

#### Генерация самоподписанного сертификата <!-- NAME -->

```CODE
cd /var/lib/ssl                                                                          
  openssl req -new -x509 -days 1461 -nodes -out certs/owncloud.pem -keyout                    
  private/owncloud.key -subj "/C=RU/ST=SPb/L=SPb/O=Global Security/OU=IT                      
  Department/CN=cloud.example.com/CN=owncloud"                                                
 
```

> Опционально, для тестирования

#### Запуск веб-сервера <!-- NAME -->

```CODE
systemctl enable --now nginx                                                             
                                                                                              
 
```

#### Веб-установщик <!-- NAME -->

> Открыть в браузере https://IP_адрес_или_доменное_имя

> Игнорировать предупреждение безопасности при использовании самоподписанного сертификата

#### Параметры веб-установщика <!-- LIST -->
- Admin user: admin
- Admin password: P@ssw0rd
- Data folder: /var/www/webapps/owncloud/data
- Configure the database: MySQL/MariaDB
- Database user: owncloud
- Database password: owncloud
- Database host: localhost
- Нажать Finish setup
- Войти в созданную учётную запись

### Проверка <!-- HEAD -->

> Доступ к веб-интерфейсу: https://IP_адрес_или_доменное_имя

### partitions_of_devices <!-- HEAD -->

[Содержание](#Содержание)

#### Создание GPT разметки на диске /dev/sda <!-- NAME -->

```CODE
parted /dev/sda                                                                          
  mklabel gpt                                                                                 
  mkpart boot 0% 100%                                                                         
 
```

> mklabel(создание таблицы разделов) {gpt, msdos}

> mkpart(создание раздела) boot(название раздела, любое)

> 0% 100%(начало и конец раздела в процентах) {1MiB 100%, 0% 50GB}

#### Создание раздела с указанием файловой системы <!-- NAME -->

```CODE
parted /dev/sdc                                                                          
  mklabel gpt                                                                                 
  mkpart root ext4 0% 100%                                                                    
 
```

> ext4(тип файловой системы) {ext4, xfs, btrfs, swap}

> root(название раздела, может быть любым{A–Z, a–z}, {0–9}, {`-`, `_`})

#### Создание нескольких разделов <!-- NAME -->

```CODE
parted /dev/sdd                                                                          
  mklabel gpt                                                                                 
  mkpart system 0% 50%                                                                        
  mkpart data 50% 100%                                                                        
 
```

> Создание двух разделов по 50% диска с названиями system и data

#### Создание раздела с точным размером <!-- NAME -->

```CODE
parted /dev/sde                                                                          
  mklabel gpt                                                                                 
  mkpart root 1MiB 10GiB
 
```

> 1MiB(начало раздела, выравнивание) 10GiB(конец раздела)

> Единицы измерения {MiB, GiB, TiB, MB, GB, TB}

#### Создание swap раздела <!-- NAME -->

```CODE
parted /dev/sdf                                                                          
  mklabel gpt                                                                                 
  mkpart swap linux-swap 0% 4GiB
  mkpart root ext4 4GiB 100%                                                                  
 
```

> Первый раздел для swap, второй для системы

#### Создание EFI раздела для UEFI систем <!-- NAME -->

```CODE
parted /dev/sdg                                                                          
  mklabel gpt                                                                                 
  mkpart EFI fat32 1MiB 512MiB                                                                
  set 1 esp on                                                                                
  mkpart root ext4 512MiB 100%                                                                
 
```

> EFI(название раздела) для загрузчика UEFI

> esp(флаг для UEFI загрузки) обязателен для EFI раздела

> Размер EFI раздела обычно 512MiB {256MiB, 512MiB, 1GiB}

> GPT обязательна для UEFI систем

#### Создание разметки для BIOS Legacy загрузки <!-- NAME -->

```CODE
parted /dev/sdh                                                                          
  mklabel msdos                                                                               
  mkpart primary ext4 1MiB 100%                                                               
  set 1 boot on                                                                               
 
```

> msdos(таблица разделов MBR) для BIOS Legacy систем

> boot(флаг загрузочного раздела) для Legacy BIOS

> Для BIOS Legacy лучше использовать msdos, не gpt

#### Создание разметки BIOS Legacy с swap <!-- NAME -->

```CODE
parted /dev/sdi                                                                          
  mklabel msdos                                                                               
  mkpart primary linux-swap 1MiB 4GiB                                                         
  mkpart primary ext4 4GiB 100%                                                               
  set 2 boot on                                                                               
 
```

> msdos для совместимости со старыми BIOS

> boot устанавливается на корневой раздел

#### Создание полной разметки с boot разделом <!-- NAME -->

```CODE
parted /dev/sdj                                                                          
  mklabel gpt                                                                                 
  mkpart boot ext4 1MiB 512MiB                                                                
  set 1 boot on                                                                               
  mkpart swap linux-swap 512MiB 4GiB                                                          
  set 2 swap on                                                                               
  mkpart root ext4 4GiB 100%                                                                  
 
```

> boot(название и флаг загрузочного раздела) для /boot

> swap(название и флаг раздела подкачки) для swap

> Типичная схема: boot + swap + root

#### Создание разметки для UEFI с boot и swap <!-- NAME -->

```CODE
parted /dev/sdk                                                                          
  mklabel gpt                                                                                 
  mkpart EFI fat32 1MiB 512MiB                                                                
  set 1 esp on                                                                                
  mkpart boot ext4 512MiB 1GiB                                                                
  set 2 boot on                                                                               
  mkpart swap linux-swap 1GiB 5GiB                                                            
  set 3 swap on                                                                               
  mkpart root ext4 5GiB 100%                                                                  
 
```

> esp(EFI раздел) + boot(/boot) + swap(подкачка) + root(корень)

> Полная схема для UEFI системы

#### Создание разметки с LVM <!-- NAME -->

```CODE
parted /dev/sdl                                                                          
  mklabel gpt                                                                                 
  mkpart EFI fat32 1MiB 512MiB                                                                
  set 1 esp on                                                                                
  mkpart lvm 512MiB 100%                                                                      
  set 2 lvm on                                                                                
 
```

> lvm(флаг для LVM) для физического тома LVM

> LVM позволяет гибко управлять разделами: изменять размер, создавать снапшоты, объединять диски

#### Пример использования LVM после создания раздела <!-- NAME -->

```CODE
pvcreate /dev/sdl2
  vgcreate vg0 /dev/sdl2                                                                      
  lvcreate -L 4G -n swap vg0                                                                  
  lvcreate -L 20G -n root vg0                                                                 
  lvcreate -l 100%FREE -n home vg0                                                            
 
```

> pvcreate(создание физического тома)

> vgcreate(создание группы томов) vg0(название группы)

> lvcreate(создание логического тома) -L(размер) -n(название) -l(процент свободного места)

> LVM позволяет изменять размер разделов без перезагрузки

#### Создание разметки с RAID <!-- NAME -->

```CODE
parted /dev/sdm                                                                          
  mklabel gpt                                                                                 
  mkpart raid1 1MiB 100%
  set 1 raid on                                                                               
 
```

> raid(флаг для RAID) для программного RAID массива

> RAID объединяет несколько дисков для отказоустойчивости или производительности

#### Неинтерактивное создание разметки <!-- NAME -->

```CODE
parted -s /dev/sdg mklabel gpt                                                           
  parted -s /dev/sdg mkpart root 0% 100%                                                      
 
```

> -s(неинтерактивный режим, без подтверждений)

#### Удаление раздела <!-- NAME -->

```CODE
parted /dev/sdh                                                                          
  rm 1                                                                                        
 
```

> rm(удаление раздела) 1(номер раздела)

#### Изменение размера раздела <!-- NAME -->

```CODE
parted /dev/sdi                                                                          
  resizepart 1 50GiB                                                                          
 
```

> resizepart(изменение размера) 1(номер раздела) 50GiB(новый размер)

#### Установка и снятие флагов раздела <!-- NAME -->

```CODE
parted /dev/sdj                                                                          
  set 1 boot on                                                                               
  set 1 boot off                                                                              
 
```

> set(установка флага) 1(номер раздела) boot(тип флага) on/off(включить/выключить)

> Типы флагов {boot, esp, swap, raid, lvm, bios_grub}

#### Просмотр доступных флагов <!-- NAME -->

```CODE
parted /dev/sda                                                                          
  help set                                                                                    
 
```

> Показывает все доступные флаги для установки

### Проверка <!-- HEAD -->

#### Просмотр разделов дисков <!-- NAME -->

```CODE
lsblk                                                                                    
 
```

> Показывает все блочные устройства и разделы

#### Просмотр информации о разделах диска <!-- NAME -->

```CODE
parted /dev/sda print                                                                    
 
```

> Показывает таблицу разделов конкретного диска с флагами

#### Просмотр всех дисков <!-- NAME -->

```CODE
parted -l                                                                                
 
```

> Показывает информацию о всех дисках в системе

#### Проверка выравнивания разделов <!-- NAME -->

```CODE
parted /dev/sda align-check optimal 1                                                    
 
```

> align-check(проверка выравнивания) optimal(тип) 1(номер раздела)

#### Проверка активации swap <!-- NAME -->

```CODE
swapon --show                                                                            
 
```

> Показывает активные swap разделы

#### Проверка монтирования EFI раздела <!-- NAME -->

```CODE
mount | grep efi                                                                         
 
```

> Показывает смонтированные EFI разделы

#### Проверка LVM томов <!-- NAME -->

```CODE
pvdisplay                                                                                
  vgdisplay                                                                                   
  lvdisplay                                                                                   
 
```

> Показывает физические тома, группы томов и логические тома LVM Исправления: - primary заменено на осмысленные названия разделов (boot, root, swap, data) - Для BIOS Legacy использую msdos, не gpt - Добавлено объяснение LVM: технология для гибкого управления разделами (изменение размера, снапшоты, объединение дисков) - Добавлен пример создания LVM томов после разметки

### phpMyAdmin <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка MariaDB <!-- NAME -->

```CODE
apt-get update -y && apt-get install -y mariadb-server                                   
                                                                                              
 
```

#### Запуск MariaDB <!-- NAME -->

```CODE
systemctl enable --now mariadb                                                           
                                                                                              
 
```

#### Установка PHP расширений для phpMyAdmin <!-- NAME -->

```CODE
apt-get install -y php8.2 php8.2-{fpm-fcgi,mbstring,zip,gd,libs,mysqlnd,mysqlnd-mysqli,bz
  2,curl,mcrypt,opcache,openssl} libmcrypt wget                                               
 
```

> Расширения для дополнительных функций и производительности phpMyAdmin

#### Загрузка phpMyAdmin <!-- NAME -->

```CODE
wget https://files.phpmyadmin.net/phpMyAdmin/5.2.1/phpMyAdmin-5.2.1-all-languages.zip    
 
```

> Ссылку на последнюю версию копировать со страницы https://docs.phpmyadmin.net

#### Распаковка архива <!-- NAME -->

```CODE
unzip phpMyAdmin-5.2.1-all-languages.zip                                                 
                                                                                              
 
```

#### Перемещение в рабочую директорию <!-- NAME -->

```CODE
mv phpMyAdmin-5.2.1-all-languages /usr/share/phpmyadmin                                  
                                                                                              
 
```

#### Создание директории для временных файлов <!-- NAME -->

```CODE
mkdir -p /var/lib/phpmyadmin/tmp                                                         
                                                                                              
 
```

#### Установка веб-сервера Apache <!-- NAME -->

```CODE
apt-get install -y httpd2 apache2-{httpd-prefork,mod_php8.2}                             
                                                                                              
 
```

#### Назначение владельца файлов phpMyAdmin <!-- NAME -->

```CODE
chown -R apache2:apache2 /usr/share/phpmyadmin                                           
  chown -R apache2:apache2 /var/lib/phpmyadmin                                                
 
```

> apache2(пользователь веб-сервера)

#### Создание конфигурационного файла phpMyAdmin <!-- NAME -->

```CODE
cp /usr/share/phpmyadmin/config.sample.inc.php /usr/share/phpmyadmin/config.inc.php      
                                                                                              
 
```

#### Создание базы данных и таблиц phpMyAdmin <!-- NAME -->

```CODE
mariadb < /usr/share/phpmyadmin/sql/create_tables.sql                                    
 
```

> Создание базы данных хранилища конфигурации

#### Создание пользователя pma для phpMyAdmin <!-- NAME -->

```CODE
mariadb                                                                                  
  GRANT SELECT, INSERT, UPDATE, DELETE ON phpmyadmin.* TO 'pma'@'localhost' IDENTIFIED BY     
  'P@ssw0rd';                                                                                 
  EXIT;                                                                                       
 
```

> pma(пользователь для административных задач phpMyAdmin)

### Настройка <!-- HEAD -->

#### В /usr/share/phpmyadmin/config.inc.php параметр blowfish_secret <!-- NAME -->

```CODE
$cfg['blowfish_secret'] = 'случайная_строка_32_символа';
 
```

> Строка из 32 случайных символов для шифрования AES

> Если короче 32 символов - менее надежные куки

#### Генерация случайной строки для blowfish_secret <!-- NAME -->

```CODE
openssl rand -base64 32                                                                  
 
```

> Генерирует случайную строку, результат скопировать в config.inc.php

> Альтернативные способы {openssl rand -hex 16, pwgen 32 1, head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32}

#### Пример сгенерированной строки в config.inc.php <!-- NAME -->

```CODE
$cfg['blowfish_secret'] = 'a8b7c6d5e4f3g2h1i0j9k8l7m6n5o4p3';
 
```

> Использовать результат команды openssl rand -base64 32

#### В /usr/share/phpmyadmin/config.inc.php раскомментировать controluser и controlpass <!-- NAME -->

```CODE
$cfg['Servers'][$i]['controluser'] = 'pma';                                              
  $cfg['Servers'][$i]['controlpass'] = 'P@ssw0rd';                                            
 
```

> Пользователь для административных задач в многопользовательских сценариях

#### В /usr/share/phpmyadmin/config.inc.php раскомментировать Storage database and tables <!-- NAME -->

```CODE
$cfg['Servers'][$i]['pmadb'] = 'phpmyadmin';                                             
  $cfg['Servers'][$i]['bookmarktable'] = 'pma__bookmark';                                     
  $cfg['Servers'][$i]['relation'] = 'pma__relation';                                          
  $cfg['Servers'][$i]['table_info'] = 'pma__table_info';                                      
  $cfg['Servers'][$i]['table_coords'] = 'pma__table_coords';                                  
  $cfg['Servers'][$i]['pdf_pages'] = 'pma__pdf_pages';                                        
  $cfg['Servers'][$i]['column_info'] = 'pma__column_info';                                    
  $cfg['Servers'][$i]['history'] = 'pma__history';                                            
  $cfg['Servers'][$i]['table_uiprefs'] = 'pma__table_uiprefs';                                
  $cfg['Servers'][$i]['tracking'] = 'pma__tracking';                                          
  $cfg['Servers'][$i]['userconfig'] = 'pma__userconfig';                                      
  $cfg['Servers'][$i]['recent'] = 'pma__recent';                                              
  $cfg['Servers'][$i]['favorite'] = 'pma__favorite';                                          
  $cfg['Servers'][$i]['users'] = 'pma__users';                                                
  $cfg['Servers'][$i]['usergroups'] = 'pma__usergroups';                                      
  $cfg['Servers'][$i]['navigationhiding'] = 'pma__navigationhiding';                          
  $cfg['Servers'][$i]['savedsearches'] = 'pma__savedsearches';                                
  $cfg['Servers'][$i]['central_columns'] = 'pma__central_columns';                            
  $cfg['Servers'][$i]['designer_settings'] = 'pma__designer_settings';                        
  $cfg['Servers'][$i]['export_templates'] = 'pma__export_templates';                          
 
```

> Определение базы данных и таблиц хранилища конфигурации

#### В /usr/share/phpmyadmin/config.inc.php настроить временную директорию <!-- NAME -->

```CODE
$cfg['TempDir'] = '/var/lib/phpmyadmin/tmp';                                             
 
```

> Использование созданной ранее директории для временных файлов

#### В /usr/share/phpmyadmin/config.inc.php разрешить указывать сервер БД <!-- NAME -->

```CODE
$cfg['AllowArbitraryServer'] = true;                                                     
 
```

> Опционально, для явного указания IP-адреса или имени сервера БД

#### Настройка удалённого доступа к MariaDB в /etc/my.cnf.d/server.cnf <!-- NAME -->

```CODE
bind-address = 0.0.0.0                                                                   
  #skip-networking                                                                            
 
```

> bind-address(IP-адрес для подключений) {0.0.0.0, 192.168.1.0/24, конкретный_IP}

> 0.0.0.0(разрешено подключаться всем и отовсюду)

> skip-networking(закомментировать для разрешения сетевых подключений)

> Опционально, не влияет на работу phpMyAdmin

#### Предоставление привилегий пользователю root для удалённого доступа <!-- NAME -->

```CODE
mariadb                                                                                  
  GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'P@ssw0rd' WITH GRANT OPTION;       
  EXIT;                                                                                       
 
```

> Опционально, если необходимо удалённое подключение

> GRANT ALL PRIVILEGES(полные права на все операции)

> *.*(все базы данных и таблицы)

> 'root'@'%'(пользователь root с любого хоста)

> %(с любого хоста)

#### Запуск веб-сервера Apache <!-- NAME -->

```CODE
systemctl enable --now httpd2                                                            
                                                                                              
 
```

#### Содержимое файла /etc/httpd2/conf/sites-available/phpmyadmin.conf <!-- NAME -->

```CODE
Alias /phpmyadmin /usr/share/phpmyadmin                                                  
                                                                                              
  <Directory /usr/share/phpmyadmin>                                                           
      Options FollowSymLinks                                                                  
      DirectoryIndex index.php                                                                
      AllowOverride All
      Require all granted                                                                     
  </Directory>                                                                                
                                                                                              
 
```

#### Включение конфигурационного файла <!-- NAME -->

```CODE
a2ensite phpmyadmin                                                                      
                                                                                              
 
```

#### Проверка синтаксиса конфигурации Apache <!-- NAME -->

```CODE
apachectl configtest                                                                     
                                                                                              
 
```

#### Применение изменений Apache <!-- NAME -->

```CODE
systemctl reload httpd2                                                                  
                                                                                              
 
```

#### Исправление ошибки входа в phpMyAdmin в /etc/my.cnf.d/server.cnf <!-- NAME -->

```CODE
skip-grant-tables                                                                        
 
```

> Опционально, если возникает ошибка при входе

#### Перезагрузка MariaDB после изменений <!-- NAME -->

```CODE
systemctl restart mariadb                                                                
                                                                                              
 
```

### Проверка <!-- HEAD -->

#### Проверка открытого порта MariaDB <!-- NAME -->

```CODE
ss -tlpn | grep mysqld                                                                   
 
```

> Показывает открытый порт 3306 для удалённых подключений

#### Проверка удалённого доступа с клиента <!-- NAME -->

```CODE
mariadb -h IP_адрес_сервера -u root -p                                                   
 
```

> На клиенте должен быть установлен пакет mariadb-client

#### Доступ к phpMyAdmin <!-- NAME -->

> Открыть в браузере http://IP_адрес_сервера/phpmyadmin

> Вход под пользователем root с паролем P@ssw0rd

### PostgreSQL_base-command <!-- HEAD -->

[Содержание](#Содержание)

### Подключение к PostgreSQL <!-- HEAD -->

#### Подключение к БД от имени пользователя postgres <!-- NAME -->

```CODE
psql -U postgres                                                                         
 
```

> -U(имя пользователя)

#### Подключение к конкретной базе данных <!-- NAME -->

```CODE
psql -U user01 -d db01                                                                   
 
```

> -d(имя базы данных)

#### Удалённое подключение к БД <!-- NAME -->

```CODE
psql -U user01 -h 192.168.1.10 -d db01                                                   
 
```

> -h(IP-адрес или hostname сервера)

#### Подключение с указанием порта <!-- NAME -->

```CODE
psql -U user01 -h 192.168.1.10 -p 5432 -d db01                                           
 
```

> -p(порт) по умолчанию 5432

#### Выход из psql <!-- NAME -->

```CODE
\q                                                                                       
                                                                                              
 
```

### Управление базами данных <!-- HEAD -->

#### Создание базы данных <!-- NAME -->

```CODE
CREATE DATABASE mydb;                                                                    
 
```

> mydb(имя создаваемой БД)

#### Создание БД с указанием владельца и кодировки <!-- NAME -->

```CODE
CREATE DATABASE mydb OWNER myuser ENCODING 'UTF8';                                       
 
```

> OWNER(владелец БД); ENCODING(кодировка) {UTF8, LATIN1}

#### Удаление базы данных <!-- NAME -->

```CODE
DROP DATABASE mydb;                                                                      
 
```

> Удаляет БД безвозвратно

#### Переименование базы данных <!-- NAME -->

```CODE
ALTER DATABASE mydb RENAME TO newdb;                                                     
                                                                                              
 
```

#### Просмотр списка баз данных <!-- NAME -->

```CODE
\l                                                                                       
 
```

> Показывает все БД с владельцами и кодировками

#### Просмотр списка БД через SQL <!-- NAME -->

```CODE
SELECT datname FROM pg_database;                                                         
                                                                                              
 
```

#### Подключение к другой БД внутри psql <!-- NAME -->

```CODE
\c dbname                                                                                
 
```

> Переключение между базами данных

#### Просмотр размера базы данных <!-- NAME -->

```CODE
SELECT pg_size_pretty(pg_database_size('mydb'));                                         
                                                                                              
 
```

### Управление пользователями <!-- HEAD -->

#### Создание пользователя <!-- NAME -->

```CODE
CREATE USER username WITH PASSWORD 'P@ssw0rd';                                           
 
```

> username(имя пользователя)

#### Создание пользователя с правами суперпользователя <!-- NAME -->

```CODE
CREATE USER admin WITH SUPERUSER PASSWORD 'P@ssw0rd';                                    
 
```

> SUPERUSER(полные права на сервер)

#### Создание пользователя с правами создания БД <!-- NAME -->

```CODE
CREATE USER dbcreator WITH CREATEDB PASSWORD 'P@ssw0rd';                                 
 
```

> CREATEDB(право создавать базы данных)

#### Изменение пароля пользователя <!-- NAME -->

```CODE
ALTER USER username WITH PASSWORD 'NewP@ssw0rd';                                         
                                                                                              
 
```

#### Удаление пользователя <!-- NAME -->

```CODE
DROP USER username;                                                                      
                                                                                              
 
```

#### Просмотр списка пользователей <!-- NAME -->

```CODE
\du                                                                                      
 
```

> Показывает пользователей с их ролями

#### Просмотр списка пользователей через SQL <!-- NAME -->

```CODE
SELECT usename, usesuper, usecreatedb FROM pg_catalog.pg_user;                           
                                                                                              
 
```

#### Переименование пользователя <!-- NAME -->

```CODE
ALTER USER oldname RENAME TO newname;                                                    
                                                                                              
 
```

### Управление правами доступа <!-- HEAD -->

#### Предоставление всех прав на БД пользователю <!-- NAME -->

```CODE
GRANT ALL PRIVILEGES ON DATABASE mydb TO username;                                       
 
```

> ALL PRIVILEGES(все права на БД)

#### Предоставление прав на подключение к БД <!-- NAME -->

```CODE
GRANT CONNECT ON DATABASE mydb TO username;                                              
 
```

> CONNECT(право подключаться к БД)

#### Предоставление прав на схему <!-- NAME -->

```CODE
GRANT ALL ON SCHEMA public TO username;                                                  
 
```

> public(схема по умолчанию)

#### Предоставление прав на все таблицы в схеме <!-- NAME -->

```CODE
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO username;                         
                                                                                              
 
```

#### Предоставление прав на конкретную таблицу <!-- NAME -->

```CODE
GRANT SELECT, INSERT, UPDATE, DELETE ON tablename TO username;                           
 
```

> SELECT, INSERT, UPDATE, DELETE(типы операций)

#### Отзыв прав у пользователя <!-- NAME -->

```CODE
REVOKE ALL PRIVILEGES ON DATABASE mydb FROM username;                                    
                                                                                              
 
```

#### Изменение владельца базы данных <!-- NAME -->

```CODE
ALTER DATABASE mydb OWNER TO newowner;                                                   
                                                                                              
 
```

#### Изменение владельца таблицы <!-- NAME -->

```CODE
ALTER TABLE tablename OWNER TO newowner;                                                 
                                                                                              
 
```

### Управление таблицами <!-- HEAD -->

#### Просмотр списка таблиц <!-- NAME -->

```CODE
\dt                                                                                      
 
```

> Показывает таблицы в текущей БД

#### Просмотр списка таблиц с размерами <!-- NAME -->

```CODE
\dt+                                                                                     
 
```

> Показывает таблицы с размерами и описанием

#### Просмотр структуры таблицы <!-- NAME -->

```CODE
\d tablename                                                                             
 
```

> Показывает столбцы, типы данных, индексы

#### Создание таблицы <!-- NAME -->

```CODE
CREATE TABLE users (                                                                     
      id SERIAL PRIMARY KEY,                                                                  
      username VARCHAR(50) NOT NULL,                                                          
      email VARCHAR(100) UNIQUE,                                                              
      created_at TIMESTAMP DEFAULT NOW()                                                      
  );                                                                                          
 
```

> SERIAL(автоинкремент); PRIMARY KEY(первичный ключ); NOT NULL(обязательное поле); UNIQUE(уникальное значение)

#### Удаление таблицы <!-- NAME -->

```CODE
DROP TABLE tablename;
                                                                                              
 
```

#### Переименование таблицы <!-- NAME -->

```CODE
ALTER TABLE oldname RENAME TO newname;                                                   
                                                                                              
 
```

#### Добавление столбца в таблицу <!-- NAME -->

```CODE
ALTER TABLE tablename ADD COLUMN columnname VARCHAR(50);                                 
                                                                                              
 
```

#### Удаление столбца из таблицы <!-- NAME -->

```CODE
ALTER TABLE tablename DROP COLUMN columnname;                                            
                                                                                              
 
```

#### Изменение типа данных столбца <!-- NAME -->

```CODE
ALTER TABLE tablename ALTER COLUMN columnname TYPE INTEGER;                              
                                                                                              
 
```

#### Очистка таблицы <!-- NAME -->

```CODE
TRUNCATE TABLE tablename;                                                                
 
```

> Удаляет все строки, но сохраняет структуру

### Работа с данными <!-- HEAD -->

#### Вставка данных в таблицу <!-- NAME -->

```CODE
INSERT INTO users (username, email) VALUES ('john', 'john@example.com');                 
                                                                                              
 
```

#### Вставка нескольких строк <!-- NAME -->

```CODE
INSERT INTO users (username, email) VALUES                                               
  ('alice', 'alice@example.com'),                                                             
  ('bob', 'bob@example.com');                                                                 
                                                                                              
 
```

#### Выборка всех данных из таблицы <!-- NAME -->

```CODE
SELECT * FROM users;                                                                     
                                                                                              
 
```

#### Выборка конкретных столбцов <!-- NAME -->

```CODE
SELECT username, email FROM users;                                                       
                                                                                              
 
```

#### Выборка с условием <!-- NAME -->

```CODE
SELECT * FROM users WHERE id = 1;                                                        
 
```

> WHERE(условие фильтрации)

#### Выборка с сортировкой <!-- NAME -->

```CODE
SELECT * FROM users ORDER BY created_at DESC;                                            
 
```

> ORDER BY(сортировка); DESC(по убыванию) {ASC, DESC}

#### Выборка с ограничением количества строк <!-- NAME -->

```CODE
SELECT * FROM users LIMIT 10;                                                            
 
```

> LIMIT(ограничение количества строк)

#### Обновление данных <!-- NAME -->

```CODE
UPDATE users SET email = 'newemail@example.com' WHERE id = 1;                            
                                                                                              
 
```

#### Удаление данных <!-- NAME -->

```CODE
DELETE FROM users WHERE id = 1;                                                          
                                                                                              
 
```

#### Подсчёт количества строк <!-- NAME -->

```CODE
SELECT COUNT(*) FROM users;                                                              
                                                                                              
 
```

### Резервное копирование и восстановление <!-- HEAD -->

#### Создание резервной копии БД <!-- NAME -->

```CODE
pg_dump -U postgres -d mydb -f backup.sql                                                
 
```

> -f(файл для сохранения резервной копии)

#### Создание резервной копии в сжатом формате <!-- NAME -->

```CODE
pg_dump -U postgres -d mydb -F c -f backup.dump                                          
 
```

> -F c(custom format, сжатый формат)

#### Создание резервной копии всех БД <!-- NAME -->

```CODE
pg_dumpall -U postgres -f all_databases.sql                                              
 
```

> pg_dumpall(резервное копирование всех БД и пользователей)

#### Восстановление БД из SQL файла <!-- NAME -->

```CODE
psql -U postgres -d mydb -f backup.sql                                                   
 
```

> Восстановление из текстового SQL файла

#### Восстановление БД из сжатого формата <!-- NAME -->

```CODE
pg_restore -U postgres -d mydb backup.dump                                               
 
```

> pg_restore(восстановление из custom format)

#### Восстановление с созданием новой БД <!-- NAME -->

```CODE
pg_restore -U postgres -C -d postgres backup.dump                                        
 
```

> -C(создать БД перед восстановлением)

### Информационные команды psql <!-- HEAD -->

#### Список всех команд psql <!-- NAME -->

```CODE
\?                                                                                       
 
```

> Показывает все доступные команды psql

#### Список SQL команд <!-- NAME -->

```CODE
\h                                                                                       
 
```

> Показывает справку по SQL командам

#### Справка по конкретной SQL команде <!-- NAME -->

```CODE
\h CREATE TABLE                                                                          
 
```

> Показывает синтаксис команды CREATE TABLE

#### Просмотр текущей БД и пользователя <!-- NAME -->

```CODE
\conninfo                                                                                
 
```

> Показывает информацию о текущем подключении

#### Просмотр всех схем <!-- NAME -->

```CODE
\dn                                                                                      
 
```

> Показывает список схем в текущей БД

#### Просмотр всех представлений <!-- NAME -->

```CODE
\dv                                                                                      
 
```

> Показывает список представлений (views)

#### Просмотр всех индексов <!-- NAME -->

```CODE
\di                                                                                      
 
```

> Показывает список индексов

#### Просмотр всех последовательностей <!-- NAME -->

```CODE
\ds                                                                                      
 
```

> Показывает список sequences

#### Включение расширенного вывода <!-- NAME -->

```CODE
\x                                                                                       
 
```

> Переключает между обычным и расширенным форматом вывода

#### Выполнение команд из файла <!-- NAME -->

```CODE
\i /path/to/file.sql                                                                     
 
```

> Выполняет SQL команды из файла

#### Вывод результата запроса в файл <!-- NAME -->

```CODE
\o /path/to/output.txt                                                                   
  SELECT * FROM users;                                                                        
  \o                                                                                          
 
```

> \o(перенаправление вывода в файл); \o без параметра(отключение перенаправления)

#### Измерение времени выполнения запросов <!-- NAME -->

```CODE
\timing                                                                                  
 
```

> Включает/выключает отображение времени выполнения

### Управление индексами <!-- HEAD -->

#### Создание индекса <!-- NAME -->

```CODE
CREATE INDEX idx_username ON users(username);                                            
 
```

> idx_username(имя индекса); users(таблица); username(столбец)

#### Создание уникального индекса <!-- NAME -->

```CODE
CREATE UNIQUE INDEX idx_email ON users(email);                                           
 
```

> UNIQUE(индекс с уникальными значениями)

#### Удаление индекса <!-- NAME -->

```CODE
DROP INDEX idx_username;                                                                 
                                                                                              
 
```

#### Просмотр индексов таблицы <!-- NAME -->

```CODE
\d tablename                                                                             
 
```

> Показывает индексы в описании таблицы

### Управление транзакциями <!-- HEAD -->

#### Начало транзакции <!-- NAME -->

```CODE
BEGIN;                                                                                   
                                                                                              
 
```

#### Фиксация транзакции <!-- NAME -->

```CODE
COMMIT;                                                                                  
                                                                                              
 
```

#### Откат транзакции <!-- NAME -->

```CODE
ROLLBACK;
                                                                                              
 
```

#### Пример использования транзакции <!-- NAME -->

```CODE
BEGIN;                                                                                   
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;                                   
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;                                   
  COMMIT;                                                                                     
 
```

> Транзакция для атомарного выполнения нескольких операций

### Проверка <!-- HEAD -->

#### Проверка версии PostgreSQL <!-- NAME -->

```CODE
SELECT version();                                                                        
                                                                                              
 
```

#### Проверка текущего времени на сервере <!-- NAME -->

```CODE
SELECT NOW();                                                                            
                                                                                              
 
```

#### Проверка активных подключений <!-- NAME -->

```CODE
SELECT * FROM pg_stat_activity;                                                          
 
```

> Показывает все активные подключения к серверу

#### Проверка размера всех БД <!-- NAME -->

```CODE
SELECT datname, pg_size_pretty(pg_database_size(datname)) FROM pg_database;              
                                                                                              
 
```

#### Проверка размера всех таблиц в БД <!-- NAME -->

```CODE
SELECT tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))     
  FROM pg_tables WHERE schemaname = 'public';
```

### RADIUS <!-- HEAD -->

[Содержание](#Содержание)

### Установка RADIUS сервера <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get update && apt-get install -y freeradius freeradius-utils                         
 
```

#### Запуск службы <!-- NAME -->

```CODE
systemctl enable --now radiusd                                                           
                                                                                              
 
```

### Настройка RADIUS сервера <!-- HEAD -->

#### В /etc/raddb/clients.conf <!-- NAME -->

```CODE
client ALL {                                                                             
    ipaddr = 0.0.0.0
    netmask = 0                                                                               
    secret = P@ssw0rd                                                                         
  }                                                                                           
 
```

> ipaddr(IP клиента); netmask(маска сети); secret(общий секрет)

#### В конец /etc/raddb/users <!-- NAME -->

```CODE
netuser Cleartext-Password := "P@ssw0rd"                                                 
          Service-Type = Administrative-User,                                                 
          Cisco-AVPair = "shell:roles=admin"                                                  
 
```

> Cleartext-Password(пароль пользователя); Service-Type(тип доступа); Cisco-AVPair(роль для Cisco)

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart radiusd
                                                                                              
 
```

### Проверка RADIUS сервера <!-- HEAD -->

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status radiusd                                                                 
 
```

> служба должна быть active (running)

#### Тестирование аутентификации <!-- NAME -->

```CODE
radtest netuser P@ssw0rd localhost 0 P@ssw0rd                                            
 
```

> должен вернуть Access-Accept

### Установка RADIUS клиента <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get update && apt-get install -y pam_radius                                          
 
```

#### В /etc/pam_radius_auth.conf <!-- NAME -->

```CODE
<ip сервера> P@ssw0rd 3                                                                  
 
```

> формат: IP секрет таймаут

#### В /etc/pam.d/sshd и /etc/pam.d/system-auth-local <!-- NAME -->

```CODE
auth  sufficient  pam_radius_auth.so                                                     
 
```

> sufficient(достаточно для авторизации); pam_radius_auth.so(модуль RADIUS)

#### Создание пользователя <!-- NAME -->

```CODE
useradd netuser                                                                          
 
```

> пользователь должен совпадать с настроенным на сервере

### Проверка RADIUS клиента <!-- HEAD -->

#### Проверка подключения через SSH <!-- NAME -->

```CODE
ssh netuser@<ip клиента>                                                                 
 
```

> вход должен пройти с паролем P@ssw0rd через RADIUS-сервер

### replication_postgresql-server <!-- HEAD -->

[Содержание](#Содержание)

### Установка PostgreSQL на резервном сервере <!-- HEAD -->

#### На SRV-BR установка пакетов <!-- NAME -->

```CODE
apt-get install -y postgresql16 postgresql16-server postgresql16-contrib                 
 
```

> SRV-BR(резервный сервер); SRV-HQ(основной сервер)

### Настройка основного сервера <!-- HEAD -->

#### На SRV-HQ в /var/lib/pgsql/data/postgresql.conf <!-- NAME -->

```CODE
wal_level = replica                                                                      
  max_wal_senders = 2                                                                         
  max_replication_slots = 2                                                                   
  hot_standby = on                                                                            
  hot_standby_feedback = on                                                                   
 
```

> wal_level(уровень журналирования); max_wal_senders(количество процессов репликации); hot_standby(чтение на реплике)

#### Перезапуск службы на SRV-HQ <!-- NAME -->

```CODE
systemctl restart postgresql
                                                                                              
 
```

### Настройка репликации на резервном сервере <!-- HEAD -->

#### На SRV-BR остановка службы <!-- NAME -->

```CODE
systemctl stop postgresql                                                                
                                                                                              
 
```

#### Очистка директории данных <!-- NAME -->

```CODE
rm -rf /var/lib/pgsql/data/*                                                             
 
```

> удаляет существующие данные для создания реплики

#### Создание базовой копии с SRV-HQ <!-- NAME -->

```CODE
pg_basebackup -h 192.168.11.67 -U postgres -D /var/lib/pgsql/data --wal-method=stream    
  --write-recovery-conf                                                                       
 
```

> -h(IP основного сервера); -U(пользователь); -D(директория данных); --wal-method(метод передачи WAL); --write-recovery-conf(создание конфига репликации)

#### Установка прав доступа <!-- NAME -->

```CODE
chown -R postgres:postgres /var/lib/pgsql/data/
                                                                                              
 
```

#### Запуск службы на SRV-BR <!-- NAME -->

```CODE
systemctl start postgresql                                                               
                                                                                              
 
```

### Проверка репликации <!-- HEAD -->

#### Подключение к базе данных <!-- NAME -->

```CODE
psql -U postgres                                                                         
 
```

> подключение к PostgreSQL

#### Проверка статуса репликации на SRV-HQ <!-- NAME -->

```CODE
SELECT * FROM pg_stat_replication;                                                       
 
```

> показывает подключенные реплики

#### Проверка данных на SRV-BR <!-- NAME -->

```CODE
\c one                                                                                   
  \dt+                                                                                        
 
```

> \c(подключение к БД); \dt+(список таблиц с размерами)

### resolve_options <!-- HEAD -->

[Содержание](#Содержание)

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

### rsyslog <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка пакетов на всех устройствах <!-- NAME -->

```CODE
apt-get install rsyslog logrotate                                                        
 
```

> rsyslog(сбор и пересылка логов); logrotate(ротация и сжатие логов)

> Обычно работают в связке

### Настройка сервера сбора логов <!-- HEAD -->

#### В /etc/rsyslog.conf <!-- NAME -->

```CODE
module(load="imuxsock")                                                                  
  module(load="imklog")                                                                       
  module(load="imudp")                                                                        
  input(type="imudp" port="514")                                                              
  module(load="imtcp")                                                                        
  input(type="imtcp" port="514")                                                              
                                                                                              
  $template RemoteLogs, "/opt/%HOSTNAME%/%PROGRAMNAME%.log"                                   
                  
  if ($fromhost-ip != "127.0.0.1" and $syslogseverity <= 4) then ?RemoteLogs                  
  & stop          
 
```

> imuxsock(локальные сообщения); imklog(логи ядра); imudp/imtcp(приём по UDP/TCP); $syslogseverity <= 4(warning и выше); & stop(остановка обработки)

#### Создание каталогов для логов <!-- NAME -->

```CODE
mkdir -p /opt/client1
  mkdir -p /opt/client2                                                                       
  mkdir -p /opt/client3                                                                       
 
```

> создаются каталоги для каждого клиента

#### Установка прав на каталоги <!-- NAME -->

```CODE
chown -R root:root /opt                                                                  
  chmod -R 755 /opt                                                                           
 
```

> права для записи логов службой rsyslog

#### Перезапуск службы на сервере <!-- NAME -->

```CODE
systemctl restart rsyslog                                                                
                                                                                              
 
```

### Настройка клиента <!-- HEAD -->

#### В /etc/rsyslog.conf на клиенте <!-- NAME -->

```CODE
*.warning action(type="omfwd"                                                            
      target="<HQ-SRV_IP>"                                                                    
      port="514"                                                                              
      protocol="tcp"                                                                          
      action.resumeRetryCount="-1"                                                            
      queue.type="linkedList"                                                                 
      queue.size="10000")                                                                     
 
```

> *.warning(уровень warning и выше); target(IP сервера логов); protocol(tcp для надежности); resumeRetryCount=-1(бесконечные попытки); queue.size(размер очереди сообщений)

#### Перезапуск службы на клиенте <!-- NAME -->

```CODE
systemctl restart rsyslog
                                                                                              
 
```

### Проверка <!-- HEAD -->

#### Проверка открытого порта на сервере <!-- NAME -->

```CODE
ss -tulpn | grep 514                                                                     
 
```

> должен показать порты 514 TCP и UDP

#### Проверка каталогов логов на сервере <!-- NAME -->

```CODE
ls -la /opt/                                                                             
 
```

> должны появиться каталоги с именами клиентов

#### Проверка содержимого логов <!-- NAME -->

```CODE
ls -la /opt/client1/                                                                     
 
```

> должны появиться файлы логов от клиента

#### Тестовая отправка сообщения с клиента <!-- NAME -->

```CODE
logger -p user.warning "Test message from client"                                        
 
```

> отправляет тестовое сообщение уровня warning

#### Проверка получения на сервере <!-- NAME -->

```CODE
tail -f /opt/client1/*.log                                                               
 
```

> должно появиться тестовое сообщение

### SAMBA_INTERNAL_samba <!-- HEAD -->

[Содержание](#Содержание)

### Установка Samba DC <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get update && apt-get install -y task-samba-dc                                       
 
```

> task-samba-dc(Samba DC на базе Heimdal Kerberos)

#### Остановка конфликтующих служб <!-- NAME -->

```CODE
for i in smb nmb krb5kdc slapd bind; do systemctl disable $i --now; done                 
 
```

> Samba DC использует собственные LDAP и Kerberos

### Настройка имени узла и домена <!-- HEAD -->

#### В /etc/sysconfig/network <!-- NAME -->

```CODE
HOSTNAME=dc.domain.sample
 
```

> dc.domain.sample(FQDN сервера); domain.sample(имя домена)

#### Установка имени узла <!-- NAME -->

```CODE
hostnamectl set-hostname dc.domain.sample                                                  
  exec bash                                                                                   
  domainname domain.sample                                                                      
 
```

> exec bash(перезагрузка оболочки для применения)

#### В /etc/resolvconf.conf <!-- NAME -->

```CODE
nameserver 127.0.0.1                                                                     
 
```

> для корректного распознавания локальных DNS-запросов

### Подготовка к созданию домена <!-- HEAD -->

#### Очистка баз и конфигурации Samba <!-- NAME -->

```CODE
rm -f /etc/samba/smb.conf
  rm -rf /var/lib/samba                                                                       
  rm -rf /var/cache/samba                                                                     
  mkdir -p /var/lib/samba/sysvol                                                              
 
```

> удаляет предыдущую конфигурацию домена

### Создание домена <!-- HEAD -->

#### Интерактивное создание домена <!-- NAME -->

```CODE
samba-tool domain provision
 
```

> указать: доменное имя, рабочую группу, роль dc, бэкенд SAMBA_INTERNAL, DNS forwarder 77.88.8.8, пароль администратора

#### Пакетное создание домена <!-- NAME -->

```CODE
samba-tool domain provision --realm=domain.sample --domain=domain --adminpass='P@ssw0rd'
  --dns-backend=SAMBA_INTERNAL --option="dns forwarder=77.88.8.8" --server-role=dc            
  --use-rfc2307   
 
```

> --realm(имя области Kerberos и DNS домена); --domain(имя рабочей группы); --dns-backend(бэкенд DNS); --use-rfc2307(поддержка UID/GID и ACL)

#### Запуск службы Samba <!-- NAME -->

```CODE
systemctl enable --now samba
                                                                                              
 
```

#### Копирование конфигурации Kerberos <!-- NAME -->

```CODE
cp /var/lib/samba/private/krb5.conf /etc/krb5.conf                                       
 
```

> Samba создает шаблон krb5.conf при создании домена

### Проверка <!-- HEAD -->

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status samba
 
```

> служба должна быть active (running)

#### Просмотр информации о домене <!-- NAME -->

```CODE
samba-tool domain info 127.0.0.1                                                         
 
```

> показывает общую информацию о домене

#### Просмотр общих ресурсов <!-- NAME -->

```CODE
smbclient -L localhost -U administrator                                                  
 
```

> должны быть netlogon и sysvol

#### Проверка DNS в /etc/resolv.conf <!-- NAME -->

```CODE
cat /etc/resolv.conf                                                                     
 
```

> должен быть nameserver 127.0.0.1

#### Проверка SRV-записи Kerberos <!-- NAME -->

```CODE
host -t SRV _kerberos._udp.domain.sample.                                                  
 
```

> утилита host из пакета bind-utils

#### Проверка SRV-записи LDAP <!-- NAME -->

```CODE
host -t SRV _ldap._tcp.domain.sample.                                                      
 
```

> проверяет доступность LDAP

#### Проверка A-записи хоста <!-- NAME -->

```CODE
host -t A dc.domain.sample.                                                                
 
```

> должен вернуть IP-адрес контроллера домена

#### Проверка Kerberos <!-- NAME -->

```CODE
kinit administrator@DOMAIN.SAMPLE                                                          
 
```

> имя домена в верхнем регистре; запрашивает пароль администратора

### samba_share_folder <!-- HEAD -->

[Содержание](#Содержание)

### Настройка Samba для анонимного доступа <!-- HEAD -->

#### Создание общей директории <!-- NAME -->

```CODE
mkdir /opt/data                                                                          
  chmod 777 /opt/data                                                                         
 
```

> 777(полные права для всех пользователей)

#### В /etc/samba/smb.conf добавить секцию <!-- NAME -->

```CODE
[samba]                                                                                  
  path = /opt/data                                                                            
  browseable = yes                                                                            
  writable = yes                                                                              
  guest ok = yes                                                                              
  read only = no                                                                              
  force user = nobody                                                                         
 
```

> guest ok = yes(анонимный доступ); force user(все действия от имени nobody)

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart smbd                                                                   
                                                                                              
 
```

### Настройка Samba для пользователей домена <!-- HEAD -->

#### Создание общей директории <!-- NAME -->

```CODE
mkdir /opt/data
  chmod 770 /opt/data                                                                         
  chown root:domain_users /opt/data                                                           
 
```

> 770(доступ только владельцу и группе); domain_users(группа домена)

#### В /etc/samba/smb.conf добавить секцию <!-- NAME -->

```CODE
[samba]                                                                                  
  path = /opt/data                                                                            
  browseable = yes                                                                            
  writable = yes                                                                              
  valid users = @domain_users                                                                 
  read only = no                                                                              
  create mask = 0660                                                                          
  directory mask = 0770                                                                       
 
```

> valid users = @domain_users(доступ только группе домена); create mask(права на новые файлы); directory mask(права на новые каталоги)

#### Добавление пользователя Samba <!-- NAME -->

```CODE
smbpasswd -a username
 
```

> создает пароль Samba для существующего системного пользователя

### Настройка Samba для конкретных пользователей <!-- HEAD -->

#### В /etc/samba/smb.conf добавить секцию <!-- NAME -->

```CODE
[samba]      
  path = /opt/data                                                                            
  browseable = yes                                                                            
  writable = yes                                                                              
  valid users = user1, user2, user3                                                           
  read only = no                                                                              
  write list = user1, user2                                                                   
 
```

> valid users(список разрешенных пользователей); write list(пользователи с правом записи)

### Описание основных опций Samba <!-- HEAD -->

#### Опции доступа <!-- NAME -->

```CODE
browseable = yes
  guest ok = yes                                                                              
  valid users = user1, @group1                                                                
  invalid users = user2                                                                       
  read only = no                                                                              
  writable = yes                                                                              
  write list = user1, @group1                                                                 
  read list = user2                                                                           
 
```

> browseable(видимость в сети); guest ok(гостевой доступ); valid users(разрешенные пользователи/группы); invalid users(запрещенные); write list(право записи); read list(только чтение)

#### Опции прав доступа <!-- NAME -->

```CODE
create mask = 0660
  directory mask = 0770                                                                       
  force user = nobody                                                                         
  force group = nogroup                                                                       
  inherit permissions = yes                                                                   
 
```

> create mask(права на файлы); directory mask(права на каталоги); force user/group(принудительный владелец); inherit permissions(наследование прав)

#### Опции безопасности <!-- NAME -->

```CODE
hosts allow = 192.168.1.0/24
  hosts deny = 192.168.2.0/24                                                                 
  max connections = 10                                                                        
 
```

> hosts allow(разрешенные сети); hosts deny(запрещенные сети); max connections(лимит подключений)

### Проверка <!-- HEAD -->

#### Проверка конфигурации <!-- NAME -->

```CODE
testparm     
 
```

> проверяет синтаксис smb.conf

#### Просмотр активных подключений <!-- NAME -->

```CODE
smbstatus                                                                                
 
```

> показывает подключенных пользователей и открытые файлы

#### Подключение с клиента Windows <!-- NAME -->

```CODE
\\192.168.1.1\samba                                                                      
 
```

> в проводнике Windows

#### Подключение с клиента Linux <!-- NAME -->

```CODE
smb://192.168.1.1/samba                                                                  
 
```

> в файловом менеджере или через smbclient

### SQL_install_MariaDB <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install -y mariadb-server                                                        
   
 
```

#### Включение и запуск службы <!-- NAME -->

```CODE
systemctl enable --now mariadb

 
```

### Настройка MariaDB <!-- HEAD -->

#### Установка пароля root <!-- NAME -->

```CODE
mariadb -u root
  ALTER USER 'root'@'localhost' IDENTIFIED BY 'P@ssw0rd';
  EXIT;

 
```

#### Разрешение доступа из сети в /etc/my.cnf.d/server.cnf <!-- NAME -->

```CODE
sed -i "s/skip-networking/#skip-networking/g" /etc/my.cnf.d/server.cnf
                                                                                              
 
```

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart mariadb                                                                
                                                                                              
 
```

#### Разрешение доступа для root по сети <!-- NAME -->

```CODE
mariadb -u root -p                                                                       
  GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';                                          
  UPDATE mysql.user SET host='%' WHERE user='root';                                           
  FLUSH PRIVILEGES;                                                                           
  EXIT;                                                                                       
 
```

> host='%' разрешает подключение с любого узла

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart mariadb                                                                
                                                                                              
 
```

### Проверка MariaDB <!-- HEAD -->

#### Проверка пользователей на сервере <!-- NAME -->

```CODE
mariadb -u root -p                                                                       
  SELECT user, HOST FROM mysql.user;                                                          
  EXIT;                                                                                       
                                                                                              
 
```

#### Удаленное подключение с клиента <!-- NAME -->

```CODE
mariadb -h IP_СЕРВЕРА -u root -p
                                                                                              
 
```

### Создание БД и пользователей <!-- HEAD -->

#### Создание базы данных <!-- NAME -->

```CODE
mariadb -u root -p                                                                       
  CREATE DATABASE db01;                                                                       
 
```

> db01 - имя создаваемой БД

#### Создание пользователя <!-- NAME -->

```CODE
CREATE USER 'user01'@'%' IDENTIFIED BY 'P@ssw0rd';                                       
 
```

> '%' означает подключение с любого хоста

#### Предоставление прав пользователю <!-- NAME -->

```CODE
GRANT ALL PRIVILEGES ON db01.* TO 'user01'@'%';                                          
  FLUSH PRIVILEGES;                                                                           
                                                                                              
 
```

#### Проверка существования БД и пользователей <!-- NAME -->

```CODE
SHOW DATABASES;                                                                          
  SELECT user, HOST FROM mysql.user;                                                          
  EXIT;
```

### SQL_install_MySQL <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка пакета <!-- NAME -->

```CODE
apt-get install -y MySQL-server                                                          
   
 
```

#### Включение и запуск службы <!-- NAME -->

```CODE
systemctl enable --now mysqld

 
```

### Настройка MySQL <!-- HEAD -->

#### Установка пароля root <!-- NAME -->

```CODE
mysql -u root
  ALTER USER 'root'@'localhost' IDENTIFIED BY 'P@ssw0rd';
  EXIT;

 
```

#### Разрешение доступа из сети в /etc/my.cnf.d/server.cnf <!-- NAME -->

```CODE
sed -i "s/skip-networking/#skip-networking/g" /etc/my.cnf.d/server.cnf
                                                                                              
 
```

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart mysqld                                                                 
                                                                                              
 
```

#### Разрешение доступа для root по сети <!-- NAME -->

```CODE
mysql -u root -p                                                                         
  GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';                                          
  UPDATE mysql.user SET host='%' WHERE user='root';                                           
  FLUSH PRIVILEGES;                                                                           
  EXIT;                                                                                       
 
```

> host='%' разрешает подключение с любого узла

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart mysqld                                                                 
                                                                                              
 
```

### Проверка MySQL <!-- HEAD -->

#### Проверка пользователей на сервере <!-- NAME -->

```CODE
mysql -u root -p                                                                         
  SELECT user, HOST FROM mysql.user;                                                          
  EXIT;                                                                                       
                                                                                              
 
```

#### Удаленное подключение с клиента <!-- NAME -->

```CODE
mysql -h IP_СЕРВЕРА -u root -p                                                           
                                                                                              
 
```

### Создание БД и пользователей <!-- HEAD -->

#### Создание базы данных <!-- NAME -->

```CODE
mysql -u root -p                                                                         
  CREATE DATABASE db01;                                                                       
 
```

> db01 - имя создаваемой БД

#### Создание пользователя <!-- NAME -->

```CODE
CREATE USER 'user01'@'%' IDENTIFIED BY 'P@ssw0rd';                                       
 
```

> '%' означает подключение с любого хоста

#### Предоставление прав пользователю <!-- NAME -->

```CODE
GRANT ALL PRIVILEGES ON db01.* TO 'user01'@'%';                                          
  FLUSH PRIVILEGES;                                                                           
                                                                                              
 
```

#### Проверка существования БД и пользователей <!-- NAME -->

```CODE
SHOW DATABASES;                                                                          
  SELECT user, HOST FROM mysql.user;                                                          
  EXIT;
```

### SQL_install_PostgreSQL <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get install -y postgresql16 postgresql16-server postgresql16-contrib                 
 
```

> postgresql16-contrib(дополнительные модули и утилиты)

#### Создание системных БД <!-- NAME -->

```CODE
/etc/init.d/postgresql initdb
                                                                                              
 
```

#### Запуск службы <!-- NAME -->

```CODE
systemctl enable --now postgresql                                                        
                                                                                              
 
```

#### Установка пароля для пользователя postgres <!-- NAME -->

```CODE
psql -U postgres                                                                         
  ALTER USER postgres WITH PASSWORD 'P@ssw0rd';                                               
  \q                                                                                          
                                                                                              
 
```

### Настройка <!-- HEAD -->

#### Разрешение доступа из сети в /var/lib/pgsql/data/postgresql.conf <!-- NAME -->

```CODE
listen_addresses = '*'                                                                   
 
```

> Найти listen_addresses = 'localhost' и заменить на '*'

> listen_addresses(адреса для прослушивания) {'*', 'localhost', '192.168.1.1'}

#### Перезапуск службы после изменения postgresql.conf <!-- NAME -->

```CODE
systemctl restart postgresql                                                             
                                                                                              
 
```

#### Настройка парольной аутентификации в /var/lib/pgsql/data/pg_hba.conf <!-- NAME -->

```CODE
host    all             all             0.0.0.0/0               md5                      
  host    replication     all             0.0.0.0/0               md5                         
 
```

> Добавить строки в конец файла перед секцией IPv6

> host(тип подключения) {host, local, hostssl}

> all(база данных) {all, имя_БД}

> all(пользователь) {all, имя_пользователя}

> 0.0.0.0/0(IP-адреса клиентов) {0.0.0.0/0, 192.168.1.0/24, конкретный_IP}

> md5(метод аутентификации) {md5, trust, reject, scram-sha-256}

> Первая строка для обычных подключений, вторая для репликации

#### Перезапуск службы после изменения pg_hba.conf <!-- NAME -->

```CODE
systemctl restart postgresql                                                             
                                                                                              
 
```

#### Создание базы данных и пользователя <!-- NAME -->

```CODE
psql -U postgres                                                                         
  CREATE DATABASE db01;                                                                       
  CREATE USER user01 WITH PASSWORD 'P@ssw0rd';
  GRANT ALL PRIVILEGES ON DATABASE db01 TO user01;                                            
  \q                                                                                          
 
```

> db01(имя создаваемой БД); user01(имя пользователя)

#### Создание нескольких баз данных и пользователей <!-- NAME -->

```CODE
psql -U postgres                                                                         
  CREATE DATABASE one;                                                                        
  CREATE DATABASE two;                                                                        
  CREATE USER oneuser WITH PASSWORD 'P@ssw0rd';                                               
  CREATE USER twouser WITH PASSWORD 'P@ssw0rd';                                               
  GRANT ALL PRIVILEGES ON DATABASE one TO oneuser;                                            
  GRANT ALL PRIVILEGES ON DATABASE two TO twouser;                                            
  \q                                                                                          
                                                                                              
 
```

#### Заполнение базы данных тестовыми данными <!-- NAME -->

```CODE
pgbench -U postgres -i one                                                               
  pgbench -U postgres -i two                                                                  
 
```

> Опционально, для тестирования производительности

### Проверка <!-- HEAD -->

#### Проверка открытого порта PostgreSQL <!-- NAME -->

```CODE
ss -tlpn | grep postgres                                                                 
 
```

> Показывает открытый порт 5432

#### Проверка БД и пользователей на сервере <!-- NAME -->

```CODE
psql -U postgres                                                                         
  SELECT datname FROM pg_database;                                                            
  SELECT usename, usesuper, usecreatedb FROM pg_catalog.pg_user;                              
  \q                                                                                          
 
```

> Показывает список баз данных и пользователей

#### Проверка таблиц в базе данных <!-- NAME -->

```CODE
psql -U postgres                                                                         
  \c one                                                                                      
  \dt+                                                                                        
  \c two                                                                                      
  \dt+                                                                                        
  \q              
 
```

> \c(подключение к БД); \dt+(список таблиц с размерами)

#### Локальное подключение на клиенте <!-- NAME -->

```CODE
psql -U user01 db01                                                                      
 
```

> Подключение к БД db01 от имени user01

#### Удалённое подключение на клиенте <!-- NAME -->

```CODE
psql -U user01 -h IP_сервера -d db01                                                     
 
```

> -h(хост сервера); -d(имя базы данных)

### squid_base_options <!-- HEAD -->

[Содержание](#Содержание)

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

### SSH <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка пакетов OpenSSH <!-- NAME -->

```CODE
sudo apt-get install openssh-server
 
```

> openssh-server(SSH-сервер, включает openssh-common автоматически)

#### Запуск и автозагрузка службы <!-- NAME -->

```CODE
sudo systemctl enable --now sshd                                                         
                                                                                              
 
```

### Проверка <!-- HEAD -->

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status sshd
                                                                                              
 
```

#### Проверка прослушиваемого порта <!-- NAME -->

```CODE
ss -tulpn | grep ssh                                                                     
                                                                                              
 
```

#### Проверка конфигурации <!-- NAME -->

```CODE
sshd -t                                                                                  
 
```

> Необязательно, проверяет синтаксис /etc/openssh/sshd_config перед перезапуском

#### Просмотр активных подключений <!-- NAME -->

```CODE
who                                                                                      
 
```

> Необязательно, показывает текущие SSH-сессии

#### Просмотр логов SSH <!-- NAME -->

```CODE
journalctl -u sshd                                                                       
 
```

> Необязательно, для диагностики проблем подключения

### Настройка сервера <!-- HEAD -->

#### Основной конфигурационный файл <!-- NAME -->

```CODE
/etc/openssh/sshd_config
                                                                                              
 
```

#### Настройка /etc/openssh/sshd_config <!-- NAME -->

```CODE
Port 22                                                                                  
  PasswordAuthentication yes                                                                  
  PermitRootLogin no                                                                          
  AllowUsers sshuser adminuser                                                                
  MaxAuthTries 3                                                                              
  PubkeyAuthentication yes                                                                    
 
 AuthorizedKeysFile .ssh/authorized_keys                                                     
  Banner /etc/ssh/banner.txt                                                                  
 
```

> Port(обычно 22, изменение необязательно); PasswordAuthentication(yes для начальной настройки, no после настройки ключей); PermitRootLogin no(рекомендуется); AllowUsers(необязательно, белый список); MaxAuthTries(необязательно, обычно 3-6); PubkeyAuthentication yes(обычно включено по умолчанию); AuthorizedKeysFile(стандартное расположение); Banner(необязательно)

#### Создание файла баннера /etc/ssh/banner.txt <!-- NAME -->

```CODE
************************************
  - Authorized Access Only          *                                                         
  - All activity is monitored        *                                                        
  ---
 
```

> Необязательно, содержимое баннера произвольное

#### Перезапуск службы после изменений <!-- NAME -->

```CODE
sudo systemctl restart sshd                                                              
                                                                                              
 
```

### Настройка аутентификации по ключам <!-- HEAD -->

#### Генерация SSH-ключа на клиенте <!-- NAME -->

```CODE
ssh-keygen -t ed25519 -f ~/.ssh/srv_ssh_key
 
```

> -t ed25519(современный стандарт, быстрее и безопаснее RSA); -f(имя файла, по умолчанию id_ed25519)

#### Копирование публичного ключа на сервер <!-- NAME -->

```CODE
ssh-copy-id -i ~/.ssh/srv_ssh_key.pub sshuser@192.168.11.67
 
```

> Публичный ключ добавляется в ~/.ssh/authorized_keys на сервере

### Настройка клиента <!-- HEAD -->

#### Настройка ~/.ssh/config для упрощения подключения <!-- NAME -->

```CODE
Host srv-hq  
      HostName 192.168.11.67                                                                  
      User sshuser                                                                            
      IdentityFile ~/.ssh/srv_ssh_key
      Port 22                                                                                 
 
```

> Необязательно, упрощает подключение. Port(указывать только если не 22)

#### Установка прав на config <!-- NAME -->

```CODE
chmod 600 ~/.ssh/config                                                                  
                                                                                              
 
```

#### Подключение к серверу по псевдониму <!-- NAME -->

```CODE
ssh srv-hq                                                                               
 
```

> Работает только при настроенном ~/.ssh/config

#### Подключение к серверу напрямую <!-- NAME -->

```CODE
ssh -i ~/.ssh/srv_ssh_key sshuser@192.168.11.67                                          
 
```

> Стандартный способ подключения с указанием ключа, для нестандартного порта использовать -p {8022]

#### Подключение по паролю <!-- NAME -->

```CODE
ssh sshuser@192.168.11.67                                                                
 
```

> Работает если PasswordAuthentication yes на сервере

### Создание пользователя <!-- HEAD -->

#### Создание пользователя <!-- NAME -->

```CODE
useradd -u 2026 -m -g users -G wheel sshuser
 
```

> -u(UID, необязательно); -m(создать домашний каталог); -g(основная группа, обычно users); -G wheel(для sudo)

#### Установка пароля <!-- NAME -->

```CODE
passwd sshuser
                                                                                              
 
```

#### Настройка sudo без пароля <!-- NAME -->

```CODE
visudo                                                                                   
 
```

> Добавить: %wheel ALL=(ALL:ALL) NOPASSWD: ALL. Необязательно, обычно sudo требует пароль

#### Проверка sudo <!-- NAME -->

```CODE
sudo whoami                                                                              
 
```

> Результат: root

### strongswan_ipsec <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка StrongSwan <!-- NAME -->

```CODE
apt-get install strongswan
                                                                                              
 
```

### Настройка первого маршрутизатора <!-- HEAD -->

#### Основной конфигурационный файл <!-- NAME -->

```CODE
/etc/strongswan/ipsec.conf
                                                                                              
 
```

#### Настройка /etc/strongswan/ipsec.conf на маршрутизаторе 10.10.10.1 <!-- NAME -->

```CODE
config setup                                                                             
                                                                                              
  conn nameConnect                                                                            
      authby=psk                                                                              
      keyexchange=ikev2                                                                       
                                                                                              
  leftid=10.10.10.1                                                                           
  left=10.10.10.1                                                                             
  leftsubnet=10.10.10.0/30                                                                    
                                                                                              
  rightid=10.10.10.2                                                                          
  right=10.10.10.2                                                                            
  rightsubnet=10.10.10.0/30                                                                   
                                                                                              
  auto=start                                                                                  
 
```

> authby=psk(аутентификация по общему ключу); keyexchange=ikev2(протокол обмена ключами); leftid(публичный идентификатор локального узла); left(локальный IP-адрес); leftsubnet(локальная подсеть); rightid(публичный идентификатор удалённого узла); right(удалённый IP-адрес); rightsubnet(удалённая подсеть); auto=start(автоматический запуск туннеля)

#### Файл с общими ключами <!-- NAME -->

```CODE
/etc/strongswan/ipsec.secrets                                                            
                                                                                              
 
```

#### Настройка /etc/strongswan/ipsec.secrets на маршрутизаторе 10.10.10.1 <!-- NAME -->

```CODE
10.10.10.1 10.10.10.2 : PSK "P@ssw0rd"                                                   
 
```

> Формат: локальный_IP удалённый_IP : PSK "пароль"

### Настройка второго маршрутизатора <!-- HEAD -->

#### Настройка /etc/strongswan/ipsec.conf на маршрутизаторе 10.10.10.2 <!-- NAME -->

```CODE
config setup 
                                                                                              
  conn nameConnect                                                                            
      authby=psk
      keyexchange=ikev2                                                                       
                                                                                              
  leftid=10.10.10.2                                                                           
  left=10.10.10.2                                                                             
  leftsubnet=10.10.10.0/30                                                                    
                                                                                              
  rightid=10.10.10.1                                                                          
  right=10.10.10.1                                                                            
  rightsubnet=10.10.10.0/30                                                                   
                                                                                              
  auto=start                                                                                  
 
```

> Зеркальная конфигурация: left и right меняются местами

#### Настройка /etc/strongswan/ipsec.secrets на маршрутизаторе 10.10.10.2 <!-- NAME -->

```CODE
10.10.10.2 10.10.10.1 : PSK "P@ssw0rd"                                                   
 
```

> Тот же пароль, адреса в обратном порядке

### Запуск <!-- HEAD -->

#### Запуск и автозагрузка службы на обоих маршрутизаторах <!-- NAME -->

```CODE
systemctl enable --now strongswan-starter ipsec
                                                                                              
 
```

### Проверка <!-- HEAD -->

#### Проверка статуса туннеля <!-- NAME -->

```CODE
ipsec status
 
```

> Показывает состояние IPsec соединений

#### Проверка связности через туннель <!-- NAME -->

```CODE
ping 10.10.10.2                                                                          
 
```

> С первого маршрутизатора, с второго ping 10.10.10.1

### sudo <!-- HEAD -->

[Содержание](#Содержание)

### Установка <!-- HEAD -->

#### Установка sudo <!-- NAME -->

```CODE
apt-get install sudo
 
```

> sudo(выполнение команд от имени другого пользователя, обычно root)

### Создание пользователя <!-- HEAD -->

#### Создание пользователя с параметрами <!-- NAME -->

```CODE
useradd -m -g users -G wheel -s /bin/bash username
 
```

> -m(создать домашний каталог); -g(основная группа); -G(дополнительные группы); -s(оболочка по умолчанию /bin/bash)

#### Создание пользователя с указанным UID <!-- NAME -->

```CODE
useradd -u 2026 -m -g users -G wheel username
 
```

> -u(указать конкретный UID)

#### Установка пароля пользователю <!-- NAME -->

```CODE
passwd username                                                                          
                                                                                              
 
```

#### Создание пользователя интерактивно <!-- NAME -->

```CODE
adduser username                                                                         
 
```

> Либо интерактивный режим с запросом всех параметров

### Настройка sudo <!-- HEAD -->

#### Основной конфигурационный файл <!-- NAME -->

```CODE
/etc/sudoers 
                                                                                              
 
```

#### Редактирование конфигурации sudo <!-- NAME -->

```CODE
visudo                                                                                   
 
```

> Безопасное редактирование /etc/sudoers с проверкой синтаксиса

#### Предоставление sudo группе wheel <!-- NAME -->

```CODE
%wheel ALL=(ALL:ALL) ALL                                                                 
 
```

> Пользователи группы wheel могут выполнять любые команды через sudo с вводом пароля

#### Предоставление sudo без пароля группе wheel <!-- NAME -->

```CODE
%wheel ALL=(ALL:ALL) NOPASSWD: ALL                                                       
 
```

> Пользователи группы wheel могут выполнять sudo без ввода пароля

#### Предоставление sudo конкретному пользователю <!-- NAME -->

```CODE
username ALL=(ALL:ALL) ALL                                                               
 
```

> Конкретный пользователь может выполнять любые команды через sudo

#### Предоставление sudo для конкретных команд <!-- NAME -->

```CODE
username ALL=(ALL) /usr/bin/systemctl, /usr/bin/apt-get                                  
 
```

> Пользователь может выполнять только указанные команды через sudo

#### Добавление пользователя в группу wheel <!-- NAME -->

```CODE
usermod -aG wheel username                                                               
 
```

> -aG(добавить в дополнительные группы, не удаляя из существующих)

### Управление пользователями <!-- HEAD -->

#### Изменение оболочки пользователя <!-- NAME -->

```CODE
usermod -s /bin/bash username
 
```

> -s(изменить оболочку по умолчанию)

#### Изменение домашнего каталога <!-- NAME -->

```CODE
usermod -d /home/newdir username                                                         
 
```

> -d(изменить домашний каталог)

#### Блокировка пользователя <!-- NAME -->

```CODE
usermod -L username                                                                      
 
```

> -L(заблокировать учётную запись, запретить вход)

#### Разблокировка пользователя <!-- NAME -->

```CODE
usermod -U username                                                                      
 
```

> -U(разблокировать учётную запись)

#### Удаление пользователя <!-- NAME -->

```CODE
userdel username                                                                         
 
```

> Удаляет пользователя, но сохраняет домашний каталог

#### Удаление пользователя с домашним каталогом <!-- NAME -->

```CODE
userdel -r username                                                                      
 
```

> -r(удалить вместе с домашним каталогом)

#### Просмотр групп пользователя <!-- NAME -->

```CODE
groups username                                                                          
 
```

> Показывает все группы пользователя

#### Просмотр информации о пользователе <!-- NAME -->

```CODE
id username                                                                              
 
```

> Показывает UID, GID и группы пользователя

### Проверка <!-- HEAD -->

#### Проверка sudo <!-- NAME -->

```CODE
sudo whoami  
 
```

> Результат: root

#### Проверка выполнения команды от другого пользователя <!-- NAME -->

```CODE
sudo -u username whoami                                                                  
 
```

> -u(выполнить от имени указанного пользователя), результат: username

#### Просмотр прав sudo текущего пользователя <!-- NAME -->

```CODE
sudo -l                                                                                  
 
```

> Показывает какие команды может выполнять пользователь через sudo

#### Просмотр истории sudo <!-- NAME -->

```CODE
journalctl -u sudo                                                                       
 
```

> Показывает логи выполнения команд через sudo

#### Просмотр всех пользователей системы <!-- NAME -->

```CODE
cat /etc/passwd                                                                          
 
```

> Список всех пользователей с их параметрами

#### Просмотр всех групп системы <!-- NAME -->

```CODE
cat /etc/group                                                                           
 
```

> Список всех групп и их членов

### sudo-schema-samba <!-- HEAD -->

[Содержание](#Содержание)

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

### systemd-timesyncd <!-- HEAD -->

[Содержание](#Содержание)

### Установка и настройка systemd-timesyncd <!-- HEAD -->

#### Проверка установки <!-- NAME -->

```CODE
systemctl status systemd-timesyncd
 
```

> systemd-timesyncd(встроенный NTP-клиент/сервер systemd, обычно уже установлен)

#### Остановка и отключение chrony <!-- NAME -->

```CODE
systemctl stop chronyd
  systemctl disable chronyd
 
```

> systemd-timesyncd и chrony несовместимы на одной машине, работает только один NTP-сервис

### Настройка NTP-сервера <!-- HEAD -->

#### Основной конфигурационный файл <!-- NAME -->

```CODE
/etc/systemd/timesyncd.conf

 
```

#### Настройка /etc/systemd/timesyncd.conf для сервера <!-- NAME -->

```CODE
[Time]
  NTP=ntp2.vniiftri.ru
  FallbackNTP=0.pool.ntp.org 1.pool.ntp.org
 
```

> NTP(основные NTP-серверы через пробел); FallbackNTP(резервные серверы)

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart systemd-timesyncd

 
```

#### Включение службы <!-- NAME -->

```CODE
systemctl enable systemd-timesyncd

 
```

### Разрешение NTP в firewall <!-- HEAD -->

#### Разрешение UDP 123 в iptables <!-- NAME -->

```CODE
iptables -A INPUT -p udp --dport 123 -j ACCEPT
  iptables -A OUTPUT -p udp --sport 123 -j ACCEPT
 
```

> UDP порт 123 используется для NTP

#### Разрешение UDP 123 в nftables <!-- NAME -->

```CODE
nft add rule inet filter input udp dport 123 accept
  nft add rule inet filter output udp sport 123 accept

 
```

### Проверка NTP-сервера <!-- HEAD -->

#### Проверка статуса синхронизации <!-- NAME -->

```CODE
timedatectl status
 
```

> Показывает System clock synchronized, NTP service

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status systemd-timesyncd

 
```

#### Подробная информация о синхронизации <!-- NAME -->

```CODE
timedatectl timesync-status
 
```

> Показывает сервер, stratum, задержку, смещение

#### Проверка открытого UDP-порта 123 <!-- NAME -->

```CODE
ss -ulnp | grep 123

 
```

#### Просмотр логов <!-- NAME -->

```CODE
journalctl -u systemd-timesyncd

 
```

### Настройка NTP-клиента <!-- HEAD -->

#### Остановка и отключение chrony <!-- NAME -->

```CODE
systemctl stop chronyd
  systemctl disable chronyd

 
```

#### Настройка /etc/systemd/timesyncd.conf для клиента <!-- NAME -->

```CODE
[Time]
  NTP=192.168.11.67
  FallbackNTP=ntp2.vniiftri.ru
 
```

> NTP(локальный NTP-сервер); FallbackNTP(резервный внешний сервер)

#### Перезапуск службы <!-- NAME -->

```CODE
systemctl restart systemd-timesyncd

 
```

#### Включение службы <!-- NAME -->

```CODE
systemctl enable systemd-timesyncd

 
```

### Проверка клиента <!-- HEAD -->

#### Проверка синхронизации <!-- NAME -->

```CODE
timedatectl status

 
```

#### Подробная информация <!-- NAME -->

```CODE
timedatectl timesync-status

 
```

#### Включение NTP-синхронизации <!-- NAME -->

```CODE
timedatectl set-ntp true
 
```

> Включает автоматическую синхронизацию времени

#### Проверка синхронизации с сервером <!-- NAME -->

```CODE
ntpdate -q 192.168.11.67
 
```

> -q(запрос без изменения времени), показывает смещение времени

### systemd_backup <!-- HEAD -->

[Содержание](#Содержание)

### Настройка службы резервного копирования <!-- HEAD -->

#### Создание директории для резервных копий <!-- NAME -->

```CODE
mkdir -p /var/backup
                                                                                              
 
```

#### Создание службы /etc/systemd/system/backup.service <!-- NAME -->

```CODE
[Unit]                                                                                   
  Description=Backup shared folder to /var/backup                                             
  After=network.target                                                                        
                                                                                              
  [Service]                                                                                   
  Type=oneshot                                                                                
  ExecStart=/bin/bash -c 'tar -czf /var/backup/shared-$(date +%%Y-%%m-%%d-%%H-%%M-%%S).tar.gz 
  /path/to/shared/folder'                                                                     
 
```

> Type=oneshot(служба завершается после выполнения команды); ExecStart(команда создания архива с датой и временем); %%(двойной процент для экранирования в systemd)

#### Создание таймера /etc/systemd/system/backup.timer <!-- NAME -->

```CODE
[Unit]       
  Description=Run backup.service daily at 20:00                                               
                                                                                              
  [Timer]                                                                                     
  OnCalendar=20:00                                                                            
  Persistent=true                                                                             
                                                                                              
  [Install]                                                                                   
  WantedBy=timers.target                                                                      
 
```

> OnCalendar=20:00(запуск каждый день в 20:00); Persistent=true(выполнить пропущенную задачу при загрузке, если система была выключена)

### Запуск <!-- HEAD -->

#### Перезагрузка конфигурации systemd <!-- NAME -->

```CODE
systemctl daemon-reload
 
```

> Применяет изменения после создания или редактирования unit-файлов

#### Включение и запуск таймера <!-- NAME -->

```CODE
systemctl enable --now backup.timer                                                      
                                                                                              
 
```

### Проверка <!-- HEAD -->

#### Просмотр активных таймеров <!-- NAME -->

```CODE
systemctl list-timers
 
```

> Показывает все таймеры, время следующего запуска и последнего выполнения

#### Проверка статуса таймера <!-- NAME -->

```CODE
systemctl status backup.timer                                                            
                                                                                              
 
```

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status backup.service                                                          
                                                                                              
 
```

#### Ручной запуск службы резервного копирования <!-- NAME -->

```CODE
systemctl start backup.service                                                           
 
```

> Для проверки работы службы без ожидания таймера

#### Просмотр созданных архивов <!-- NAME -->

```CODE
ls -lh /var/backup                                                                       
 
```

> -lh(список с размерами в читаемом формате)

#### Просмотр логов службы <!-- NAME -->

```CODE
journalctl -u backup.service                                                             
 
```

> Показывает логи выполнения резервного копирования

#### Просмотр логов таймера <!-- NAME -->

```CODE
journalctl -u backup.timer                                                               
                                                                                              
 
```

#### Дополнительные варианты OnCalendar <!-- LIST -->
- OnCalendar=daily (каждый день в 00:00)
- OnCalendar=weekly (каждую неделю в понедельник 00:00)
- OnCalendar=--* 02:00:00 (каждый день в 02:00)
- OnCalendar=Mon,Fri 18:00 (понедельник и пятница в 18:00)
- OnCalendar=*:0/15 (каждые 15 минут)
- OnCalendar=hourly (каждый час)

### timedatectl <!-- HEAD -->

[Содержание](#Содержание)

### Управление временем через timedatectl <!-- HEAD -->

#### Просмотр текущего времени и настроек <!-- NAME -->

```CODE
timedatectl  
 
```

> Показывает локальное время, UTC, часовой пояс, синхронизацию NTP

#### Просмотр статуса синхронизации времени <!-- NAME -->

```CODE
timedatectl status                                                           
 
```

> Показывает полную информацию

### Настройка времени <!-- HEAD -->

#### Установка текущей даты и времени <!-- NAME -->

```CODE
timedatectl set-time "2026-05-31 10:30:00"
 
```

> Формат: YYYY-MM-DD HH:MM:SS

#### Установка только даты <!-- NAME -->

```CODE
timedatectl set-time "2026-05-31"                                            
                                                                                  
 
```

#### Установка только времени <!-- NAME -->

```CODE
timedatectl set-time "10:30:00"                                              
                                                                                  
 
```

### Настройка часового пояса <!-- HEAD -->

#### Просмотр текущего часового пояса <!-- NAME -->

```CODE
timedatectl show-timezones
 
```

> Показывает список всех доступных часовых поясов

#### Поиск часового пояса <!-- NAME -->

```CODE
timedatectl list-timezones | grep Moscow                                     
                                                                                  
 
```

#### Установка часового пояса <!-- NAME -->

```CODE
timedatectl set-timezone Europe/Moscow                                       
 
```

> Часовой пояс Москвы

#### Установка UTC <!-- NAME -->

```CODE
timedatectl set-timezone UTC                                                 
                                                                                  
 
```

### Настройка NTP-синхронизации <!-- HEAD -->

#### Включение NTP-синхронизации <!-- NAME -->

```CODE
timedatectl set-ntp true
 
```

> Включает автоматическую синхронизацию времени через systemd-timesyncd

#### Отключение NTP-синхронизации <!-- NAME -->

```CODE
timedatectl set-ntp false                                                    
 
```

> Отключает автоматическую синхронизацию, позволяет устанавливать время вручную

#### Проверка статуса NTP-синхронизации <!-- NAME -->

```CODE
timedatectl timesync-status                                                  
 
```

> Показывает сервер, stratum, задержку, смещение времени

### Настройка аппаратных часов <!-- HEAD -->

#### Синхронизация системного времени с аппаратными часами <!-- NAME -->

```CODE
hwclock --systohc
 
```

> Записывает системное время в аппаратные часы (RTC)

#### Синхронизация аппаратных часов с системным временем <!-- NAME -->

```CODE
hwclock --hctosys                                                            
 
```

> Устанавливает системное время из аппаратных часов

#### Просмотр аппаратных часов <!-- NAME -->

```CODE
hwclock --show                                                               
 
```

> Показывает время из RTC

#### Установка аппаратных часов в UTC <!-- NAME -->

```CODE
timedatectl set-local-rtc 0                                                  
 
```

> 0(RTC в UTC), рекомендуется для Linux

#### Установка аппаратных часов в локальное время <!-- NAME -->

```CODE
timedatectl set-local-rtc 1                                                  
 
```

> 1(RTC в локальном времени), используется для совместимости с Windows

### Проверка <!-- HEAD -->

#### Просмотр всех свойств <!-- NAME -->

```CODE
timedatectl show
 
```

> Показывает все параметры в формате ключ=значение

#### Просмотр конкретного свойства <!-- NAME -->

```CODE
timedatectl show -p Timezone                                                 
 
```

> -p(конкретное свойство): Timezone, NTPSynchronized, LocalRTC

#### Просмотр логов службы времени <!-- NAME -->

```CODE
journalctl -u systemd-timesyncd                                              
                                                                                  
 
```

#### Примеры часовых поясов <!-- LIST -->
- Europe/Moscow (Москва, UTC+3)
- Asia/Yekaterinburg (Екатеринбург, UTC+5)
- Asia/Novosibirsk (Новосибирск, UTC+7)
- Asia/Vladivostok (Владивосток, UTC+10)
- UTC (Всемирное координированное время)

### wireguard <!-- HEAD -->

[Содержание](#Содержание)

### Установка WireGuard <!-- HEAD -->

#### Установка пакетов <!-- NAME -->

```CODE
apt-get update && apt-get install -y wireguard-tools wireguard-tools-wg-quick
 
```

> wireguard-tools(утилиты для управления WireGuard); wireguard-tools-wg-quick(утилита wg-quick для быстрой настройки)

### Настройка сервера FW-L <!-- HEAD -->

#### Создание директории для ключей <!-- NAME -->

```CODE
mkdir -p /etc/wireguard/keys
                                                                                  
 
```

#### Генерация ключей сервера и клиента <!-- NAME -->

```CODE
cd /etc/wireguard/keys                                                       
  wg genkey | tee srv-sec.key | wg pubkey > srv-pub.key                           
  wg genkey | tee cli-sec.key | wg pubkey > cli-pub.key                           
 
```

> wg genkey(генерация приватного ключа); wg pubkey(генерация публичного ключа из приватного); srv-sec.key(приватный ключ сервера); srv-pub.key(публичный ключ сервера); cli-sec.key(приватный ключ клиента); cli-pub.key(публичный ключ клиента)

#### Создание конфигурационного файла /etc/wireguard/wg0.conf <!-- NAME -->

```CODE
[Interface]
  Address = 10.20.30.1/30                                                         
  ListenPort = 51820                                                              
  PrivateKey = <содержимое srv-sec.key>                                           
                                                                                  
  [Peer]                                                                          
  PublicKey = <содержимое cli-pub.key>                                            
  AllowedIPs = 10.20.30.2/32, 172.16.100.0/24                                     
 
```

> [Interface](настройки сервера); Address(адрес в VPN-сети); ListenPort(порт сервера, обычно 51820); PrivateKey(приватный ключ сервера); [Peer](настройки клиента); PublicKey(публичный ключ клиента); AllowedIPs(разрешённые маршруты от клиента)

#### Включение и автозагрузка туннельного интерфейса <!-- NAME -->

```CODE
systemctl enable --now wg-quick@wg0
                                                                                  
 
```

### Настройка клиента FW-R <!-- HEAD -->

#### Создание директории для ключей <!-- NAME -->

```CODE
mkdir -p /etc/wireguard/keys
                                                                                  
 
```

#### Копирование ключей с сервера <!-- NAME -->

```CODE
cd /etc/wireguard/keys
  scp root@4.4.4.2:/etc/wireguard/keys/cli-sec.key ./                             
  scp root@4.4.4.2:/etc/wireguard/keys/srv-pub.key ./                             
 
```

> Копируем приватный ключ клиента и публичный ключ сервера

#### Создание конфигурационного файла /etc/wireguard/wg0.conf <!-- NAME -->

```CODE
[Interface]                                                                  
  Address = 10.20.30.2/30                                                         
  PrivateKey = <содержимое cli-sec.key>                                           
                                                                                  
  [Peer]                                                                          
  PublicKey = <содержимое srv-pub.key>                                            
  Endpoint = 4.4.4.2:51820                                                        
  AllowedIPs = 10.20.30.1/32, 192.168.100.0/24                                    
  PersistentKeepalive = 25                                                        
 
```

> Endpoint(адрес и порт сервера); AllowedIPs(разрешённые маршруты к серверу); PersistentKeepalive(интервал проверки соединения в секундах, обычно 25)

#### Включение и автозагрузка туннельного интерфейса <!-- NAME -->

```CODE
systemctl enable --now wg-quick@wg0
                                                                                  
 
```

### Разрешение WireGuard в firewall <!-- HEAD -->

#### Разрешение UDP 51820 в iptables на сервере <!-- NAME -->

```CODE
iptables -A INPUT -p udp --dport 51820 -j ACCEPT
 
```

> UDP порт 51820 используется для WireGuard

#### Разрешение UDP 51820 в nftables на сервере <!-- NAME -->

```CODE
nft add rule inet filter input udp dport 51820 accept                        
                                                                                  
 
```

### Проверка <!-- HEAD -->

#### Проверка статуса туннеля <!-- NAME -->

```CODE
wg show wg0  
 
```

> Показывает информацию о туннеле, пиры, передачу данных

#### Проверка интерфейса wg0 <!-- NAME -->

```CODE
ip -c a | grep wg0                                                           
                                                                                  
 
```

#### Проверка статуса службы <!-- NAME -->

```CODE
systemctl status wg-quick@wg0                                                
                                                                                  
 
```

#### Проверка связности через туннель <!-- NAME -->

```CODE
ping 10.20.30.2                                                              
 
```

> С сервера пинг клиента, с клиента ping 10.20.30.1

#### Проверка связности из LAN LEFT в LAN RIGHT <!-- NAME -->

```CODE
ping 172.16.100.10                                                           
 
```

> С машины в сети 192.168.100.0/24 пинг в сеть 172.16.100.0/24

### Управление туннелем <!-- HEAD -->

#### Остановка туннеля <!-- NAME -->

```CODE
systemctl stop wg-quick@wg0
                                                                                  
 
```

#### Запуск туннеля <!-- NAME -->

```CODE
systemctl start wg-quick@wg0                                                 
                                                                                  
 
```

#### Перезапуск туннеля <!-- NAME -->

```CODE
systemctl restart wg-quick@wg0                                               
                                                                                  
 
```

#### Ручное поднятие интерфейса <!-- NAME -->

```CODE
wg-quick up wg0                                                              
                                                                                  
 
```

#### Ручное отключение интерфейса <!-- NAME -->

```CODE
wg-quick down wg0                                                            
                                                                                  
 
```

### Настройка динамической маршрутизации OSPF <!-- HEAD -->

#### Установка FRR на обоих серверах <!-- NAME -->

```CODE
apt-get install -y frr
 
```

> FRR(Free Range Routing, пакет для динамической маршрутизации OSPF, BGP)

#### Изменение конфигурации WireGuard на сервере <!-- NAME -->

```CODE
[Interface]                                                                  
  Address = 10.20.30.1/30                                                         
  ListenPort = 51820                                                              
  PrivateKey = <содержимое srv-sec.key>                                           
  Table = off                                                                     
                                                                                  
  [Peer]                                                                          
  PublicKey = <содержимое cli-pub.key>
  AllowedIPs = 10.20.30.2/32                                                      
 
```

> Table = off(отключить автоматическое управление маршрутами, маршруты будут управляться через OSPF); AllowedIPs(только адрес клиента, без сетей)

#### Изменение конфигурации WireGuard на клиенте <!-- NAME -->

```CODE
[Interface]  
  Address = 10.20.30.2/30                                                         
  PrivateKey = <содержимое cli-sec.key>                                           
  Table = off                                                                     
                                                                                  
  [Peer]                                                                          
  PublicKey = <содержимое srv-pub.key>                                            
  Endpoint = 4.4.4.2:51820                                                        
  AllowedIPs = 10.20.30.1/32                                                      
  PersistentKeepalive = 25                                                        
                                                                                  
 
```

#### Перезапуск туннеля на обоих серверах <!-- NAME -->

```CODE
systemctl restart wg-quick@wg0                                               
                                                                                  
 
```

#### Включение демона OSPF на обоих серверах <!-- NAME -->

```CODE
sed -i 's/ospfd=no/ospfd=yes/g' /etc/frr/daemons                             
                                                                                  
 
```

#### Запуск и автозагрузка FRR на обоих серверах <!-- NAME -->

```CODE
systemctl enable --now frr                                                   
                                                                                  
 
```

#### Настройка OSPF на сервере FW-L <!-- NAME -->

```CODE
vtysh                                                                        
  configure terminal                                                              
  router ospf     
  passive-interface default                                                       
  network 10.20.30.0/30 area 0
  network 192.168.100.0/24 area 0                                                 
  exit                                                                            
  interface wg0                                                                   
  no ip ospf passive                                                              
  exit                                                                            
  end                                                                             
  wr mem                                                                          
 
```

> vtysh(интерактивная оболочка FRR); router ospf(включить OSPF); passive-interface default(все интерфейсы пассивные по умолчанию); network(объявить сети в OSPF area 0); no ip ospf passive(сделать wg0 активным для OSPF); wr mem(сохранить конфигурацию)

#### Настройка OSPF на клиенте FW-R <!-- NAME -->

```CODE
vtysh
  configure terminal                                                              
  router ospf                                                                     
  passive-interface default
  network 10.20.30.0/30 area 0                                                    
  network 172.16.100.0/24 area 0                                                  
  exit                                                                            
  interface wg0                                                                   
  no ip ospf passive                                                              
  exit            
  end                                                                             
  wr mem          
                                                                                  
 
```

#### Проверка OSPF соседей <!-- NAME -->

```CODE
vtysh -c "show ip ospf neighbor"                                             
 
```

> Должен показать соседа в состоянии Full

#### Проверка маршрутов OSPF <!-- NAME -->

```CODE
ip -c r | grep ospf                                                          
 
```

> Показывает маршруты, полученные через OSPF

#### Проверка таблицы маршрутизации OSPF <!-- NAME -->

```CODE
vtysh -c "show ip route ospf"                                                
                                                                                  
 
```

#### Проверка статуса OSPF <!-- NAME -->

```CODE
vtysh -c "show ip ospf"                                                      
                  
 
```

#### Проверка интерфейсов OSPF <!-- NAME -->

```CODE
vtysh -c "show ip ospf interface"
```

### Zabbix_agent <!-- HEAD -->

[Содержание](#Содержание)

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

### Zabbix_web-interface <!-- HEAD -->

[Содержание](#Содержание)

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
