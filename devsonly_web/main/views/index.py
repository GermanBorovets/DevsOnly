from django.shortcuts import render
from src.logger import init_logger


def index_page(request) -> None:
    logger = init_logger(__name__)

    logger.info('info')
    logger.warning('warning')
    logger.debug('debug')
    logger.error('error')
    logger.critical('critical')

    return render(request, 'pages/index.html')
