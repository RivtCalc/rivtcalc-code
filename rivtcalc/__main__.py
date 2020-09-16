"""
***rivtcalc** may be run interactively from and editor or IDE, one cell (#%%),
or from command line. If run as a command line file the command is:

    python -m rivtcalc rddss_calcfile.py 

where ddss is the calc number made up of a two digit division plus subdivision
number. The calc number is used for document and report organization. UTF calcs
are always printed to to the terminal when the calc or interactive cell is run.
If a file output type (utf, pdf and html) is specified within the calc the
entire calc is processed and the calc file(s) are written to disk."""

import os
import sys
import textwrap
import logging
import warnings
import re
import importlib
import numpy as np
from pathlib import Path
from collections import deque
from typing import List, Set, Dict, Tuple, Optional

import rivtcalc.rc_lib as rc
import rivtcalc.rc_calc as _rc_calc

__version__ = "0.8.1-beta.1"
__author__ = "rholland@structurelabs.com"
if sys.version_info < (3, 7):
    sys.exit("rivtCalc requires Python version 3.7 or later")     

def _cmdlinehelp():
    """command line help """
    print()
    print("Run rivtCalc at the command line in the 'calc' folder with:")
    print("     python  -m rivtcalc rddcc_modelfile.py")
    print("where rddcc_ calcname.py is the model file in the folder")
    print("and **ddcc** is the model number")
    print()
    print("Specified output is written to the 'calc' or 'doc' folder:")
    print("     ddcc_userdescrip.txt")
    print("     ddcc_userdescrip.html")
    print("     ddcc_userdescrip.pdf")
    print("Logs and other intermediate files are written to the temp subfolder.")
    print()
    print("Program and documentation are here: http://rivtcalc.github.io.")
    sys.exit()

_modfileS = "empty"
if __name__ == "__main__":
    try:
        _modfileS = sys.argv[1]                       # model file argument
        _cwdS = os.getcwd()
        _cfull = Path(_modfileS)                      # model file full path
        _cfileS = Path(_cfull).name                   # calc file name
        _cname  = _cfileS.split(".py")[0]             # calc file basename
        print("current folder: ", os.getcwd())
        print("model name: ", _cfileS)
        importlib.import_module(_cname)
    except ImportError as error:
        print("error---------------------------------------------")
        print(error)
    except Exception as exception:
        # Output unexpected Exceptions.
        print("exception-----------------------------------------")
        print(exception)


