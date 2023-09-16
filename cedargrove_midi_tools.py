# SPDX-FileCopyrightText: Copyright (c) 2023 JG for Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`cedargrove_midi_tools`
================================================================================

A collection of helpers for processing MIDI notes and Control Change codes.

* Author(s): JG

Implementation Notes
--------------------
**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
"""

from math import log  # Required for freq_note helper

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/CedarGroveStudios/CircuitPython_MIDI_Tools.git"


# Note names used by note_or_name, note_name, and name_note helpers
NOTE_BASE = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def note_or_name(value):
    """Bidirectionally translates a MIDI sequential note value to a note name
    or a note name to a MIDI sequential note value. Note values are integers in
    the range of 0 to 127 (inclusive). Note names are character strings
    expressed in the format NoteOctave such as 'C4' or 'G#7'. Note names range
    from 'C-1' (note value 0) to 'F#9' (note value 127). If the input value is
    outside the note value or name range, the value of `None` is returned.

    :param union(int, str) value: The note name or note value input. Note value
    is an integer Note name is a string. No default value.
    """
    if isinstance(value, str):
        # Input is a string, so it's a note name
        return name_to_note(value)
    if isinstance(value, int):
        # Input is an integer, so it's a note value
        return note_to_name(value)
    return None  # Invalid input parameter type


def note_to_name(note):
    """Translates a MIDI sequential note value to a note name. Note values are
    integers in the range of 0 to 127 (inclusive). Note names are character
    strings expressed in the format NoteOctave such as 'C4' or 'G#7'. Note
    names range from 'C-1' (note value 0) to 'F#9' (note value 127). If the
    input value is outside that range, the value of `None` is returned.

    :param int note: The note value input in the range of 0 to 127 (inclusive).
    No default value.
    """
    if 0 <= note <= 127:
        return NOTE_BASE[note % 12] + str((note // 12) - 1)
    return None  # Note value outside valid range


def name_to_note(name):
    """Translates a note name to a MIDI sequential note value. Note names are
    character strings expressed in Scienfic Pitch Notation (NoteOctave) format
    such as 'C4' or 'G#7' with middle C defined as 'C4'. Note names range from
    'C-1' (note value 0) to 'G9' (note value 127). Note values are of integer
    type in the range of 0 to 127 (inclusive). If the input value is outside
    that range, the value of `None` is returned.

    :param str name: The note name input in SPN format. No default value.
    """
    name = name.upper()  # Convert lower to uppercase
    if "-" in name:
        octave = int(name[-2:])
        name = name[:-2]
    else:
        octave = int(name[-1:])
        name = name[:-1]

    if name in NOTE_BASE:
        # Note name is valid
        note = NOTE_BASE.index(name)
        midi_note = note + (12 * (octave + 1))  # MIDI note value
        if 0 <= midi_note <= 127:
            return midi_note
    return None  # Name is invalid or outside MIDI value range


def note_to_frequency(note):
    """Translates a MIDI sequential note value to a corresponding frequency in
    Hertz (Hz). Note values are integers in the range of 0 to 127 (inclusive).
    Frequency values are floating point. If the input note value is less than
    0 or greater than 127, the input is invalid and the value of `None` is
    returned. Ref: MIDI Tuning Standard formula:
    https://en.wikipedia.org/wiki/MIDI_tuning_standard

    :param int note: The MIDI note value input in the range of 0 to 127
    (inclusive). No default.
    """
    if 0 <= note <= 127:
        return pow(2, (note - 69) / 12) * 440
    return None  # note value outside valid range


def frequency_to_note(frequency):
    """Translates a frequency in Hertz (Hz) to a MIDI sequential note value.
    Frequency values are floating point. Note values are integers in the range
    of 0 to 127 (inclusive). If the input frequency is less than the
    corresponding frequency for note 0 or greater than note 127, the note value
    cannot be determined and `None` is returned. Ref: MIDI Tuning Standard
    formula:
    https://en.wikipedia.org/wiki/MIDI_tuning_standard

    :param float frequency: The frequency value input in Hz. No default.
    """
    if (pow(2, (0 - 69) / 12) * 440) <= frequency <= (pow(2, (128 - 69) / 12) * 440):
        return int(69 + (12 * log(frequency / 440, 2)))
    return None  # Frequency outside valid range


def frequency_to_note_cents(frequency):
    """Translates a frequency in Hertz (Hz) to a MIDI sequential note value and
    positive offset in cents. Frequency values are floating point. Note values
    are integers in the range of 0 to 127 (inclusive). Cent values range from
    0 to +100 cents. If the input frequency is less than the corresponding
    frequency for note 0 or greater than note 127, the note value cannot be
    determined and `None` is returned. Ref: MIDI Tuning Standard and cent
    formulae:
    https://en.wikipedia.org/wiki/MIDI_tuning_standard
    https://en.wikipedia.org/wiki/Cent_(music)

    :param float frequency: The frequency value input in Hz. No default.
    """
    if (pow(2, (0 - 69) / 12) * 440) <= frequency <= (pow(2, (128 - 69) / 12) * 440):
        note = int(69 + (12 * log(frequency / 440, 2)))
        note_freq = pow(2, (note - 69) / 12) * 440
        return note, int(1200 * log(frequency / note_freq, 2))
    return None, None  # Frequency outside valid range


# Controller descriptions -- no list offset
#   0-63 continuous, 64-121 switch, 122-127 channel mode
CONTROLLERS = [
    "Bank_Select",
    "Modulation",
    "Breath_Ctrl",
    "Ctrl_3",
    "Foot_Ctrl",
    "Portamento_Time",
    "Data_Entry_MSB",
    "Chan_Vol",
    "Balance",
    "Ctrl_9",
    "Pan_Ctrl",
    "Exp_Pedal",
    "FX_Ctrl_1",
    "FX_Ctrl_2",
    "Ctrl_14",
    "Ctrl_15",
    "Gen_Pur_1",
    "Gen_Pur_2",
    "Gen_Pur_3",
    "Gen_Pur_4",
    "Ctrl_20",
    "Ctrl_21",
    "Ctrl_22",
    "Ctrl_23",
    "Ctrl_24",
    "Ctrl_25",
    "Ctrl_26",
    "Ctrl_27",
    "Ctrl_28",
    "Ctrl_29",
    "Ctrl_30",
    "Ctrl_31",
    "Bank_Sel_LSB",
    "Modulation_LSB",
    "Breath_Ctrl_LSB",
    "Ctrl_3_LSB",
    "Foot_Ctrl_LSB",
    "Portamento_Time_LSB",
    "Data_Entry_LSB",
    "Chan_Vol_LSB",
    "Balance_LSB",
    "Ctrl_9_LSB",
    "Pan_Ctrl_LSB",
    "Exp_Pedal_LSB",
    "FX_Ctrl_1_LSB",
    "FX_Ctrl_2_LSB",
    "Ctrl_14_LSB",
    "Ctrl_15_LSB",
    "Gen_Pur_1_LSB",
    "Gen_Pur_2_LSB",
    "Gen_Pur_3_LSB",
    "Gen_Pur_4_LSB",
    "Ctrl_20_LSB",
    "Ctrl_21_LSB",
    "Ctrl_22_LSB",
    "Ctrl_23_LSB",
    "Ctrl_24_LSB",
    "Ctrl_25_LSB",
    "Ctrl_26_LSB",
    "Ctrl_27_LSB",
    "Ctrl_28_LSB",
    "Ctrl_29_LSB",
    "Ctrl_30_LSB",
    "Ctrl_31_LSB",
    "Sus_Damp_Pedal_sw",
    "Portamento_sw",
    "Sostenuto_sw",
    "Soft_Pedal_sw",
    "Legato_Foot_sw",
    "Hold_2_sw",
    "Sound_Ctrl_1_Variation",
    "Sound_Ctrl_2_Timbre",
    "Sound_Ctrl_3_Release",
    "Sound_Ctrl_4_Attack",
    "Sound_Ctrl_5_Bright",
    "Sound_Ctrl_6_Decay",
    "Sound_Ctrl_7_Vib_Rate",
    "Sound_Ctrl_8_Vib_Depth",
    "Sound_Ctrl_9_Vib_Delay",
    "Sound_Ctrl_10",
    "Gen_Pur_5",
    "Gen_Pur_6",
    "Gen_Pur_7",
    "Gen_Pur_8",
    "Portamento_Ctrl",
    "Ctrl_85",
    "Ctrl_86",
    "Ctrl_87",
    "HR_Vel_Prefix",
    "Ctrl_89",
    "Ctrl_90",
    "FX_1_Depth_Reverb",
    "FX_2_Depth",
    "FX_3_Depth",
    "FX_4_Depth",
    "FX_5_Depth",
    "Data_Inc + Value",
    "Data_Dec + Value",
    "NRPN_LSB + Value",
    "NRPN_MSB + Value",
    "RPN_LSB + Value",
    "RPN_MSB + Value",
    "Ctrl_102",
    "Ctrl_103",
    "Ctrl_104",
    "Ctrl_105",
    "Ctrl_106",
    "Ctrl_107",
    "Ctrl_108",
    "Ctrl_109",
    "Ctrl_110",
    "Ctrl_111",
    "Ctrl_112",
    "Ctrl_113",
    "Ctrl_114",
    "Ctrl_115",
    "Ctrl_116",
    "Ctrl_117",
    "Ctrl_118",
    "Ctrl_119",
    "All_Sound_Off",
    "Reset_All_Ctrls",
    "Local_Ctrl_Sw",
    "All_Notes_Off",
    "Omni_Mode_Off",
    "Omni_Mode_On",
    "Mono_Mode_On",
    "Poly_Mode_On",
]


def cc_code_to_description(cc_code):
    """Provides a controller description decoded from a Control Change code value.
    https://www.midi.org/specifications-old/item/table-3-control-change-messages-data-bytes-2

    :param int cc_code: The Control Change code value in the range of 0 to 127.
    No default value.
    """
    return CONTROLLERS[cc_code]
