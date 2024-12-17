def convert_to_int(value: int | str) -> int:
    try:
        return int(value)
    except Exception:
        return 1