# encoding: utf-8
from os.path import abspath, dirname
from errbot.backends.test import testbot, push_message, pop_message
from convert import Converter

extra_plugin_dir = dirname(abspath(__name__))


class TestTemperatureConversions(object):
    def test_convert_botcmd(self, testbot):
        push_message("!convert 1 kilometer to meters")
        assert pop_message() == "1 kilometer = 1000 meter"
        push_message("!convert 1 kilometer to yards")
        assert pop_message() == "1 kilometer = 1093.61 yard"

        push_message("!convert a kilometer to yards")
        m = pop_message()
        assert (
            m == "I don't know how to convert that (could not convert string to float: 'a')."
            or m == "I don't know how to convert that (could not convert string to float: a)."
        )
        push_message("!convert 1 foo to bar")
        assert pop_message() == "I don't know how to convert that ('foo' is not defined in the unit registry)."

    def test_temperature_regex(self, testbot):
        say_expect = [
            ("It's 30 degrees C", u"30 degC = 86 degF"),
            ("It's 30 degrees Celsius", u"30 degC = 86 degF"),
            ("It's 30 degrees C today", u"30 degC = 86 degF"),
            ("It's 30 degrees c today", u"30 degC = 86 degF"),
            ("It's 30 degrees Celsius today", u"30 degC = 86 degF"),
            ("It's 30 degrees celsius today", u"30 degC = 86 degF"),
            ("It's 30 degrees c.", u"30 degC = 86 degF"),
            ("It's 30 degrees celsius.", u"30 degC = 86 degF"),
            ("It's 30 celsius today", u"30 degC = 86 degF"),
            ("It's 86 degrees Fahrenheit today", u"86 degF = 30 degC"),
            ("It's -40 degrees Celsius today", u"-40 degC = -40 degF"),
            ("30 degrees Celsius", u"30 degC = 86 degF"),
            ("What's 37 degrees celsius in fahrenheit?", u"37 degC = 98.6 degF"),
            ("What's 98.6 degrees fahrenheit in celsius?", u"98.6 degF = 37 degC"),
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
