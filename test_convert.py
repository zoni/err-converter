# encoding: utf-8
from os.path import abspath, dirname
from errbot.backends.test import testbot, push_message, pop_message
from convert import Converter

extra_plugin_dir = dirname(abspath(__name__))


class TestTemperatureConversions(object):
    def test_celsius_to_fahrenheit(self):
        c_to_f = Converter.celsius_to_fahrenheit
        assert c_to_f(100) == 212
        assert c_to_f(0) == 32
        assert c_to_f(-40) == -40
        assert abs(c_to_f(37) - 98.6) < 0.00001

    def test_fahrenheit_to_celsius(self):
        f_to_c = Converter.fahrenheit_to_celsius
        assert f_to_c(212) == 100
        assert f_to_c(32) == 0
        assert f_to_c(-40) == -40
        assert abs(f_to_c(98.6) - 37) < 0.00001

    def test_ctof(self, testbot):
        push_message("!ctof 100")
        assert pop_message() == "100 °C equals 212 °F"
        push_message("!ctof 37")
        assert pop_message() == "37 °C equals 98.6 °F"
        push_message('!ctof abc')
        assert pop_message() == "'abc' is not a temperature I understand."

    def test_ftoc(self, testbot):
        push_message("!ftoc 212")
        assert pop_message() == "212 °F equals 100 °C"
        push_message("!ftoc 98.6")
        assert pop_message() == "98.6 °F equals 37 °C"
        push_message('!ftoc abc')
        assert pop_message() == "'abc' is not a temperature I understand."
