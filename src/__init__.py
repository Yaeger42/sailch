import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
)

LOGGER = logging.getLogger(__name__)
