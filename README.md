# party-hat-generator
Party hat generator for 3D-printing

Print using vase - or spiral mode for best results. See printed hints when exporting.


## Installation
Tested with Python 3.9.
1. Clone this repository.
2. Create a virtual environment.
3. Install python dependencies using `pip -r requirements.txt`
4. For using emojis, download the Google Noto Emoji font here: https://fonts.google.com/noto/specimen/Noto+Emoji and put the font in a new folder called Noto_Emoji next to main.py. Like this: "Noto_Emoji/NotoEmoji-VariableFont_wght.ttf".


The last step will install a specific cadquery version, as this project is dependent on 3mf export format support. You could need to upgrade your slicer to use the produced files.