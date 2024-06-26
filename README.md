# party-hat-generator 🥳
<img src="partyhats.jpg" width="42%" alt="Partyhats" align="right">
Party hat generator for 3D-printing. Not suitable for children due to possible sharp edges and possible printing problems like delamination.
<br/><br/>
Print using vase -- or spiral mode -- for best results. See slicing hints when exporting.
<br/><br/>
Note: Text cutting and union + filleting is a little bit buggy, maybe used wrong, so all words will not work. Font size below 20 will increase failure rate. A possible quick-fix is to increase the model size 100% or more, and scale back before export or in the slicer. This is not implemented.

## License, see formal LICENSE file and this Suno AI song:
https://github.com/kristianmk/party-hat-generator/assets/1713062/72897062-d188-467a-9c4d-a07b666da05b

(Original idea from https://x.com/goodside/status/1775713487529922702?s=20)

## Installation
### Recommended way (conda)
Tested with Python 3.11.
1. Clone this repository.
2. Install miniforge (macos: `brew install miniforge`)
3. Create a virtual environment for qadquery 2 and install a specific version (tested with party hat generator):
```
conda create -n cq22
conda activate cq22
conda install -c conda-forge cadquery=2.2.0 occt=7.7.0
```
4. For using emojis, download the Google Noto Emoji font here: https://fonts.google.com/noto/specimen/Noto+Emoji and put the font in a new folder called Noto_Emoji next to main.py. Like this: "Noto_Emoji/NotoEmoji-VariableFont_wght.ttf".


### Deprecated (pip)
Using pip, not recommended as cadquery 2 series plays better with conda.
Tested with Python 3.9.
1. Clone this repository.
2. Create a virtual environment.
3. Install python dependencies using `pip install -r requirements.txt`
4. For using emojis, download the Google Noto Emoji font here: https://fonts.google.com/noto/specimen/Noto+Emoji and put the font in a new folder called Noto_Emoji next to main.py. Like this: "Noto_Emoji/NotoEmoji-VariableFont_wght.ttf".


Step 3 will install a specific cadquery version, as this project is dependent on 3mf export format support. You could need to upgrade your slicer to use the produced files.

## Making a hat
Edit list of names, icons and/or font size in main.py. Run main.py from the conda (or pip) virtual environment, and hopefully get a 3mf file ready for slicing using Cura or another 3D printer software.

Material consumption: Around 12 grams of PLA filament for one hat (95 mm diameter).

## Some nice filaments for hats
Elefun: https://www.elefun.no/p/prod.aspx?v=55582 (not an advertisement, this is the filament type used for the printed hats (picture).)
