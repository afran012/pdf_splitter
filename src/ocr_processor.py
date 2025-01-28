import pytesseract
from PIL import Image
import logging
from config.config import OCR_CONFIG, SEARCH_PATTERNS

logger = logging.getLogger(__name__)

class OCRProcessor:
    def __init__(self, lang=OCR_CONFIG['lang'], psm=OCR_CONFIG['psm']):
        self.lang = lang
        self.psm = psm
        self.config = f'--psm {psm}'

    def process_image(self, image: Image.Image) -> str:
        """
        Procesa una imagen usando OCR y retorna el texto detectado
        """
        try:
            text = pytesseract.image_to_string(image, lang=self.lang, config=self.config)
            return text
        except Exception as e:
            logger.error(f"Error en OCR: {str(e)}")
            return ""

    def detect_liquidacion_provisional(self, image: Image.Image) -> bool:
        """
        Detecta si la imagen contiene el texto 'LIQUIDACIÓN PROVISIONAL'
        """
        text = self.process_image(image).upper()
        return any(pattern.upper() in text for pattern in SEARCH_PATTERNS)