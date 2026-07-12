import requests
import urls


class CreateOrderAPI:
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
            f"{urls.base_url}{urls.create_order_endpoint}",
            json=payload
        )
        return response


class GetOrderListAPI:
    def get_list_orders(self):
        response = requests.get(f"{urls.base_url}{urls.list_orders}")
        return response

