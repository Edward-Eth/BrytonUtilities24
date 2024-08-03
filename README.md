This is a forked version of @Mateus0312's "BrytonUtilities" repo, which I am making updates to to (hopefully) improve it.

# Intent
Bryton make a range of reasonably priced cycling head units with routing, recording and sensor connnectivity features, unfortunately they don't support importing externally created routes *with* their instructions. This means that when you import a route from eg PlotARoute.com, it will appear with just a line, making not missing turns challenging. The Bryton app features an "add turn by turn instructions" feature, but this often introduces unacceptable changes to the intended route as Bryton's road map may differ from the one you plotted on.

As such, the purpose of this codebase is to convert externally generated .Gpx (a type of extensable mark up language or .xml file) into a Bryton encoded .fit file, which can then be put on the device using a USB connection. When the device then opens this route it sees it as a Bryton app plotted route and displays instructions as intended.

# Limitations
As the exact formatting of .GPX files differs from source to source, at present the repo can only support files from PlotARoute.com or OpenRouteService. Adding new sources is encouraged, it only took me a few hours of work to add support for PlotARoute so it's not hugely difficult.

# Windows installation steps using git (if you want to contribute)
1. This repo is written for python 3.12, which can be downloaded here: https://www.python.org/downloads/ or by using the windows app store (easier for beginners)
2. You will also need to install git, for instructions go here: https://git-scm.com/download/win
3. After installing python 3.12, checkout the repo using this command: `git clone https://github.com/Edward-Eth/BrytonUtilities24.git` in the location you want to keep the files
4. Create a new virtual environment in the repo folder: `python -m venv BrytonUtilities24/BrytonUtilitiesVenv`
5. Change directory to within the repo: `cd BrytonUtilities24`
6. Activate the virtual environment: `BrytonUtilitiesVenv\Scripts\activate`
7. Update pip: `python -m pip install --upgrade pip`
8. Use pip to install the packages required for the repo: `pip install -r requirements.txt`
9. The repo is now ready to use, you may want to install an editor intended for python, such as pycharm, but this is user preference.

# Usage:
TODO: Add usage instructions.
