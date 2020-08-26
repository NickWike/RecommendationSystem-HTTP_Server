import decimal


def str_to_int(str_n) -> int:
    number = 0
    try:
        number = int(str_n)
    except ValueError as e:
        pass
    finally:
        return number


def str_to_float(str_n, precision):
    f_n = 0.00


def str_to_bool(str_bool) -> bool:
    if not str_bool:
        return False
    upper_str_bool = str_bool.upper()
    if upper_str_bool == "FALSE":
        return False
    elif upper_str_bool == "TRUE":
        return True
    return False


def format_line(pre_data: dict) -> dict:
    result_data = {}
    for k, v in pre_data.items():
        if type(v) not in (float, int, str):
            result_data[k] = str(v)
        else:
            result_data[k] = v
    return result_data


def decimal_to_float(d):
    return str(decimal.Decimal(d).quantize(decimal.Decimal('0.00')))


if __name__ == '__main__':
    print(str_to_bool("True"))
