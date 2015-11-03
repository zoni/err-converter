# encoding: utf-8
from __future__ import unicode_literals
import re
import pint
from errbot import BotPlugin, botcmd, re_botcmd

TEMPERATURE_REGEX = re.compile(
    r"""(?P<degrees>[-+]?[\d]*\.?[\d]+)\s+  # Digit with optional precision followed by whitespace
        (
            ((degrees )?(?P<type1>(Celsius|Fahrenheit)))  # Word 'degrees' optional
        |
            (degrees\ (?P<type2>(Celsius|Fahrenheit|C|F)))  # 'degrees' required when just C/F
        )
        ([^\w]+|$)  # after c/f should come non-word character or end of line.""",
    flags=re.IGNORECASE|re.VERBOSE
)
UNIT_REPLACEMENTS = {re.escape(k): v for k, v in {
    "degC": "°C",
    "degF": "°F",
    "degK": "°K",
}.items()}
UNIT_REPLACEMENT_REGEX = re.compile("|".join(UNIT_REPLACEMENTS.keys()))


class Converter(BotPlugin):
    """Convert various measurements and metrics"""
    min_err_version = '3.1.0'

    def activate(self):
        self.unitregistry = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)
        super(Converter, self).activate()

    def convert(self, quantity, from_, to):
        """
        Convert quantity from one thing to another

        :param quantity:
            The quantity to convert
        :param from_:
            The type of metric to convert from
        :param to:
            The type of metric to convert to
        :return:
            A tuple in the form (from, to) where from is the quantity
            in the from_ form, to is the quantity in the to form.
        """
        from_ = float(quantity) * getattr(self.unitregistry, from_)
        to = from_.to(getattr(self.unitregistry, to))
        return (from_, to)

    def format_quantity(self, quantity):
        """
        Format a Quantity for pretty-printing.

        :param quantity:
            A pint Quantity object
        :return:
            A pretty-printed string
        """
        text = UNIT_REPLACEMENT_REGEX.sub(
            lambda m: UNIT_REPLACEMENTS[re.escape(m.group(0))],
            "{:1g}".format(quantity)
        )
        return text

    @botcmd(name="convert", split_args_with=None)
    def convert_cmd(self, msg, args):
        """
        Convert a given measurement into something else.

        Usage:
            !convert <amount> <from> <to>
        or:
            !convert <amount> <from> to <to>

        Examples:
            !convert 30 celsius fahrenheit
            !convert 30 celsius to fahrenheit
            !convert 10 meters yards
            !convert 10 meters to yards
        """
        l = len(args)
        if l == 3:
            amount, from_, to = args
        elif l == 4 and args[2] == "to":
            amount, from_, to = (args[0], args[1], args[3])
        else:
            return "Usage: !convert <amount> <from> to <to>"

        try:
            from_, to = self.convert(amount, from_, to)
            return "{} = {}".format(
                self.format_quantity(from_),
                self.format_quantity(to)
            )
        except Exception as e:
            return "I don't know how to convert that ({}).".format(e)

    @re_botcmd(pattern=TEMPERATURE_REGEX, prefixed=False)
    def listen_for_temperature_mentions(self, msg, match):
        gd = match.groupdict()
        type_ = gd['type1'] if gd['type1'] is not None else gd['type2']

        if type_.lower() in ("c", "celsius"):
            return self.convert_cmd(msg, (gd['degrees'], 'celsius', 'fahrenheit'))
        else:
            return self.convert_cmd(msg, (gd['degrees'], 'fahrenheit', 'celsius'))
