from locust import HttpUser, task, between


class PerformanceTestUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def test_performance_endpoint(self):
        response = self.client.get("/perfomance_testing")
        if response.status_code != 200:
            print(f"Ошибка: {response.status_code}, {response.text}")
