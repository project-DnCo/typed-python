from collections import namedtuple
from dataclasses import dataclass
from typing import Iterable, Sequence, Mapping, Iterator, TypeVar, Callable
import datetime


# @dataclass
# class User:
#     username: str
#     created_at: datetime.datetime
#     birthday: datetime.datetime | None = None


# user = 'Petr'
# user = 120560
# user = {
#     'name': 'Petr',
#     'email': 'petr@email.com',
#     'id': 120560,
# }
# user = ('Petr', 'petr@email.com', 120560)


# def validate_user_on_server(_): pass
# def check_username(_): pass
# def check_birthday(_): pass


# def validate_user(user: User):
#     """Checks the user, raises an exception if something is wrong with it."""
#     validate_user_on_server(user)
#     check_username(user)
#     check_birthday(user)


# user_id = 123
# validate_user(user_id)


def plus_two(num: int):
    print('start function plus two')
    return num + 2


print(plus_two(5))


Car = namedtuple('Car', 'A B')
car = Car(A=4, B=5)


def print_hello(name: str | None = None) -> None:
    print(f'hello, {name}' if name is not None else 'hello, anon!')


print_hello()
print_hello('Alex')


@dataclass
class User:
    birthday: datetime.datetime


users = (
    User(birthday=datetime.datetime.fromisoformat('1988-01-01')),
    User(birthday=datetime.datetime.fromisoformat('1985-07-29')),
    User(birthday=datetime.datetime.fromisoformat('2000-10-10')),
)


def get_youngest_user(users: Sequence[User]) -> User:
    if not users:
        raise ValueError('empty users!')
    print(users[0])
    sorted_users = sorted(users, key=lambda user: user.birthday, reverse=True)
    return sorted_users[0]


print(get_youngest_user(users))


def smth(some_users: Mapping[str, User]) -> None:
    print(some_users['alex'])


smth({
    'alex': User(birthday=datetime.datetime.fromisoformat('1990-01-01')),
    'petr': User(birthday=datetime.datetime.fromisoformat('1988-10-23')),
})


class Users:
    def __init__(self, users: Sequence[User]):
        self._users = users

    # def __getitem__(self, key: int) -> User:
    #     return self._users[key]

    def __iter__(self) -> Iterator[User]:
        return iter(self._users)


users_ = Users((
    User(birthday=datetime.datetime.fromisoformat('1988-01-01')),
    User(birthday=datetime.datetime.fromisoformat('1985-07-29')),
    User(birthday=datetime.datetime.fromisoformat('2000-10-10')),
))

print()
# print(users_[2])

for u in users_:
    print(u)


three_ints = tuple[int, int, int]
int_tuple = tuple[int, ...]


def dsljfldkf(fsdjljf: int_tuple): pass
def lkdsfjsdf(fdsljkfl: three_ints): pass


T = TypeVar('T')


def first(iterable: Iterable[T]) -> T | None:
    for element in iterable:
        return element
    return None


print(first(['one', 'two']))
print(first((100, 200)))
print(first([]))


def mysum(a: int, b: int) -> int:
    return a + b


def process_operation(operation: Callable[[int, int], int], a: int, b: int) -> int:
    return operation(a, b)


print(process_operation(mysum, 1, 5))


book: str = 'some book'
