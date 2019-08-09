import os.path


def split_at(s: str, i: int):
    """Returns a tuple containing the part of the string before the
    specified index (non-inclusive) and the part after the index
    """

    return (s[:i], s[i:])


def get_user_home():
    return os.path.expanduser("~")
