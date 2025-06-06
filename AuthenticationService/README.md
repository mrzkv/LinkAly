Authentication Service - part of ALSMS
-----
> [!WARNING]
> All configuration in this branch.
> To run the service as a separate 
> service on a separate machine.  
> If you want to try everything at
> once, then in the main the configuration
> is set to run on one machine

## How to run:
#### Windows(PowerShell)/Linux(Shell):
~~~
git clone https://github.com/mrzkv/LinkAly.git -b auth-service
cd LinkAly/AuthenticationService
docker compose up -d
~~~
#### When the launch is complete, you will be able to access the application and his infrastructure.  

**FastAPI** docs: [localhost:8000/docs](http://localhost:8000/docs)  

**MailDev**: [localhost:1080](http://localhost:1080) 

**Grafana**: [localhost:3000](http://localhost:3000)  
username - root  
password - root

**Postgres**: jdbc:postgresql://0.0.0.0:8312/root   
port - 8312  
user - root  
password - root  
db - root  


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

### Application config:
- .env.template
- src/core/config.py
- docker-compose.yaml

### Tables: 
#### Users

| id                                                  | login | email          | hashed_password | 
|-----------------------------------------------------|-------|----------------|-----------------|
| **1**                                               | mrzkv | mrzkv@tech.com | {argon2-hash}   |
| **2**                                               | user  | user@email.com | {argon2-hash}   | 
| **3**                                               | user2 | None           | {argon2-hash}   |
