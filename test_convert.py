# encoding: utf-8
from __future__ import unicode_literals
from os.path import abspath, dirname
from errbot.backends.test import testbot, FullStackTest
from convert import Converter

extra_plugin_dir = dirname(abspath(__name__))


class TestTemperatureConversions(object):
    def test_convert_botcmd(self, testbot):
        testbot.bot.push_message("!convert 1 kilometer to meters")
        assert testbot.bot.pop_message() == "1 kilometer = 1000 meter"
        testbot.bot.push_message("!convert 1 kilometer to yards")
        assert testbot.bot.pop_message() == "1 kilometer = 1093.61 yard"

        testbot.bot.push_message("!convert a kilometer to yards")
        m = testbot.bot.pop_message()
        assert m in (
            "I don't know how to convert that (could not convert string to float: 'a').",
            "I don't know how to convert that (could not convert string to float: a)."
        )
        testbot.bot.push_message("!convert 1 foo to bar")
        assert testbot.bot.pop_message() == \
            "I don't know how to convert that ('foo' is not defined in the unit registry)."

    def test_temperature_regex(self, testbot):
        say_expect = [
            ("It's 30 degrees C", "30 °C = 86 °F"),
            ("It's 30 degrees Celsius", "30 °C = 86 °F"),
            ("It's 30 degrees C today", "30 °C = 86 °F"),
            ("It's 30 degrees c today", "30 °C = 86 °F"),
            ("It's 30 degrees Celsius today", "30 °C = 86 °F"),
            ("It's 30 degrees celsius today", "30 °C = 86 °F"),
            ("It's 30 degrees c.", "30 °C = 86 °F"),
            ("It's 30 degrees celsius.", "30 °C = 86 °F"),
            ("It's 30 celsius today", "30 °C = 86 °F"),
            ("It's 86 degrees Fahrenheit today", "86 °F = 30 °C"),
            ("It's -40 degrees Celsius today", "-40 °C = -40 °F"),
            ("30 degrees Celsius", "30 °C = 86 °F"),
            ("What's 37 degrees celsius in fahrenheit?", "37 °C = 98.6 °F"),
            ("What's 98.6 degrees fahrenheit in celsius?", "98.6 °F = 37 °C"),
        ]

        for item in say_expect:
            testbot.bot.push_message(item[0])
            assert testbot.bot.pop_message() == item[1]

        testbot.bot.push_message("It's 30 c today")
        testbot.bot.push_message("It's 30 f today")
        testbot.bot.push_message("It's 30 degrees celvin (I know Kelvin should be with a K)")

        # None of the above should match so response to this should be
        # first item returned by testbot.bot.pop_message().
        testbot.bot.push_message("!echo trick-to-avoid-wait-for-empty-queue")
        assert testbot.bot.pop_message() == "trick-to-avoid-wait-for-empty-queue"
