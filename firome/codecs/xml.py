"""Common XML functions"""


def add_ns(tag, ns):
    return f"{{{ns}}}{tag}"
