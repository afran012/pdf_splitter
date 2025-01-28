import os
import logging
from config.config import LOGS_DIR, OUTPUT_DIR, TEMP_DIR

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
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler(),  # Envía logs a la consola
            logging.FileHandler(os.path.join(LOGS_DIR, 'pdf_splitter.log'))  # Envía logs a un archivo
        ]
    )