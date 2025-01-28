import argparse
from src.pdf_handler import PDFHandler
from src.utils import setup_environment, setup_logging
import logging

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

    # Procesar el PDF
    try:
        pdf_handler = PDFHandler()
        pdf_handler.split_pdf(args.input_pdf, args.output_pattern)
        logger.info("Proceso completado exitosamente")
    except Exception as e:
        logger.error(f"Error durante el procesamiento: {str(e)}")

if __name__ == "__main__":
    main()