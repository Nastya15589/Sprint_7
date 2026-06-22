import random
import string


def generate_random_word(length=10):
    letters = string.ascii_lowercase
    random_login = ''.join(random.choice(letters) for i in range(length))
    random_password = ''.join(random.choice(letters) for i in range(length))
    random_first_name = ''.join(random.choice(letters) for i in range(length))
    return random_login, random_password, random_first_name
