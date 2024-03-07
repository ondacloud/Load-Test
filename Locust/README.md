## Install Package
```
sudo yum install -y python3 python3-devel gcc
sudo pip3 install locust
```

## Load Test Code
```python
import time
from locust import HttpUser, task

class Zombie(HttpUser):
    @task
    def get_url(self):
        self.client.get('/v1/static')
        
    @task
    def get_healthz(self):
        self.client.get("/healthz")

```

## Start Locust
```
locust -f locust.py
```