import requests


class CreateOrderAPI:
    def __init__(self, base_url="https://qa-scooter.education-services.ru"):
        self.base_url = base_url
        self.create_order_endpoint = '/api/v1/orders'

    def create_order(self, first_name, last_name, address, metro_station, phone, rent_time, delivery_date, comment, color=None):
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "address": address,
            "metroStation": metro_station,
            "phone": phone,
            "rentTime": rent_time,
            "deliveryDate": delivery_date,
            "comment": comment,
            "color": color
        }

        response = requests.post(
            f"{self.base_url}{self.create_order_endpoint}",
            json=payload
        )
        return response


class GetOrderListAPI:
    def __init__(self, base_url="https://qa-scooter.education-services.ru"):
        self.base_url = base_url
        self.list_orders = '/api/v1/orders'

    def get_list_orders(self):
        response = requests.get(f"{self.base_url}{self.list_orders}")
        return response

