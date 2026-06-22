import requests
import urls

class CreateCourierAPI:
    def create_courier(self, login, password, first_name=None):
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(
            f"{urls.base_url}{urls.create_courier_endpoint}",
            json=payload
        )
        return response


class LoginCourierAPI:
    def login_courier(self, login, password):
        payload = {
            "login": login,
            "password": password,
        }

        response = requests.post(f"{urls.base_url}{urls.login_courier_endpoint}", json=payload)

        return response
