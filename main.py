import argparse
from src.pdf_handler import PDFHandler
from src.utils import setup_environment, setup_logging
import logging
import os
import pytesseract

# Configurar Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def main():
    setup_environment()
    setup_logging()
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description='Analiza y divide PDFs basado en la detección de "LIQUIDACIÓN PROVISIONAL"')
    parser.add_argument('input_pdf', help='Ruta al archivo PDF de entrada')
    parser.add_argument('--analyze-only', action='store_true', help='Solo realizar análisis sin dividir el PDF')
    parser.add_argument('--output-pattern', default='liquidacion_{}.pdf',
                      help='Patrón para nombrar los archivos de salida (default: liquidacion_{}.pdf)')

    args = parser.parse_args()

    if not os.path.exists(args.input_pdf):
        logger.error(f"El archivo {args.input_pdf} no existe")
        return

    try:
        pdf_handler = PDFHandler()
        
        # Primero realizar el análisis
        pdf_handler.analyze_pdf_text(args.input_pdf)
        
        if not args.analyze_only:
            # Proceder con la división si no es solo análisis
            pdf_handler.split_pdf(args.input_pdf, args.output_pattern)
            
        logger.info("Proceso completado exitosamente")
    except Exception as e:
        logger.error(f"Error durante el procesamiento: {str(e)}")

if __name__ == "__main__":
    main()