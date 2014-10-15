err-converter
=============

.. image:: https://coveralls.io/repos/zoni/err-converter/badge.png?branch=master
   :target: https://coveralls.io/r/zoni/err-converter?branch=master
.. image:: https://travis-ci.org/zoni/err-converter.svg?branch=master
   :target: https://travis-ci.org/zoni/err-converter

Plugin for `Err <http://errbot.net>`_ to convert various measurements and metrics.


Requirements
------------

This plugin supports both Python 2 and 3. See `requirements.txt` for
further requirements.


Installation
------------

Give your bot the command `!repos install https://github.com/zoni/err-converter.git`.


Usage
-----

This plugin provides the `!convert` command to run conversions::

    >> !convert 20 celsius to fahrenheit
    20 degC = 68 degF
    >> !convert 1 meter to feet
    1 meter = 3.28084 foot
    >> !convert 75 miles/hour to kilometers/hour
    75 mile / hour = 120.701 kilometer / hour
    >> !convert 180 degrees to radians
    180 degree = 3.14159 radian

(Refer to the documentation for `Pint <https://pypi.python.org/pypi/Pint>`_ to
see all the values that are understood.)

Addiontally, it automatically listens to certain keywords/phrases spoken during
conversation to run conversions automatically. At the moment, this only works
for temperature conversions::

    >> It's 30 degrees Celsius today.
    30 degC = 86 degF
    >> It's 30 degrees C today.
    30 degC = 86 degF
    >> It's 30 Celsius today.
    30 degC = 86 degF


License
-------

The MIT License. See the file *LICENSE* for more details.
