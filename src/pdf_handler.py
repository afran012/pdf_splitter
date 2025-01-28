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
            logger.info(f"Iniciando conversión de PDF a imágenes con DPI={dpi}")
            images = convert_from_path(pdf_path, dpi=dpi)
            logger.info(f"PDF convertido exitosamente. Total de páginas: {len(images)}")
            return images
        except Exception as e:
            logger.error(f"Error al convertir PDF a imágenes: {str(e)}")
            return []

    def find_split_points(self, images: list[Image.Image]) -> list[int]:
        """
        Encuentra los puntos de división basados en la detección de texto
        """
        split_points = []
        total_images = len(images)
        logger.info(f"Iniciando búsqueda de puntos de división en {total_images} páginas")

        for i, image in enumerate(images):
            logger.debug(f"Procesando página {i+1} de {total_images}")
            if self.ocr_processor.detect_liquidacion_provisional(image):
                split_points.append(i)
                logger.info(f"Encontrado punto de división en página {i+1}")

        logger.info(f"Búsqueda completada. Encontrados {len(split_points)} puntos de división")
        return split_points

    def split_pdf(self, input_path: str, output_pattern: str = "liquidacion_{}.pdf"):
        """
        Divide el PDF en múltiples archivos basados en la detección de texto
        """
        logger.info(f"Iniciando proceso de división para {input_path}")
        
        # Verificar si el archivo existe
        if not os.path.exists(input_path):
            logger.error(f"Error: El archivo {input_path} no existe")
            return

        # Crear directorios necesarios
        try:
            os.makedirs(TEMP_DIR, exist_ok=True)
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            logger.info("Directorios de trabajo creados correctamente")
        except Exception as e:
            logger.error(f"Error al crear directorios: {str(e)}")
            return

        # Convertir PDF a imágenes
        logger.info("Iniciando conversión de PDF a imágenes...")
        images = self.convert_pdf_to_images(input_path)
        if not images:
            logger.error("No se pudieron extraer imágenes del PDF")
            return

        # Encontrar puntos de división
        logger.info("Buscando puntos de división en el documento...")
        split_points = self.find_split_points(images)
        if not split_points:
            logger.warning("No se encontraron puntos de división en el documento")
            return

        # Dividir el PDF
        try:
            reader = PdfReader(input_path)
            total_pages = len(reader.pages)
            logger.info(f"PDF cargado correctamente. Total de páginas: {total_pages}")

            for i in range(len(split_points)):
                writer = PdfWriter()
                start = split_points[i]
                end = split_points[i + 1] if i + 1 < len(split_points) else total_pages

                logger.info(f"Procesando segmento {i+1}: páginas {start+1} a {end}")
                
                for page_num in range(start, end):
                    writer.add_page(reader.pages[page_num])

                output_path = os.path.join(OUTPUT_DIR, output_pattern.format(i))
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                logger.info(f"Creado archivo {output_path} ({end-start} páginas)")

            logger.info(f"Proceso de división completado. {len(split_points)} archivos creados")

        except Exception as e:
            logger.error(f"Error durante la división del PDF: {str(e)}")
            return
        finally:
            # Limpiar archivos temporales
            self.cleanup()

    def cleanup(self):
        """
        Limpia los archivos temporales
        """
        try:
            if os.path.exists(TEMP_DIR):
                for file in os.listdir(TEMP_DIR):
                    file_path = os.path.join(TEMP_DIR, file)
                    os.remove(file_path)
                    logger.debug(f"Eliminado archivo temporal: {file}")
                os.rmdir(TEMP_DIR)
                logger.info("Limpieza de archivos temporales completada")
        except Exception as e:
            logger.error(f"Error durante la limpieza de archivos temporales: {str(e)}")