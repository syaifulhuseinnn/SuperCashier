from babel.numbers import format_currency


def currency_conversion(number):
    if type(number) is int:
        formatted_price = format_currency(number, "IDR", locale='id_ID')
        formatted_price = formatted_price.replace(",00", "")
        return formatted_price
    return number


def get_index(items, key, value):
    for i in range(len(items)):
        if items[i][key].lower() == value.lower():
            return i
    return -1
