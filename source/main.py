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
from sys import argv

###################################################
# configuration

# location of input gpx file
# gpx_path = argv[1]
gpx_path_par = r"C:\Users\Edward\Downloads\test2.gpx"
gpx_path_ors = r"C:\Users\Edward\Downloads\ors-route1.gpx"
# gpx_path = r"C:\Users\Edward\Downloads\ors-route1.gpx"


# defines tipe of files to be analyzed (options: none, fit)
analysis_mode = 'none'

###################################################
# analyzing files

# function to help decode fit files
analysis.analyze_fit_files(analysis_mode)

###################################################
# decoding input

# decoding gpx file
decoded_data_par, source_par = gpx_utilities.decode_gpx(gpx_path_par)
decoded_data_ors, source_ors = gpx_utilities.decode_gpx(gpx_path_ors)

###################################################
# working with data

converted_data_par = units_conversion.convert_input_units(decoded_data_par, source_par)
converted_data_ors = units_conversion.convert_input_units(decoded_data_ors, source_ors)
# INSERTED_POI = [POI NAME, POI ID, DISTANCE FROM START IN METERS]
# inserted_poi = ['BIG', b'\x66', 40000]

extracted_attributes_par = extract_data.extract_attributes(converted_data_par)
extracted_attributes_ors = extract_data.extract_attributes(converted_data_ors)

###################################################
# encoding output

plt.figure()
plt.plot(converted_data_par["longitude"], converted_data_par["latitude"])
plt.plot(converted_data_ors["longitude"], converted_data_ors["latitude"])
plt.show()

fit_path = gpx_path_par.replace('.gpx','.fit')
fit_encode.encode_fit(fit_path,converted_data_par,extracted_attributes_par)
