import allure
import pytest

from data.order_data import OrderData as OD
from api.order_api import CreateOrderAPI as COA, GetOrderListAPI as GOLA


class TestOrder:
    @allure.title('Успешное создание заказа')
    @allure.description('При успешном создании заказа возвращается track')
    @pytest.mark.parametrize("first_name, last_name, address, metro_station, phone, rent_time, delivery_date, comment, color",
                             OD.create_order_with_black_success)
    def test_create_order_return_track(self, first_name, last_name, address, metro_station, phone, rent_time, delivery_date,
                            comment, color):
        with allure.step('Выполнение POST запроса к /api/v1/orders'):
            order_api = COA()
            response = order_api.create_order(first_name, last_name, address, metro_station, phone, rent_time, delivery_date, comment, color)
            allure.attach(
                f"Статус: {response.status_code}\nТело: {response.text}",
                "Ответ",
                allure.attachment_type.TEXT
            )

        with allure.step("Проверка статус кода ответа"):
            assert response.status_code == 201, \
                f"Expected 201, got {response.status_code}. Response: {response.text}"

        with allure.step("Проверка текста тела ответа"):
            assert 'track' in response.json()


    @allure.title('Успешное получение списка заказов')
    @allure.description('Успешное получение списка всех заказов')
    def test_get_list_orders_return_list(self):
        with allure.step('Выполнение Get запроса к /api/v1/orders'):
            order_api = GOLA()
            response = order_api.get_list_orders()
            allure.attach(
                f"Статус: {response.status_code}\nТело: {response.text}",
                "Ответ",
                allure.attachment_type.TEXT
            )

        with allure.step("Проверка статус кода ответа"):
            assert response.status_code == 200
        with allure.step("Проверка текста тела ответа"):
            assert "orders" in response.json()