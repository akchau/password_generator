""" Модуль генерации паролей """
import secrets
import string
from enum import Enum


class SignCategoryE(Enum):
    """ Категории символов """
    DIGIT = "digit"
    LETTER_UPPERCASE = "letter_uppercase"
    LETTER_LOWERCASE = "letter_lowercase"
    SIGN = "sign"


__pool_password_sign = {
    SignCategoryE.DIGIT: list(map(str, list(range(10)))),
    SignCategoryE.LETTER_UPPERCASE: list(string.ascii_uppercase),
    SignCategoryE.LETTER_LOWERCASE: list(string.ascii_lowercase),
    SignCategoryE.SIGN: [
        '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
        '_', '+', '-', '=', '[', ']', '{', '}', '|',
        ';', ':', ',', '.', '<', '>', '?'
    ]
}


def secrets_shuffle(lst):
    """
    Перемешивание списка элементов.

    (Используется алгоритм Фишера-Йетса)
    """
    for i in range(len(lst) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        lst[i], lst[j] = lst[j], lst[i]


def generate(length: int) -> str:
    """ Генерация паролей """
    if length < len(__pool_password_sign):
        raise ValueError(
            "Пароль не может содержать меньше символов чем категорий символов "
            f"{len(__pool_password_sign)}"
        )
    password_chars = []
    for _, symbols in __pool_password_sign.items():
        password_chars.append(secrets.choice(symbols))
    all_symbols = []
    for symbols in __pool_password_sign.values():
        all_symbols.extend(symbols)
    remaining_length = length - len(password_chars)
    for _ in range(remaining_length):
        password_chars.append(secrets.choice(all_symbols))
    secrets_shuffle(password_chars)
    return ''.join(password_chars)


def generate_password() -> str:
    """ Выбор длинны пароля и вызов генерации """
    password_length = secrets.choice(range(12, 17))
    return generate(password_length)


print(generate_password())
