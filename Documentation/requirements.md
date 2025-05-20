Analytic Link Shortening Micro-Services (ALSMS)
-----
### Business-Plan:
 - **Target**: Create ALSMS
 - **Solving problem**: Analytic for users, who need statistics of redirects
 - **Growth points**: Add more analytic features.

### Technologies:
 1. Programming languages: 
    - Golang
    - Python
 2. Storages:
    - Relational: PostgreSQL
    - Cache: Redis
 3. Authentication: 
    - JWT
 4. Deploy:
    - Docker Compose
 5. Logging:
    - Grafana
    - Loki
 6. Monitoring:
    - Prometheus
 7. Security, Proxy:
    - Nginx
 8. Development: 
    - CI/CD on GitHub Actions
 9. Message broker:
    - Kafka
 

### Services and his Responsibilities: 
    1. Authentication Service (Python, FastAPI, PostgreSQL)
        1. Manage Users
        2. Public keys distribution
    2. Analytic Service (Python, FastAPI, PostgreSQL)
        1. Create Pairs: {real_url: short_url} -> Send to Redirect Service 
        2. Redirect Analytic: charts, dashboards
    3. Redirect Service (Golang, Fiber, PostgreSQL, Redis)
        1. Redirect users
        2. Send to kafka user data.
        3. Reciving pairs {real_url:short_url} <- Analytic Service/Unauthorized users


### Entities:
 - User


