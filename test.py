from collections import namedtuple
from dataclasses import dataclass
import datetime


@dataclass
class User:
    username: str
    created_at: datetime.datetime
    birthday: datetime.datetime | None = None


user = 'Petr'
user = 120560
user = {
    'name': 'Petr',
    'email': 'petr@email.com',
    'id': 120560,
}
user = ('Petr', 'petr@email.com', 120560)


def validate_user_on_server(_): pass
def check_username(_): pass
def check_birthday(_): pass


def validate_user(user: User):
    """Checks the user, raises an exception if something is wrong with it."""
    validate_user_on_server(user)
    check_username(user)
    check_birthday(user)


user_id = 123
validate_user(user_id)


def plus_two(num: int):
    print('start function plus two')
    return num + 2


print(plus_two(5))


Car = namedtuple('Car', 'A B')
car = Car(A=4, B=5)
