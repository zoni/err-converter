# encoding: utf-8
from errbot import BotPlugin, botcmd


def is_number(s):
    """Return true if the given string is a number"""
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True


class Converter(BotPlugin):
    """Convert various measurements and metrics"""

    @staticmethod
    def celsius_to_fahrenheit(celsius):
        """Convert Celsius to Fahrenheit"""
        return celsius * 1.8 + 32.0

    @staticmethod
    def fahrenheit_to_celsius(fahrenheit):
        """Convert Fahrenheit to Celsius"""
        return (fahrenheit - 32.0) / 1.8

    @botcmd
    def ctof(self, msg, args):
        """Convert given degrees Celsius to Fahrenheit"""
        if is_number(args):
            c = float(args)
            f = self.celsius_to_fahrenheit(c)
            return u"{c:1g} °C equals {f:1g} °F".format(c=c, f=f)
        else:
            return "'{}' is not a temperature I understand.".format(args)

    @botcmd
    def ftoc(self, msg, args):
        """Convert given degrees Fahrenheit to Celsius"""
        if is_number(args):
            f = float(args)
            c = self.fahrenheit_to_celsius(f)
            return u"{f:1g} °F equals {c:1g} °C".format(f=f, c=c)
        else:
            return "'{}' is not a temperature I understand.".format(args)
