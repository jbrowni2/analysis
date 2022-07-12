# analyis


Above are the analysis codes being developed for characterization of GEMINI detectors for COHERENT

# address.json

Contains the addresses where your data is held. This will need to be updated for your machine specifically.

# foundation.py

This is a library of basic definitions that can be done with digitizer data processed with PYGAMA. Such as loading data into dataframes.

# see_spectum.py

Creates an energy spectrum from a processed dsp file. Arguments needed to run this script are 

arg('-r', '--runs', nargs=1, type=str,
        help="list of files to calibrate (-r 'Run####-Run####') ")

arg('-b', '--bin', nargs='*', type=int, help='bins number for histogram')
arg('-x', '--xlim', nargs= 2, type=int, help='lower and upper limits in x plane (-x #### ####)')
arg('-n', '--name', nargs=1, type=str, help='name of the spectrum you want to see.')

# print_table.py

Prints out the dataframe of a dsp file. Arguments needed to run this script are

arg('-r', '--runs', nargs=1, type=str,
        help="list of files to calibrate (-r 'Run####-Run####') ")

# see_waveform.py

Prints a waveform from your raw file. Arguments needed to run this script are 

arg('-r', '--runs', nargs=1, type=str,
        help="list of files to calibrate (-r 'Run####-Run####') ")

arg('-i', '--index', nargs='*', type=int, help='index of waveform you want to see.')

# pairplot.py

prints a seaborn pairplot from your dsp file. Arguments needed to run this script are 

arg('-r', '--runs', nargs=1, type=str,
        help="list of files to calibrate (-r 'Run####-Run####') ")

# energy_resolution.py

This script is meant to calculate and plot a FWHM vs Energy for a given detector, but it is not working at the moment. It needs to be updated.

# drift_dist.py

Calculates the drift time of a detector, but it also needs to be updated.
