import datetime


def get_linux_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
