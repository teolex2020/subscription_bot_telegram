import logging
import os

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    format='[%(asctime)s] %(levelname)-8s | %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/bot.log"),
        logging.StreamHandler()
    ],
)

logger = logging.getLogger(__name__)