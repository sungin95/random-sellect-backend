def errors_check(serializer: dict) -> bool:
    if serializer.get("errors") is None:
        return True
    else:
        return False
