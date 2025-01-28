import argparse
from src.pdf_handler import PDFHandler
from src.utils import setup_environment, setup_logging
import logging
import pytesseract
import os

# Configura la ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def main():
    # Configurar el entorno y logging
    setup_environment()
    setup_logging()
    logger = logging.getLogger(__name__)

    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Divide PDFs escaneados basado en la detección de "LIQUIDACIÓN PROVISIONAL"')
    parser.add_argument('input_pdf', help='Ruta al archivo PDF de entrada')
    parser.add_argument('--output-pattern', default='liquidacion_{}.pdf',
                      help='Patrón para nombrar los archivos de salida (default: liquidacion_{}.pdf)')

    args = parser.parse_args()

    # Verificar que el archivo existe
    if not os.path.exists(args.input_pdf):
        logger.error(f"El archivo {args.input_pdf} no existe")
        return

    # Procesar el PDF
    try:
        logger.info(f"Iniciando procesamiento del archivo: {args.input_pdf}")
        pdf_handler = PDFHandler()
        pdf_handler.split_pdf(args.input_pdf, args.output_pattern)
        
        # Verificar los resultados
        output_dir = os.path.join(os.getcwd(), 'output')
        if os.path.exists(output_dir):
            files = os.listdir(output_dir)
            logger.info(f"Archivos generados en output/: {len(files)}")
            for file in files:
                logger.info(f"  - {file}")
        else:
            logger.warning("No se encontró el directorio output/")
            
        logger.info("Proceso completado exitosamente")
    except Exception as e:
        logger.error(f"Error durante el procesamiento: {str(e)}")

if __name__ == "__main__":
    main()