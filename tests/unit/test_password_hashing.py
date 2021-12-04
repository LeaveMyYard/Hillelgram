from core import passwords
import pytest
import string
import random


def gen_random_password(min_length: int, max_length: int) -> str:
    available_letters = string.printable
    return "".join(
        random.sample(available_letters, random.randint(min_length, max_length))
    )


@pytest.mark.parametrize(
    ["password"],
    [(gen_random_password(4, 20),) for _ in range(25)],
)
def test_password_hashing(password: str) -> None:
    hashed_password = passwords.hash_password(password)
    assert passwords.passwords_equal(password, hashed_password)
