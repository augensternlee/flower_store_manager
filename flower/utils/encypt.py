import hashlib
from django.conf import settings


def md5(data_string):
    """
    将密码进行md5加密
    :param data_string: 需要加密的密码
    :return: 密码的密文
    """
    obj = hashlib.md5(settings.SECRET_KEY.encode("utf-8"))
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()