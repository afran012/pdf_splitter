import os

# Rutas del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
TEMP_DIR = os.path.join(BASE_DIR, 'temp')

# Configuración de OCR
OCR_CONFIG = {
    'lang': 'spa',  # Idioma español
    'dpi': 300,     # DPI para la conversión de PDF a imagen
    'psm': 3,       # Page segmentation mode
}

# Patrones de búsqueda
SEARCH_PATTERNS = [
    'LIQUIDACION PROVISIONAL',
    'LIQUIDACIÓN PROVISIONAL'
]

# Configuración de logging
LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'pdf_splitter.log'),
            'formatter': 'standard'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
        }
    }
}