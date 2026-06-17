import requests


class CreateCourierAPI:
    def __init__(self, base_url="https://qa-scooter.education-services.ru"):
        self.base_url = base_url
        self.create_courier_endpoint = "/api/v1/courier"

    def create_courier(self, login, password, first_name=None):
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(
            f"{self.base_url}{self.create_courier_endpoint}",
            json=payload
        )
        return response


class LoginCourierAPI:
    def __init__(self, base_url="https://qa-scooter.education-services.ru"):
        self.base_url = base_url
        self.login_courier_endpoint = "/api/v1/courier/login"

    def login_courier(self, login, password):
        payload = {
            "login": login,
            "password": password,
        }

        response = requests.post(f"{self.base_url}{self.login_courier_endpoint}", json=payload)

        return response


