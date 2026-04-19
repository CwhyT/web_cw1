def normalize_openlibrary_key(value: str) -> str:
    if value.startswith("/works/"):
        return value
    return f"/works/{value}"

