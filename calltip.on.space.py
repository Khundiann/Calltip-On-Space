# Calltip On Space 1.0
# Copyright (C) <2024>  <khundian.twitch@gmail.com>
# This script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this script. If not, see <https://www.gnu.org/licenses/>.

import xml.etree.ElementTree as ET
from collections import defaultdict
import Tkinter as tk  # Python 2.7.18 compatibility
import tkColorChooser as colorchooser  # Python 2.7.18 compatibility
import os
import json
import time
import textwrap

# Newline character
NL = "\n"

# RGB tuples for colors
DEFAULT_BACKGROUND_COLOR = (40, 44, 52)  # Dark background color
DEFAULT_TEXT_COLOR = (189, 172, 172)  # Light grey text color


# Initialize variables
COLOR_SETTINGS_FILE = "calltip_color_settings.txt"
"""
Change the line above to where you want so save
your colorchooser settings. Default location is
the root folder of Notepad++.
"""


def load_color_settings():
    """
    Load color settings from a file.

    Returns:
    dict or None: A dictionary containing color settings
    if successfully loaded, or None if there was an error.
    """
    try:
        with open(COLOR_SETTINGS_FILE, "r") as file:
            return json.load(file) if file else None
    except Exception as e:
        return None


def save_color_settings():
    """
    Save color settings to a file.

    Returns:
    None
    """
    try:
        with open(COLOR_SETTINGS_FILE, "w") as file:
            json.dump(COLOR_SETTINGS, file)
    except Exception as e:
        return None


# Check if the color settings file exists, create if not
if not os.path.exists(COLOR_SETTINGS_FILE):
    save_color_settings()

COLOR_SETTINGS = load_color_settings()

if COLOR_SETTINGS is None:
    COLOR_SETTINGS = {
        "background_color": list(DEFAULT_BACKGROUND_COLOR),
        "text_color": list(DEFAULT_TEXT_COLOR),
    }


# Parse the XML file containing auto-completion data
XML_FILE_PATH = "autoCompletion/YOURLANGUAGENAME.xml"
"""
Update part of the line above "YOURLANGUAGENAME.xml"
with the name of your User Defined Language "AutoComplete"
file, best not change the folder location or you will lose
"Function" completion functionality for yourlanguage in Notepad++.

You should use the line below in your XML file

<Environment ignoreCase="yes" startFunc=" " stopFunc=" "/>

To prevent buggy behaviour when cycling through overloads.
After accidently hitting the default character "(" for
opening calltips in Notepad++.
"""
tree = ET.parse(XML_FILE_PATH)
root = tree.getroot()

# Dictionary to store parsed data
DATA_DICT = {}


# Convert XML ElementTree to dictionary
def etree_to_dict(t):
    """
    Convert an ElementTree element to a nested dictionary.

    Args:
    t (Element): The ElementTree element to convert.

    Returns:
    dict: A nested dictionary representation of the ElementTree element.
    """
    # Initialize the dictionary with the tag of the element
    d = {t.tag: {} if t.attrib else None}

    # Get the list of children elements
    children = list(t)

    # If the element has children
    if children:
        # Use a defaultdict to store child elements with the same tag in a list
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)

        # Update the main dictionary with the nested structure
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}

    # If the element has attributes, update the dictionary with attribute key-value pairs
    if t.attrib:
        d[t.tag].update(("" + k, v) for k, v in t.attrib.items())

    # If the element has text content
    if t.text:
        text = t.text.strip()

        # If the element has children or attributes, create a sub-dictionary with the text content
        if children or t.attrib:
            if text:
                d[t.tag]["#text"] = text
        else:
            # If there are no children or attributes, update the main dictionary with the text content
            d[t.tag] = text

    # Return the final dictionary representing the ElementTree element
    return d


# Populate DATA_DICT with parsed XML content
DATA_DICT = etree_to_dict(root)


# Function to check if language is "udf - YOURLANGUAGENAME"
def check_language():
    """
    Check if the current language in Notepad++ is
    "udf - YOURLANGUAGENAME".

    Returns:
    bool: True if the language is "udf - YOURLANGUAGENAME", False otherwise.
    """
    return notepad.getLanguageName(LANGTYPE.USER) == "udf - YOURLANGUAGENAME"
    """
    Update part the of the line above "YOURLANGUAGENAME"
    to the exaxt name of your User Defined Language.
    """


# Loop and wait for the language to be "udf - YOURLANGUAGENAME"
while not check_language():
    time.sleep(1)  # Sleep for 1 second before checking again

# Clear existing callbacks in Notepad++
editor.clearCallbacks()


# Function to update calltip based on current position
def update_calltip(pos):
    """
    Update the calltip based on the current position in the editor.

    Parameters:
    - pos (int): The current position in the editor.

    Returns:
    None
    """
    global current_overload_index, total_overloads, retval_values, current_search_word, NL, name

    # Extract the search word based on the current position
    search_word = editor.getTextRange(
        editor.wordStartPosition(pos, True), editor.wordEndPosition(pos, True)
    ).lower()

    # Check if the search word is present in the auto-completion data
    for keyword in DATA_DICT["NotepadPlus"]["AutoComplete"]["KeyWord"]:
        if keyword.get("name").lower() == search_word:
            current_search_word = search_word
            name = keyword.get("name")
            overloads = keyword.get("Overload")

            retval_values = overloads if isinstance(overloads, list) else [overloads]
            total_overloads = len(retval_values)
            current_overload_index = 0

            overload_counter = (
                "\001"
                + str(current_overload_index + 1)
                + " of "
                + str(total_overloads)
                + "\002"
                if total_overloads > 1
                else ""
            )
            retval = retval_values[current_overload_index].get("retVal")
            param = retval_values[current_overload_index]["Param"].get("name")
            descr = retval_values[current_overload_index].get("descr")

            # Construct calltip content
            calltip = (
                overload_counter
                + " "
                + retval
                + " "
                + name
                + " "
                + param
                + NL
                + descr
                + NL
            )

            # Format calltip content for display
            calltip_wrap = NL.join(
                [
                    (
                        NL.join(
                            textwrap.wrap(
                                line,
                                70,
                                break_long_words=False,
                                replace_whitespace=False,
                            )
                        )
                        if idx == 0
                        else NL.join(
                            textwrap.wrap(
                                line,
                                70,
                                break_long_words=False,
                                replace_whitespace=False,
                            )
                        )
                    )
                    for idx, line in enumerate(calltip.splitlines())
                    if line.strip() != ""
                ]
            )

            # Set colors and display the calltip
            editor.callTipSetBack(tuple(COLOR_SETTINGS["background_color"]))
            editor.callTipSetFore(tuple(COLOR_SETTINGS["text_color"]))
            editor.callTipShow(pos, calltip_wrap)
            return

    # If search word not found, cycle through overloads if available
    if total_overloads != 0:  # Check if total_overloads is not zero
        current_overload_index = (current_overload_index) % total_overloads

        overload_counter = (
            "\001"
            + str(current_overload_index + 1)
            + " of "
            + str(total_overloads)
            + "\002"
            if total_overloads > 1
            else ""
        )
        retval = retval_values[current_overload_index].get("retVal")
        param = retval_values[current_overload_index]["Param"].get("name")
        descr = retval_values[current_overload_index].get("descr")

        # Construct calltip content for cycling through overloads
        calltip = (
            overload_counter + " " + retval + " " + name + " " + param + NL + descr + NL
        )

        # Format calltip content for display
        calltip_wrap = NL.join(
            [
                (
                    NL.join(
                        textwrap.wrap(
                            line,
                            70,
                            break_long_words=False,
                            replace_whitespace=False,
                        )
                    )
                    if idx == 0
                    else NL.join(
                        textwrap.wrap(
                            line,
                            70,
                            break_long_words=False,
                            replace_whitespace=False,
                        )
                    )
                )
                for idx, line in enumerate(calltip.splitlines())
                if line.strip() != ""
            ]
        )

        # Set colors and display the calltip
        editor.callTipSetBack(tuple(COLOR_SETTINGS["background_color"]))
        editor.callTipSetFore(tuple(COLOR_SETTINGS["text_color"]))
        editor.callTipShow(pos, calltip_wrap)
    else:
        # If total_overloads is zero, there are no overloads to cycle through
        editor.callTipCancel()

# Function triggered when a calltip element is clicked
def on_calltip_click(args):
    """
    Handle the click event on a calltip element.

    Parameters:
    - args (dict): Arguments containing information about the click event.

    Returns:
    None
    """
    global current_overload_index, name
    pos = args["position"]

    # Update the current overload index based on the clicked position
    if pos == 2:
        current_overload_index = (current_overload_index + 1) % total_overloads
    elif pos == 1:
        current_overload_index = (current_overload_index - 1) % total_overloads
    elif pos == 0:
        current_overload_index = (current_overload_index) % total_overloads

    # Update the calltip based on the new overload index
    update_calltip(editor.getCurrentPos())


def on_char_add(args):
    """
    Handle the event when a character is added to the editor.

    Parameters:
    - args (dict): Arguments containing information about the character addition event.

    Returns:
    None
    """
    added_char = args["ch"]

    # If the added character is a space, update the calltip
    if added_char == ord(" "):  # Use 'ord' to get ASCII value for space
        pos = editor.getCurrentPos() - 1
        char_search_word = editor.getTextRange(
            editor.wordStartPosition(pos, True), editor.wordEndPosition(pos, True)
        ).lower()

        # Check if the char_search_word is the same as the chosen string
        if char_search_word == "calltip_color_settings":
            # Trigger color configuration interface
            configure_colors()
        elif any(
            keyword.get("name").lower() == char_search_word
            for keyword in DATA_DICT["NotepadPlus"]["AutoComplete"]["KeyWord"]
        ):
            update_calltip(pos)
        else:
            editor.callTipCancel()


def configure_colors():
    """
    Configure colors using a GUI interface.

    Returns:
    None
    """
    global COLOR_SETTINGS

    # Create Tkinter window
    root = tk.Tk()
    root.title("Color Configuration")

    # Set the window to always stay on top
    root.wm_attributes("-topmost", 1)

    # Function to set background color
    def set_background_color():
        color = colorchooser.askcolor(
            tuple(COLOR_SETTINGS["background_color"]), title="Choose Background Color"
        )
        if color[1]:
            COLOR_SETTINGS["background_color"] = [int(x) for x in color[0]]
            save_color_settings()
            update_calltip(editor.getCurrentPos())

    # Function to set text color
    def set_text_color():
        color = colorchooser.askcolor(
            tuple(COLOR_SETTINGS["text_color"]), title="Choose Text Color"
        )
        if color[1]:
            COLOR_SETTINGS["text_color"] = [int(x) for x in color[0]]
            save_color_settings()
            update_calltip(editor.getCurrentPos())

    # Label and buttons for color configuration
    label = tk.Label(root, text="Configure Calltip Colors")
    label.pack(pady=10)

    background_button = tk.Button(
        root, text="Choose Background Color", command=set_background_color
    )
    background_button.pack(pady=10)

    text_button = tk.Button(root, text="Choose Text Color", command=set_text_color)
    text_button.pack(pady=10)

    reset_button = tk.Button(root, text="Reset to Default", command=reset_to_default)
    reset_button.pack(pady=10)

    root.mainloop()


def reset_to_default():
    """
    Reset colors to default.

    Returns:
    None
    """
    global COLOR_SETTINGS
    COLOR_SETTINGS = {
        "background_color": list(DEFAULT_BACKGROUND_COLOR),
        "text_color": list(DEFAULT_TEXT_COLOR),
    }
    save_color_settings()
    update_calltip(editor.getCurrentPos())


# Register callbacks for relevant events
editor.callback(on_char_add, [SCINTILLANOTIFICATION.CHARADDED])
editor.callback(on_calltip_click, [SCINTILLANOTIFICATION.CALLTIPCLICK])


# Initialize variables
current_overload_index, total_overloads, retval_values, current_search_word = (
    0,
    0,
    [],
    "",
)
