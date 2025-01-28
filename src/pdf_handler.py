from pdf2image import convert_from_path
from PyPDF2 import PdfReader, PdfWriter
import os
import logging
from PIL import Image
from .ocr_processor import OCRProcessor
from config.config import OCR_CONFIG, OUTPUT_DIR, TEMP_DIR

logger = logging.getLogger(__name__)

class PDFHandler:
    def __init__(self):
        self.ocr_processor = OCRProcessor()

    def convert_pdf_to_images(self, pdf_path: str, dpi: int = OCR_CONFIG['dpi']):
        """
        Convierte un PDF a una lista de imágenes
        """
        try:
            return convert_from_path(pdf_path, dpi=dpi)
        except Exception as e:
            logger.error(f"Error al convertir PDF a imágenes: {str(e)}")
            return []

    def find_split_points(self, images: list[Image.Image]) -> list[int]:
        """
        Encuentra los puntos de división basados en la detección de texto
        """
        split_points = []
        for i, image in enumerate(images):
            if self.ocr_processor.detect_liquidacion_provisional(image):
                split_points.append(i)
                logger.info(f"Encontrado punto de división en página {i}")
        return split_points

    def split_pdf(self, input_path: str, output_pattern: str = "liquidacion_{}.pdf"):
        """
        Divide el PDF en múltiples archivos basados en la detección de texto
        """
        logger.info(f"Iniciando proceso de división para {input_path}")
        
        # Crear directorios necesarios
        os.makedirs(TEMP_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Convertir PDF a imágenes
        images = self.convert_pdf_to_images(input_path)
        if not images:
            logger.error("No se pudieron extraer imágenes del PDF")
            return

        # Encontrar puntos de división
        split_points = self.find_split_points(images)
        if not split_points:
            logger.warning("No se encontraron puntos de división")
            return

        # Dividir el PDF
        reader = PdfReader(input_path)
        for i in range(len(split_points)):
            writer = PdfWriter()
            start = split_points[i]
            end = split_points[i + 1] if i + 1 < len(split_points) else len(images)

            for page_num in range(start, end):
                writer.add_page(reader.pages[page_num])

            output_path = os.path.join(OUTPUT_DIR, output_pattern.format(i))
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            logger.info(f"Creado archivo {output_path}")

        # Limpiar archivos temporales
        self.cleanup()

    def cleanup(self):
        """
        Limpia los archivos temporales
        """
        if os.path.exists(TEMP_DIR):
            for file in os.listdir(TEMP_DIR):
                os.remove(os.path.join(TEMP_DIR, file))
            os.rmdir(TEMP_DIR)