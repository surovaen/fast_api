def is_digit(target: str):
    """Функция, проверяющая строку на int и float."""
    replace_values = {
        ".": "",
        ",": "",
        "-": "",
    }
    for i, j in replace_values.items():
        target = target.replace(i, j)
    return target.isdigit()
