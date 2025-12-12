from math import ceil
from flask import request
from config import Config


def paginate(items, total_count: int, page: int = None, page_size: int = None):
    page = page or int(request.args.get('page', 1))
    page_size = page_size or int(request.args.get('page_size', Config.PAGE_SIZE_DEFAULT))
    total_pages = max(1, ceil(total_count / page_size))
    return {
        'items': items,
        'page': page,
        'page_size': page_size,
        'total_count': total_count,
        'total_pages': total_pages
    }
