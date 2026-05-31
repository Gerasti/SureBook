
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
