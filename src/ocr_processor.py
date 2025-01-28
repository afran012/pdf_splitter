import pytesseract
from PIL import Image, ImageEnhance
import logging
import re
import numpy as np
import cv2

logger = logging.getLogger(__name__)

class OCRProcessor:
    def __init__(self):
        self.search_patterns = [
            'LIQUIDACION PROVISIONAL',
            'LIQUIDACIÓN PROVISIONAL',
            'LIQUIDAC[Il]ON PROVISIONAL',
            'LIQUIDAC[Il]ÓN PROVISIONAL',
            'LIQUIDACl[OÓ]N PROVISIONAL'
        ]

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocesa la imagen para mejorar la detección de texto
        """
        # Convertir PIL Image a formato numpy array
        img_np = np.array(image)
        
        # Convertir a escala de grises si no lo está
        if len(img_np.shape) == 3:
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_np

        # Aplicar umbral adaptativo
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # Reducir ruido
        denoised = cv2.fastNlMeansDenoising(binary)

        # Convertir de vuelta a PIL Image
        return Image.fromarray(denoised)

    def process_header_area(self, image: Image.Image) -> str:
        """
        Procesa el área superior de la imagen con múltiples técnicas
        """
        try:
            width, height = image.size
            
            # Procesar diferentes alturas del encabezado
            header_heights = [
                int(height * 0.1),  # 10% superior
                int(height * 0.15), # 15% superior
                int(height * 0.2)   # 20% superior
            ]
            
            results = []
            for header_height in header_heights:
                # Recortar el área del encabezado
                header_image = image.crop((0, 0, width, header_height))
                
                # Preprocesar la imagen
                processed_image = self.preprocess_image(header_image)
                
                # Probar diferentes configuraciones de OCR
                configs = [
                    '--oem 3 --psm 6',  # Asume un bloque uniforme de texto
                    '--oem 3 --psm 4',  # Asume texto variable en columnas
                    '--oem 3 --psm 3'   # Asume detección automática completa
                ]
                
                for config in configs:
                    try:
                        text = pytesseract.image_to_string(
                            processed_image, 
                            lang='spa',
                            config=config
                        )
                        if text.strip():  # Solo agregar si hay texto
                            results.append(text.upper())
                    except Exception as e:
                        logger.error(f"Error en OCR con config {config}: {str(e)}")
            
            # Combinar todos los resultados
            combined_text = ' '.join(results)
            logger.debug(f"Texto combinado detectado: {combined_text}")
            return combined_text
        except Exception as e:
            logger.error(f"Error en process_header_area: {str(e)}")
            return ""

    def detect_liquidacion_provisional(self, image: Image.Image) -> bool:
        """
        Detecta si la imagen contiene el texto 'LIQUIDACIÓN PROVISIONAL'
        """
        try:
            # Procesar el texto del encabezado
            header_text = self.process_header_area(image)
            
            # Buscar patrones en el texto procesado
            for pattern in self.search_patterns:
                if re.search(pattern, header_text, re.IGNORECASE):
                    logger.info(f"Patrón encontrado: {pattern}")
                    return True

            # Si no se encontró, intentar con configuraciones adicionales
            # Procesar la imagen completa con preprocesamiento
            processed_image = self.preprocess_image(image)
            full_text = pytesseract.image_to_string(
                processed_image,
                lang='spa',
                config='--oem 3 --psm 1'  # Orientación automática y segmentación
            )
            full_text = full_text.upper()
            
            for pattern in self.search_patterns:
                if re.search(pattern, full_text, re.IGNORECASE):
                    logger.info(f"Patrón encontrado en página completa: {pattern}")
                    return True
                    
            return False
        except Exception as e:
            logger.error(f"Error en detect_liquidacion_provisional: {str(e)}")
            return False

    def get_debug_info(self, image: Image.Image) -> dict:
        """
        Obtiene información detallada de depuración
        """
        try:
            # Asegurarse de que header_text existe
            header_text = self.process_header_area(image)
            
            # Buscar texto similar en todo el contenido
            similar_text = []
            if header_text:
                words = header_text.split()
                for word in words:
                    if 'LIQUID' in word or 'PROVIS' in word:
                        similar_text.append(word)

            # Crear el diccionario con todas las claves necesarias
            debug_info = {
                'header_text': header_text,
                'image_size': image.size,
                'patterns_tried': self.search_patterns,
                'similar_text_found': similar_text,
                'raw_text': header_text  # Agregar el texto completo detectado
            }
            
            return debug_info
        except Exception as e:
            logger.error(f"Error en get_debug_info: {str(e)}")
            # Retornar un diccionario con valores por defecto
            return {
                'header_text': "",
                'image_size': (0, 0),
                'patterns_tried': self.search_patterns,
                'similar_text_found': [],
                'raw_text': ""
            }