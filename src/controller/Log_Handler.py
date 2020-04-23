""" 
Log Handler

Funções para gerenciamento de logs de interação.
Atualmente, é utilizada apenas pela aplicação Flask
para capturar falhas de processamento durante execução
"""

from os.path import exists
from os import mkdir

from logging.handlers import RotatingFileHandler
from logging import Formatter
from logging import INFO

def error_logger_file_handler(log_dir='logs'):

    if not exists(log_dir):
        mkdir(log_dir)

    file_handler = RotatingFileHandler(log_dir + '/error.log',
        maxBytes=10240, backupCount=10)

    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(INFO)

    return file_handler
