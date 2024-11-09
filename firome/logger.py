import logging
from sys import stdout

__hdl = logging.StreamHandler(stdout)
__hdl.setFormatter(logging.Formatter())  # TODO(@outcatcher): выбрать нормальный формат

LOGGER = logging.getLogger("merger")
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(__hdl)
