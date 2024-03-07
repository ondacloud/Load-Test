import time
from locust import HttpUser, task

class Zombie(HttpUser):
    @task
    def get_url(self):
        self.client.get('/v1/static')
        
    @task
    def get_healthz(self):
        self.client.get("/healthz")
