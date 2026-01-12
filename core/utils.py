def is_htmx(request):
    """
    Check if the request is from HTMX.
    """
    return request.headers.get('HX-Request') == 'true'
