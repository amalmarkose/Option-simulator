import hashlib


def generateKey(uid, appkey):
    """
    :param uid:
    :param appkey:
    :return:
    """
    return f"{uid}|{appkey}"


def encodePwd(pwd):
    """
    :param pwd:
    :return:
    """
    return hashlib.sha256((pwd.encode()))
