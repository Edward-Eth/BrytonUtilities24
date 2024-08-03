# This is a sample Python script.

# Press R to execute it or replace it with your code.
# Press Double to search everywhere for classes, files, tool windows, actions, and settings.

import gpx_utilities
import bin_utilities
import fit_decode
import fit_encode
import fit_utilities
import analysis
import extract_data
import units_conversion
import matplotlib.pyplot as plt
import sys
import os

###################################################
# configuration

# Find repo root
repoPath = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))


# location of demo input gpx file
gpx_path = os.path.join(repoPath,r"demoData\SerraRioDoRastro.gpx")

# defines tipe of files to be analyzed (options: none, fit)
analysis_mode = 'none'

###################################################
# analyzing files

# function to help decode fit files
analysis.analyze_fit_files(analysis_mode)

###################################################
# decoding input

# decoding gpx file
decoded_data, source = gpx_utilities.decode_gpx(gpx_path)

###################################################
# working with data

converted_data = units_conversion.convert_input_units(decoded_data, source)

# INSERTED_POI = [POI NAME, POI ID, DISTANCE FROM START IN METERS]
# inserted_poi = ['BIG', b'\x66', 40000]

extracted_attributes = extract_data.extract_attributes(converted_data)

###################################################
# encoding output

plt.figure()
plt.plot(converted_data["longitude"], converted_data["latitude"])
plt.show()

fit_path = gpx_path.replace('.gpx','.fit')
fit_encode.encode_fit(fit_path,converted_data,extracted_attributes)
