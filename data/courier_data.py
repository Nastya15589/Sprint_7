class DataCreateCourier:

    ANOTHER_COURIER = {
        "login": "ninja_test_2",
        "password": "5678",
        "firstName": "naruto"
    }

    missing_field = [('', "1234", "saske"), ("ninja_test", '', "saske"), (None, "1234", "saske"), ("ninja_test", None, "saske")]

class DataLoginCourier:
    missing_field = [(None,"1234")]