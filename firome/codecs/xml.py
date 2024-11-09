"""Common XML functions."""


def add_ns(tag, ns):
    """Add namespace to the tag."""
    return f"{{{ns}}}{tag}"
