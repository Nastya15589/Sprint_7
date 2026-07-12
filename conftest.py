import string
import random
import pytest
import requests
import urls


@pytest.fixture
def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    create_response = requests.post(
        f"{urls.base_url}{urls.create_courier_endpoint}",
        json=payload
    )

    if create_response.status_code != 201:
        pytest.fail(f"Не удалось создать курьера! Статус: {create_response.status_code}, Ответ: {create_response.text}")

    auth_response = requests.post(
        f"{urls.base_url}{urls.login_courier_endpoint}",
        json={"login": login, "password": password}
    )

    courier_id = None
    if auth_response.status_code == 200:
        courier_id = auth_response.json().get('id')
    else:
        pytest.fail(f"Не удалось авторизоваться! Статус: {auth_response.status_code}")

    courier_data = [login, password, first_name, courier_id]

    yield courier_data

    if courier_id:
        delete_url = f"{urls.base_url}{urls.delete_courier}/{courier_id}"
        delete_response = requests.delete(
            delete_url,
            json={"id": str(courier_id)}
        )

        assert delete_response.status_code == 200


@pytest.fixture
def delete_courier_after_test():
    courier_data = {}

    yield courier_data

    if courier_data:
        login = courier_data.get('login')
        password = courier_data.get('password')

        if login and password:
            auth_response = requests.post(
                f"{urls.base_url}{urls.login_courier_endpoint}",
                json={"login": login, "password": password}
            )

            if auth_response.status_code == 200:
                courier_id = auth_response.json().get('id')

                if courier_id:
                    delete_response = requests.delete(
                        f"{urls.base_url}{urls.delete_courier}/{courier_id}"
                    )
