from django.shortcuts import render
from src.common import from_get_id
from src.common import logging


def index_page(request) -> None:

    return render(request, 'pages/index.html')
