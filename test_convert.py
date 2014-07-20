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
        assert pop_message() == u"100 °C equals 212 °F"
        push_message("!ctof 37")
        assert pop_message() == u"37 °C equals 98.6 °F"
        push_message('!ctof abc')
        assert pop_message() == u"'abc' is not a temperature I understand."

    def test_ftoc(self, testbot):
        push_message("!ftoc 212")
        assert pop_message() == u"212 °F equals 100 °C"
        push_message("!ftoc 98.6")
        assert pop_message() == u"98.6 °F equals 37 °C"
        push_message('!ftoc abc')
        assert pop_message() == u"'abc' is not a temperature I understand."

    def test_regex_triggers(self, testbot):
        say_expect = [
            ("It's 30 degrees C", u"30 °C equals 86 °F"),
            ("It's 30 degrees Celsius", u"30 °C equals 86 °F"),
            ("It's 30 degrees C today", u"30 °C equals 86 °F"),
            ("It's 30 degrees c today", u"30 °C equals 86 °F"),
            ("It's 30 degrees Celsius today", u"30 °C equals 86 °F"),
            ("It's 30 degrees celsius today", u"30 °C equals 86 °F"),
            ("It's 30 degrees c.", u"30 °C equals 86 °F"),
            ("It's 30 degrees celsius.", u"30 °C equals 86 °F"),
            ("It's 30 celsius today", u"30 °C equals 86 °F"),
            ("It's 86 degrees Fahrenheit today", u"86 °F equals 30 °C"),
            ("It's -40 degrees Celsius today", u"-40 °C equals -40 °F"),
            ("30 degrees Celsius", u"30 °C equals 86 °F"),
            ("What's 37 degrees celsius in fahrenheit?", u"37 °C equals 98.6 °F"),
            ("What's 98.6 degrees fahrenheit in celsius?", u"98.6 °F equals 37 °C"),
        ]

        for item in say_expect:
            push_message(item[0])
            assert pop_message() == item[1]

        push_message("It's 30 c today")
        push_message("It's 30 f today")
        push_message("It's 30 degrees celvin (I know Kelvin should be with a K)")

        # None of the above should match so response to this should be
        # first item returned by pop_message().
        push_message("!echo trick-to-avoid-wait-for-empty-queue")
        assert pop_message() == "trick-to-avoid-wait-for-empty-queue"
