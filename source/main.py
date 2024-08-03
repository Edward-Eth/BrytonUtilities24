r"""
This is the "main" file for the Bryton gpx converter code base. You can call this script to convert
a gpx file from terminal using:

python pathToFile\main.py pathToGpx\nameOfGpx.gpx

Alternatively, if you run the script without arguments it will perform a demo conversion on the
demoData SierraRioDoRastro.gpx file.

The script will convert the input .gpx file into an output .fit file, and plot a top-down view of
the route for sanity checking.
"""
import os
import sys

import matplotlib.pyplot as plt

import extract_data
import fit_encode
import gpx_utilities
import units_conversion

# If the script was called with arguments, we use the first argument as the gpx source file path.
if len(sys.argv) != 1:
    gpx_path = sys.argv[1]
# Else we use the file from the demo files folder.
else:
    # Find repo root to locate demo files regardless of where script was called from.
    repoPath = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
    # Join the path to the repo to the path to the demo file within the repo
    gpx_path = os.path.join(repoPath, r"demoData\SerraRioDoRastro.gpx")

# Calling the gpx file reader to extract necessary data from the .gpx file.
decoded_data, source = gpx_utilities.decode_gpx(gpx_path)

# Calling the unit converter to convert extracted units and shorten extracted Instruction names.
converted_data = units_conversion.convert_input_units(decoded_data, source)

# Extracting additional attributes from the extracted data, such as route bounding boxes, Instruction
# distances and climb information.
extracted_attributes = extract_data.extract_attributes(converted_data)

# Plotting the extracted route for a sanity check.
plt.figure()
plt.plot(converted_data["longitude"], converted_data["latitude"])
plt.show()

# Exporting the file, first change input path to output path by appending ".fit" and then run the
# fit encoder.
fit_path = gpx_path.replace('.gpx', '.fit')
fit_encode.encode_fit(fit_path, converted_data, extracted_attributes)
