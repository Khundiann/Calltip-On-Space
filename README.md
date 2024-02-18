
# Calltip On Space

## Introduction:

"Calltip On Space" is a script designed to enhance your coding experience in Notepad++. This script adds the missing functionality that displays calltips automatically when you type a space character, providing users that have to use languages that don't use wrappers for their arguments with an option to have calltips. Calltips in general offer quick access to function signatures and parameter information while writing code. Feel free to use any parts of the code in the script as long as its for opensource purposes,

Happy coding!

## Features:

- **Automatic Calltips**: Calltips are displayed automatically when you type a space character, allowing you to view function signatures and parameter details without interrupting your workflow.

- **Customizable Color Scheme**: The script offers customizable color settings for calltips, enabling you to personalize the appearance of calltip displays to match your preferences.

- **Support for User Defined Languages**: "Calltip On Space" seamlessly integrates with user-defined languages in Notepad++, ensuring compatibility across a wide range of programming languages and syntaxes.

## README:

### 1. Considerations & Preparation

Things to consider before install:

- You need a configured User Defined Language **"Autocomplete"** XML file to be able to show calltips. Find more information [here](https://npp-user-manual.org/docs/auto-completion/).
- When creating your **"Autcomplete"** XML file make sure to add the following parameters to the environment line.
- **\<Environment ignoreCase="yes" startFunc=" " stopFunc=" "/>**
- The **"ignoreCase"** is of no effect to this script because the script makes everything lowercase for comparison checks. But the addition of the **"startFunc"** and **"stopFunc"** are pretty important for Calltip On Space, because native calltips do not work with the space character its a good way to make sure that no other key will accidently activate the native calltips. Since activating the native calltips has undesirable behaviour when cycling calltips with the overload arrows with Calltip On Space, the cycling somehow makes both the native logic and this script want to show a calltip after that one native calltip run.
- To import your **"Autocomplete"** XML into the script go to **line 85** in the script and look for this line of code **XML_FILE_PATH = "autoCompletion/YOURLANGUAGENAME.XML"** and change **"YOURLANGUAGENAME"** to the exact name of your XML file.
- The undesirable behaviour mentioned above is of no concern when using other languages while the Calltip On Space script is running in the background, since there is a check **"   return notepad.getLanguageName(LANGTYPE.USER) == "udf - YOURLANGUAGENAME"** implemented in the script to only run with a specific User Defined Language, and when any other language is selected most of the script is dormant.
- To be able to use the script you will have to go to **line 168** in the script and look for the check mentioned above and change the **"YOURLANGUAGENAME"** part of the text to the **exact** name of your User Defined Language.
- If you want to change where the text file that holds the calltip color information is saved, look on **line 34** for **COLOR_SETTINGS_FILE = "calltip_color_settings.txt"** and change the path, the default path is the root folder of Notepad++. To put the file into the Scripts folder of the PythonScript plugin for example use **"plugins/Config/PythonScript/scripts"**.
- Should you want to change the default values of the calltip background and text color, this can be done by entering RGB values on **lines 29 and 30**.
- As mentioned in the [Notepad++ Online Manual](https://npp-user-manual.org/docs/auto-completion/), use **\&#x0a; for new lines** when formatting your text in the **Autocomplete** XML.

### 2. Installation:

To use "Calltip On Space," follow these simple steps:

- Install the PythonScript plugin in the Notepad++ **"Plugins Admin"** menu
- Copy the code inside the calltip.on.space.py file and paste code into a new file and save it as "calltip.on.space.py".
- Make the adjustments mentioned in the "Considerations & Preparation" part of the README.
- Save the script in the **\"..\plugins\Config\PythonScript\scripts"** directory for Notepad++ PythonScript scripts.
- Search for the script you just created in  the **"Plugins -Python Script -Scripts"** submenu, click the script to run it.
- Alternately you can create a menu item or button for it through the PythonScript **"Configuration menu"**. Remember that for buttons you have to restart Notepad++ for them to show up.

### 3. Triggering Calltips:

Once the script is installed and running, triggering calltips is easy:

- Begin typing code in Notepad++.
- Type a space character after a function or method name.
- The calltip for the corresponding function will automatically appear, providing you with useful information about its parameters and return values.
- If a function has multiple overloads, you can use arrow buttons within the calltip to cycle through them and view the details of each overload.

### 4. Customizing Calltip Colors:

You can customize the colors of calltips to suit your preferences:

- Best practice is to open a calltip first, that way you will have an example calltip while choosing colors.
- Type the keyword "calltip_color_settings" in your code.
- Press the spacebar
- This will open a color configuration GUI where you can adjust the background and text colors of calltips.
- Every time a color is chosen the script will show an updated calltip

![2024-02-06 15_12_23-Window](https://github.com/Khundiann/Calltip-On-Space/assets/151635111/8d30b99d-c7df-4221-8c45-8c68bb33fdc3)
