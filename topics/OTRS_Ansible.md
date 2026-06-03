
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
