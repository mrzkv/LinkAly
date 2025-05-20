Authentication Service - part of ALSMS
-----
> [!WARNING]
> All configuration in this branch.
> To run the service as a separate 
> service on a separate machine.  
> If you want to try everything at
> once, then in main the configuration
> is set to run on 1 machine

## How to run:
#### Windows(PowerShell)/Linux(Shell) without smtp:
~~~
git clone https://github.com/mrzkv/LinkAly.git -b auth-service
cd LinkAly/AuthenticationService
docker compose up -d
~~~
If you want to run service with smtp change .env.template file smtp settings

#### When the launch is complete, you will be able to access the application and his infrastructure.  

**FastAPI** docs: [localhost:8000/docs](http://localhost:8000/docs)  


**Grafana**: [localhost:3000](http://localhost:3000)  
username - root  
password - root

**PgAdmin**: [localhost:4000](http://localhost:4000)  
username - root@admin.tech  
password - root

**Postgres**: jdbc:postgresql://0.0.0.0:8312/root   
port: 8312  
user: root  
password: root  
db: root  


## Responsibilities:
    1. Manage Users
    2. Public keys distribution

## Technologies:
 1. Programming languages:
    - Python
 2. Storages:
    - PostgreSQL
 3. Authentication: 
    - JWT
 4. Deploy:
    - Docker compose
 5. Infrastructure:
    - Grafana
    - Loki
    - Promtail
    - Prometheus

### Entities:
 - Users


### Tables: 
#### Users

| id    | login | email          | hashed_password | 
|-------|-------|----------------|-----------------|
| **1** | mrzkv | mrzkv@tech.com | {argon2-hash}   |
| **2** | user  | user@email.com | {argon2-hash}   | 

