from django import template
import logging, inspect
from decimal import Decimal
register = template.Library()


logger = logging.getLogger(__name__)


    # This method filter and return one item of dictionnary
@register.filter(name ='get_item')
def get_item(dictionary, arg):
    reponse = dictionary.get(arg)
    return reponse

@register.filter(name = 'add_value')
def add_value(value, arg):
    return str(value) + str(arg)

# Function to print sum
@register.filter(name = 'somme_item')
def returnSum(myDict):
    sum = 0
    for i in myDict:
        sum = sum + myDict[i]

    return sum


def valid_numeric(arg):
    if isinstance(arg, (int, float, Decimal)):
        return arg
    try:
        return int(arg)
    except ValueError:
        return float(arg)


def handle_float_decimal_combinations(value, arg, operation):
    if isinstance(value, float) and isinstance(arg, Decimal):
        logger.warning('Unsafe operation: {0!r} {1} {2!r}.'.format(value, operation, arg))
        value = Decimal(str(value))
    if isinstance(value, Decimal) and isinstance(arg, float):
        logger.warning('Unsafe operation: {0!r} {1} {2!r}.'.format(value, operation, arg))
        arg = Decimal(str(arg))
    return value, arg

@register.filter
def sub(value, arg):
    """Subtract the arg from the value."""
    try:
        nvalue, narg = handle_float_decimal_combinations(
            valid_numeric(value), valid_numeric(arg), '-')
        return nvalue - narg
    except (ValueError, TypeError):
        try:
            return value - arg
        except Exception:
            return ''


@register.filter
def mul(value, arg):
    """Multiply the arg with the value."""
    try:
        nvalue, narg = handle_float_decimal_combinations(
            valid_numeric(value), valid_numeric(arg), '*')
        return nvalue * narg
    except (ValueError, TypeError):
        try:
            return value * arg
        except Exception:
            return ''


@register.filter
def div(value, arg):
    """Divide the arg by the value."""
    try:
        nvalue, narg = handle_float_decimal_combinations(
            valid_numeric(value), valid_numeric(arg), '/')
        if nvalue != 0 and narg != 0:
            return nvalue / narg
        else:
            return 0

    except (ValueError, TypeError):
        try:
            return value / arg
        except Exception:
            return ''

@register.filter
def intdiv(value, arg):
    """Divide the arg by the value. Use integer (floor) division."""
    try:
        nvalue, narg = handle_float_decimal_combinations(
            valid_numeric(value), valid_numeric(arg), '//')
        return nvalue // narg
    except (ValueError, TypeError):
        try:
            return value // arg
        except Exception:
            return ''

@register.filter(name='abs')
def absolute(value):
    """Return the absolute value."""
    try:
        return abs(valid_numeric(value))
    except (ValueError, TypeError):
        try:
            return abs(value)
        except Exception:
            return ''


@register.filter
def mod(value, arg):
    """Return the modulo value."""
    try:
        nvalue, narg = handle_float_decimal_combinations(
            valid_numeric(value), valid_numeric(arg), '%')
        return nvalue % narg
    except (ValueError, TypeError):
        try:
            return value % arg
        except Exception:
            return ''

@register.filter(name='addition')
def addition(value, arg):
    """Float-friendly replacement for Django's built-in `add` filter."""
    try:
        nvalue, narg = handle_float_decimal_combinations(
            valid_numeric(value), valid_numeric(arg), '+')
        return nvalue + narg
    except (ValueError, TypeError):
        try:
            return value + arg
        except Exception:
            return ''