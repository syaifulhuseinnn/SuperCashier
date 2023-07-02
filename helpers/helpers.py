from babel.numbers import format_currency


def currency_conversion(number):
    """
    Formatting number into IDR currency format
    Args:
        number: price in integer
    Returns:
        Formatted Price: Integer price in IDR currency format
        None: if args type is not integer will return None
    """
    if type(number) is int:
        formatted_price = format_currency(number, "IDR", locale='id_ID')
        formatted_price = formatted_price.replace(",00", "")
        return formatted_price
    return number


def get_index(items, key, value):
    """
    Get index of list of dictionary
    Args:
        items: list of dictionary
        key: key of dictionary
        value: value of dictionary
    Returns:
        index: Index number of item
        -1: if item isn't available in list
    """
    for i in range(len(items)):
        if items[i][key].lower() == value.lower():
            return i
    return -1
