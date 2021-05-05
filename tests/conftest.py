import pytest
import string
from random import choice


@pytest.fixture()
def generate_string(length: int = 16) -> str:

    random_source = string.ascii_letters + string.digits + string.punctuation

    random_string = "".join(choice(random_source) for i in range(length))

    return random_string


@pytest.fixture()
def generate_int(length: int = 8) -> int:

    random_int = "".join(choice(string.digits) for i in range(length))

    return int(random_int)
