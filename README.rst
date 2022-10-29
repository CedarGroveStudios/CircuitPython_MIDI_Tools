Introduction
============




.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/CedarGroveStudios/CircuitPython_MIDI_Tools/workflows/Build%20CI/badge.svg
    :target: https://github.com/CedarGroveStudios/CircuitPython_MIDI_Tools/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

A collection of helpers for processing MIDI notes and Control Change codes.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install cedargrove_midi_tools

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

``note_or_name(note)``

Bidirectionally translates a MIDI sequential note value to a note name or a note
name to a MIDI sequential note value. Note values are of integer type in the
range of 0 to 127 (inclusive). Note names are character strings expressed
in the NoteOctave format, such as 'C4' or 'G#7'. Note names can range from
'C-1' (note value 0) to 'F#9' (note value 127). If the input value is outside
of the note value or name range, the value of ``None`` is returned.

.. code_block:: python

    >>> from cedargrove_midi_tools import note_or_name
    >>> note_or_name('G5')
    79
    >>> note_or_name(79)
    'G5'

``note_to_name(note)`` and ``name_to_note(name)``

Translates a MIDI sequential note value to a note name or note name to a note
value. Note values are of integer type in the range of 0 to 127 (inclusive).
Note names are strings expressed in the NoteOctave format, such as 'C4' or
'G#7'. Note names can range from 'C-1' (note value 0) to 'F#9' (note value 127).
If the input value is outside the range, the value of ``None`` is returned.

.. code_block:: python

    >>> from cedargrove_midi_tools import note_to_name, name_to_note
    >>> note_to_name(70)
    'A#4'
    >>> name_to_note('A#4')
    70

``note_to_frequency(note)`` and ``frequency_to_note(frequency)``

Translates a MIDI sequential note value to its corresponding frequency in
Hertz (Hz) or a frequency to its nearest note value. Note values are of integer
type in the range of 0 to 127 (inclusive). Frequency values are floating point.
If the input is outside of the range, the value ``None`` is returned.
Ref: MIDI Tuning Standard formula: https://en.wikipedia.org/wiki/MIDI_tuning_standard

.. code_block:: python

    >>> from cedargrove_midi_tools import note_to_frequency, frequency_to_note
    >>> note_to_frequency(60)
    261.625
    >>> frequency_to_note(261.63)
    60

``cc_code_to_description(cc_code)``

Provides a controller description decoded from a Control Change controller code
value.
Ref: https://www.midi.org/specifications-old/item/table-3-control-change-messages-data-bytes-2

.. code_block:: python

    >>> from cedargrove_midi_tools import cc_code_to_description
    >>> cc_code_to_description(24)
    'Ctrl_24'
    >>> cc_code_to_description(1)
    'Modulation'


Documentation
=============
API documentation for this library can be found `here <https://github.com/CedarGroveStudios/CircuitPython_MIDI_Tools/blob/main/media/pseudo_rtd_cedargrove_midi_tools.pdf>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/CedarGroveStudios/CircuitPython_MIDI_Tools/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
