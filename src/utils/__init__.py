import random
import hashlib
from typing import AnyStr
from .decorators import singleton


def gen_random(mode='mixDigitLetter', length=16):
    """
    按照不同模式生成随机字符串
    :return:
    """
    upper_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower_letter = "abcdefghigklmnopqrstuvwxyz"
    digits = "0123456789"
    wpecial_characters = "!@#$%&_-.+="
    random_map = {
        "digit": digits,
        "upper": upper_letter,
        "lower": lower_letter,
        "mixDigitLetter": upper_letter + lower_letter + digits,
        "mixLetter": upper_letter + lower_letter,
        "mixDigitLetterCharcter": upper_letter + lower_letter + digits + wpecial_characters
    }

    str_list = [random.choice(random_map[mode]) for i in range(length)]
    random_str = ''.join(str_list)
    return random_str


def md5(content):
    """
    md5 加密
    :param content:
    :return:
    """
    m = hashlib.md5(content.encode(encoding='utf-8'))
    return m.hexdigest()


def gen_password(password: AnyStr, salt: AnyStr):
    """
    密码生成器
    salt 嵌在 password 中
    :param password:
    :param salt:
    :return:
    """
    return md5(salt.join(password))


__all__ = [
    singleton,
    gen_random,
    md5,
    gen_password
]