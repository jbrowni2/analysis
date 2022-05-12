# analyis


Above are the analysis codes being developed for characterization of GEMINI detectors for COHERENT

# foundation.py

This is a library of basic definitions that can be done with digitizer data processed with PYGAMA. Such as loading data into dataframes.

# see_spectum.py

Creates an energy spectrum from a processed dsp file. Arguments needed to run this script are 

arg('-r', '--runs', nargs=1, type=str,
        help="list of files to calibrate (-r 'Run####-Run####') ")

arg('-b', '--bin', nargs='*', type=int, help='bins number for histogram')
arg('-x', '--xlim', nargs= 2, type=int, help='lower and upper limits in x plane (-x #### ####)')
arg('-n', '--name', nargs=1, type=str, help='name of the spectrum you want to see.')
