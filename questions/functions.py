def page_nation(request, page_size):
    try:
        page = request.query_params.get("page", 1)
        page = int(page)
    except ValueError:
        page = 1
    page_size = page_size
    start = (page - 1) * page_size
    end = page * page_size
    return (start, end)
