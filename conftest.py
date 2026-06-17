import string
import random
import pytest
import requests


@pytest.fixture
def generate_random_word():
    def _generate_random_string(length=10):
        letters = string.ascii_lowercase
        random_login = ''.join(random.choice(letters) for i in range(length))
        random_password = ''.join(random.choice(letters) for i in range(length))
        random_first_name = ''.join(random.choice(letters) for i in range(length))
        return random_login, random_password, random_first_name
    return _generate_random_string


@pytest.fixture
def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post('https://qa-scooter.education-services.ru/api/v1/courier', json=payload)

    if response.status_code == 201:
        return [login, password, first_name]
    else:
        pytest.fail(f"Не удалось создать курьера! Статус: {response.status_code}, Ответ: {response.text}")