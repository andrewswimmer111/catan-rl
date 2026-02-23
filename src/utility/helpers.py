import random

def elementwise_add_tuples(tuple1, tuple2):
    """
    Performs element-wise addition on two tuples of equal length.
    Raises a ValueError if tuples are of different lengths.
    """
    if len(tuple1) != len(tuple2):
        raise ValueError(
            "Tuples must be of the same length for element-wise addition."
        )

    # Use zip to pair elements and a generator expression with sum()
    result = tuple(sum(items) for items in zip(tuple1, tuple2))
    return result


def quantize_point(point, ndigits=3):
    """
    Round a 2D point to a fixed number of decimal places
    to ensure stable float comparisons.
    """
    return (round(point[0], ndigits), round(point[1], ndigits))
