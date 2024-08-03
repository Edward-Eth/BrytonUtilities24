"""
This file is used to call the fit_decoder function to help understand the contents and formatting of the Bryton
 .fit files.
"""

import os

import fit_decode


def analyze_fit_files(analysis_mode):
    if analysis_mode == 'fit':
        fit_path = os.path.join(os.path.dirname(__file__) + '/files/fit/')

        print('Analyzing fit files in ' + fit_path)
        files = os.listdir(fit_path)
        for file in files:
            print('\n' + file)
            return fit_decode.decode_fit(fit_path + file)
    else:
        return 0
