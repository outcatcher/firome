import logging

from sys import stdout

__hdl = logging.StreamHandler(stdout)
__hdl.setFormatter(logging.Formatter())  # TODO: выбрать нормальный формат

LOGGER = logging.Logger("merger", logging.INFO)
LOGGER.addHandler(__hdl)
