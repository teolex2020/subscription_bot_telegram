import logging
import sys
import io
import os
from logging.handlers import RotatingFileHandler  # Додаємо імпорт

# Створюємо директорію для логів, якщо її немає
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Формат логів
log_format = "[%(asctime)s] %(levelname)-8s | %(message)s"

# Замість FileHandler використовуємо RotatingFileHandler
file_handler = RotatingFileHandler(
    f"{LOG_DIR}/bot.log",
    maxBytes=5*1024*1024,  # 5 MB
    backupCount=5,         # Зберігати до 5 архівних файлів
    encoding="utf-8"
)
file_handler.setFormatter(logging.Formatter(log_format))

# Налаштування StreamHandler для виведення в консоль
stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(logging.Formatter(log_format))

# Якщо це Windows, явно вказуємо кодування UTF-8 для консолі
if sys.platform == "win32":
    stream_handler.stream = io.TextIOWrapper(
        stream_handler.stream.buffer, encoding="utf-8"
    )

# Налаштування логера
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        file_handler,   # Використовуємо RotatingFileHandler
        stream_handler, # Залишаємо StreamHandler для консолі
    ],
)

logger = logging.getLogger(__name__)