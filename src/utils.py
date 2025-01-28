import os
import logging
import logging.config
from config.config import LOGGING_CONFIG, LOGS_DIR, OUTPUT_DIR, TEMP_DIR

def setup_environment():
    """
    Configura el entorno de trabajo creando los directorios necesarios
    """
    for directory in [LOGS_DIR, OUTPUT_DIR, TEMP_DIR]:
        os.makedirs(directory, exist_ok=True)

def setup_logging():
    """
    Configura el sistema de logging
    """
    logging.config.dictConfig(LOGGING_CONFIG)