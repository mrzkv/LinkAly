Authentication Service - part of ALSMS
-----
> [!WARNING]
> All configuration in this branch.
> To run the service as a separate 
> service on a separate machine.  
> If you want to try everything at
> once, then in main the configuration
> is set to run on 1 machine

### Responsibilities:
    1. Manage Users
    2. Public keys distribution

### Technologies:
 1. Programming languages:
    - Python
 2. Storages:
    - PostgreSQL
 3. Authentication: 
    - JWT
 4. Deploy:
    - Docker Compose
 5. Logging:
    - Grafana
    - Loki
    - Promtail

### Entities:
 - Users


### Tables: 
#### Users

| id    | login | email          | hashed_password | 
|-------|-------|----------------|-----------------|
| **1** | mrzkv | mrzkv@tech.com | {argon2-hash}   |
| **2** | user  | user@email.com | {argon2-hash}   | 

