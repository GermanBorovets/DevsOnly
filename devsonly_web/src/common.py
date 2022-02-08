import logging


fmt = '[%(levelname)s] %(asctime)s: %(message)s ' \
    'in %(pathname)s:%(lineno)d'
logging.basicConfig(level=logging.DEBUG, format=fmt)


def get_ip(request) -> str:
    # Function returns ip address from request
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def from_get_id(request) -> int:
    # Function returns id from GET request if exists, else returns -1
    requested_id = request.GET.get('id', -1)

    if requested_id == -1:
        logging.error('There is not id in GET request')

    try:
        requested_id = int(requested_id)
    except ValueError:
        requested_id = -1
        logging.error('Requested id is not a number')

    return requested_id
