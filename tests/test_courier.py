import allure
import pytest

from api.courier_api import CreateCourierAPI as CCA, LoginCourierAPI as LCA
from data.courier_data import DataCreateCourier as DCR, DataLoginCourier as DLC
import helper as h

class TestCourierCreate:
    @allure.title('Успешное создание курьера')
    @allure.description('Проверка создания курьера')
    def test_create_courier_success(self, delete_courier_after_test):
        with allure.step('Генерация данных'):
            test_data = h.generate_random_word(10)

            payload = {
                "login": test_data[0],
                "password": test_data[1],
                "firstName": test_data[2]
            }
            allure.attach(str(payload), "Данные курьера", allure.attachment_type.JSON)

        with allure.step('Выполнение POST запроса к /api/v1/courier'):
            courier_api = CCA()
            response = courier_api.create_courier(payload['login'], payload['password'], payload['firstName'])
            allure.attach(
                f"Метод: POST\nURL: /api/v1/courier\nТело: {payload}",
                "Запрос",
                allure.attachment_type.TEXT
            )
            allure.attach(
                f"Статус: {response.status_code}\nТело: {response.text}",
                "Ответ",
                allure.attachment_type.TEXT
            )
        with allure.step("Проверка статус кода ответа"):
            assert response.status_code == 201, \
                f"Expected 201, got {response.status_code}. Response: {response.text}"

        with allure.step("Проверка тела ответа"):
            assert response.json() == {"ok": True}


    @allure.title('Попытка создания одинаковых курьеров')
    @allure.description('Попытка создания одинаковых курьеров')
    def test_create_duplicate_courier_error(self, register_new_courier_and_return_login_password):
        existing_courier = register_new_courier_and_return_login_password
        login = existing_courier[0]
        password = existing_courier[1]
        first_name = existing_courier[2]

        with allure.step('Выполнение POST запроса с дублирующим логином'):
            courier_api = CCA()
            response = courier_api.create_courier(login, password, first_name)

            allure.attach(
                f"Метод: POST\nURL: /api/v1/courier\nТело: {{'login': '{login}', 'password': '{password}', 'firstName': '{first_name}'}}",
                "Запрос",
                allure.attachment_type.TEXT
            )
            allure.attach(
                f"Статус: {response.status_code}\nТело: {response.text}",
                "Ответ",
                allure.attachment_type.TEXT
            )

        with allure.step("Проверка статус кода ответа"):
            assert response.status_code == 409, \
                f"Ожидался статус 409, получен {response.status_code}"

        with allure.step("Проверка сообщения об ошибке"):
            assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой.", \
                f"Ожидалось сообщение 'Этот логин уже используется. Попробуйте другой.', получено '{response.json().get('message')}'"


    @allure.title('Попытка создания курьера при потере одного параметра')
    @allure.description('Попытка создания курьера при потере пароля или логина и при пустом пароле или логине')
    @pytest.mark.parametrize("login, password, firstname", DCR.missing_field)
    def test_create_courier_missing_field_error(self, login, password, firstname):
        with allure.step('Выполнение POST запроса к /api/v1/courier'):
            courier_api = CCA()
            response = courier_api.create_courier(login, password, firstname)
            allure.attach(
                f"Статус: {response.status_code}\nТело: {response.text}",
                "Ответ",
                allure.attachment_type.TEXT
            )

        with allure.step("Проверка статус кода ответа"):
            assert response.status_code == 400, \
                f"Expected 400, got {response.status_code}"

        with allure.step("Проверка тела ответа"):
            assert "message" in response.json()

        with allure.step("Проверка текста тела ответа"):
            assert "Недостаточно данных для создания учетной записи" == response.json()["message"]


class TestLoginCourier:
    @allure.title('Успешная авторизация курьера')
    @allure.description('При успешной авторизации курьера, возвращается id')
    def test_login_courier_return_id(self, register_new_courier_and_return_login_password):
        with allure.step('Успешное создание нового курьера'):
            test_data = register_new_courier_and_return_login_password
            allure.attach(f'Данные курьера {test_data}', "Данные созданного курьера", allure.attachment_type.TEXT)

        with allure.step('Выполнение POST запроса к /api/v1/courier/login'):
            courier_api = LCA()
            response = courier_api.login_courier(test_data[0], test_data[1])
            allure.attach(
                f"Статус: {response.status_code}\nТело: {response.text}",
                "Ответ",
                allure.attachment_type.TEXT
            )
        with allure.step("Проверка статус кода ответа"):
            assert response.status_code == 200

        with allure.step("Проверка тела ответа"):
            assert 'id' in response.json()


    @allure.title('Попытка авторизации курьера с потерянным параметром')
    @allure.description('Попытка авторизации курьера с потерянным параметром')
    @pytest.mark.parametrize("login, password", DLC.missing_field)
    def test_login_courier_missing_field_error(self, login, password):
        with allure.step('Выполнение POST запроса к /api/v1/courier/login'):
            courier_api = LCA()
            response = courier_api.login_courier(login, password)
            allure.attach(
                f"Статус: {response.status_code}\nТело: {response.text}",
                "Ответ",
                allure.attachment_type.TEXT
            )

        with allure.step("Проверка статус кода ответа"):
            assert response.status_code == 400
        with allure.step("Проверка тела ответа"):
            assert response.json()["message"] == "Недостаточно данных для входа"


    @allure.title('Попытка авторизации курьера с неправильным паролем')
    @allure.description('Попытка авторизации курьера с неправильным паролем')
    def test_login_courier_incorrect_password_error(self, register_new_courier_and_return_login_password):
        with allure.step('Успешное создание нового курьера'):
            test_data = register_new_courier_and_return_login_password
            allure.attach(f'Данные курьера {test_data}', "Данные созданного курьера", allure.attachment_type.TEXT)

        with allure.step('Изменение пароля курьера'):
            incorrect_password = test_data[1][1:-1]
            allure.attach(f'Неправильный пароль курьера {incorrect_password}', "Изменение пароля курьера", allure.attachment_type.TEXT)

        with allure.step('Выполнение POST запроса к /api/v1/courier/login'):
            courier_api = LCA()
            response = courier_api.login_courier(test_data[0], incorrect_password)
            allure.attach(
                f"Статус: {response.status_code}\nТело: {response.text}",
                "Ответ",
                allure.attachment_type.TEXT
            )

        with allure.step("Проверка статус кода ответа"):
            assert response.status_code == 404
        with allure.step("Проверка тела ответа"):
            assert response.json()["message"] == "Учетная запись не найдена"


    @allure.title('Попытка авторизации незарегистрированного курьера')
    @allure.description('Попытка авторизации незарегистрированного курьера')
    def test_login_courier_not_register_error(self, delete_courier_after_test):
        with allure.step('Успешное создание нового курьера'):
            test_data = h.generate_random_word(10)
            allure.attach(f'Данные курьера {test_data}', "Данные созданного курьера", allure.attachment_type.TEXT)

        with allure.step('Выполнение POST запроса к /api/v1/courier/login'):
            courier_api = LCA()
            response = courier_api.login_courier(test_data[0], test_data[1])
            allure.attach(
                f"Статус: {response.status_code}\nТело: {response.text}",
                "Ответ",
                allure.attachment_type.TEXT
            )

        with allure.step("Проверка статус кода ответа"):
            assert response.status_code == 404

        with allure.step("Проверка тела ответа"):
            assert response.json()["message"] == "Учетная запись не найдена"