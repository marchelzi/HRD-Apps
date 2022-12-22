import math


def int_to_roman(num):
    """
    Convert an integer to a Roman numeral. using Divide and Conquer
    """
    roman_map = [
        ('M', 1000),
        ('CM', 900),
        ('D', 500),
        ('CD', 400),
        ('C', 100),
        ('XC', 90),
        ('L', 50),
        ('XL', 40),
        ('X', 10),
        ('IX', 9),
        ('V', 5),
        ('IV', 4),
        ('I', 1),
    ]

    if not isinstance(num, int):
        raise TypeError("expected integer, got %s" % type(num))
    if not 0 < num < 4000:
        raise ValueError("Argument must be between 1 and 3999")

    def to_roman(n):
        for roman, integer in roman_map:
            x, y = divmod(n, integer)
            yield roman * x
            n -= (integer * x)
            if n > 0:
                to_roman(n)
            else:
                break
    return ''.join([a for a in to_roman(num)])
