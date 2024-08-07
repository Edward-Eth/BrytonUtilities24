This is a forked version of @Mateus0312's "BrytonUtilities" repo, which I am updating to (hopefully) improve it.

# Intent
Bryton make a range of reasonably priced cycling head units with routing, recording and sensor connectivity features, unfortunately they don't support importing externally created routes *with* their instructions. This means that when you import a route from e.g. PlotARoute.com, it will appear with just a line, making not missing turns challenging. The Bryton app features an "add turn by turn instructions" feature, but this often introduces unacceptable changes to the intended route as Bryton's road map may differ from the one you plotted on.

As such, the purpose of this codebase is to convert externally generated .Gpx (a type of extensible mark up language or .xml file) into a Bryton encoded .fit file, which can then be put on the device using a USB connection. When the device then opens this route it sees it as a Bryton app plotted route and displays instructions as intended.

# Limitations
As the exact formatting of .GPX files differs from source to source, at present the repo can only support files from PlotARoute.com or OpenRouteService. Adding new sources is encouraged, it only took me a few hours of work to add support for PlotARoute, so it's not hugely difficult.

Additionally, at present this code has only been developed for/tested on Bryton 420 units, so I cannot guarantee compatibility with any other head unit by Bryton, or any unit by any other manufacturer.

# Disclaimer
I provide no guarantee of the accuracy/reliability of this code, I always recommend taking a phone with you when cycling an unfamiliar route, or even a map if you will be in remote areas without mobile service.

# Using without installing locally
It is (TODO) possible to use this repo to convert files without installing it locally on your computer, all you need is a (free) github account.
1. Create a new branch:
    1. Click on the branch icon in the top left of the files list
    2. Click "view all branches"
    3. In the new windows, click on the top right button "create new branch"
2. In your new branch, add your gpx files to convert in the "toConvert" folder inside the "onlineConversion" folder
3. Commit your changes
4. Go to the actions tab and wait for the  "conversion" action to complete (complete once a green arrow appears)
5. Go back to the "code" window and open the "convertedFiles" folder inside "onlineConversion"
6. This folder should now contain your converted files
7. To get the files onto your Bryton rider, follow the steps further down in this readme

# Local Windows installation steps using git (if you want to contribute)
1. This repo is written for python 3.12, which can be downloaded here: https://www.python.org/downloads/
2. You will also need to install git, for instructions go here: https://git-scm.com/download/win
3. After installing python 3.12, checkout the repo using this command: `git clone https://github.com/Edward-Eth/BrytonUtilities24.git` in the location you want to keep the files
4. Create a new virtual environment in the repo folder: `python -m venv BrytonUtilities24/BrytonUtilitiesVenv`
5. Change directory to within the repo: `cd BrytonUtilities24`
6. Activate the virtual environment: `BrytonUtilitiesVenv\Scripts\activate`
7. Update pip: `python -m pip install --upgrade pip`
8. Use pip to install the packages required for the repo: `pip install -r requirements.txt`
9. The repo is now ready to use, you may want to install an editor intended for python, such as pycharm, but this is user preference
10. You may need to modify your systems TCL path to make matplotlib work correctly.

# Local usage:
In order to use this code base to convert a .gpx file into a .fit file you need to:
1. Install using above steps
2. Download your .gpx file, ensuring you select any "include instructions/waypoints" option present
3. Use this command: `python pathToRepo\BrytonUtilities24\source\main.py pathToGpxFile\gpxFile.gpx`
4. This will run the conversion and plot a map of the input route as a sanity check

# Getting files onto your Bryton
1. Plug your Bryton into your computer/laptop/(possibly phone? to test)
2. Move the exported .fit files into the "XXX" folder (To check name) on the Bryton
3. Eject the bryton and unplug it
4. On the Bryton, go to "tracks" and select the new route
5. Once processed the Bryton should display the route and give instructions as you ride
