#! python
"""rivet_lib
    Processes the r-i-v-e-t design file to a calc and sets files and paths

    The language includes five types of f-strings where each type of string is
    evaluated by a function. The first line of each f-string can be a settings
    string.

    r__() : string of python code 
    i__() : string inserts text and images
    v__() : string defines calculation values
    e__() : string defines calculation equations
    t__() : string inserts tables and plots
    
"""

import sys
import os
import inspect
import __main__ as main
from pathlib import Path

import sympy as sy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import Image, Math, Latex, HTML, display
from numpy import *
from pandas import *

import rivet.rivet_check as _chk
import rivet.rivet_utf as _utf
#import rivet.rivet_pdf as _pdf
#import rivet.rivet_rst as _rst
#import rivet.rivet_units as _units

# import rivet.rivet_report as reprt
# from rivet.rivet_units import *
# from rivet.rivet_config import *
# from rivet.rivet_html import *
# from rivet.rivet_pdf import *

__version__ = "0.9.1"
__author__ = "rholland"

if sys.version_info < (3, 7):
    sys.exit("rivet requires Python version 3.7 or later")

global_rivet_dict = {}
eqnum, sectnum = 0, 0
designfile = main.__file__
_designfile = designfile
print('design file ', designfile)

# set up files and folders
try:
    _rivetpath = os.path.dirname("rivet.rivet_cfg")
    _designpath = os.path.dirname(_designfile)
    _designname = os.path.basename(_designfile)
    _projpath = os.path.dirname(_designpath)
    _calcpath = os.path.join(_projpath, "calcs")
    _bakfile = _designfile.split(".")[0] + ".bak"
    with open(_designfile, "r") as f2:
        _designbak = f2.read()
    with open(_bakfile, "w") as f3:
        f3.write(_designbak)
    print("< folders checked and design file backup written >")
except:
    sys.exit("< required folders and files not found - program stopped >")

# design paths
_spath = os.path.join(_designpath, "scripts")
_tpath = os.path.join(_designpath, "table")
# calc paths
_rpath = os.path.join(_calcpath, "pdf")
_upath = os.path.join(_calcpath, "txt")
_xpath = os.path.join(_calcpath, "temp")
_fpath = os.path.join(_calcpath, "figures")
_hpath = os.path.join(_calcpath, "html")
# calc file names
_designbase = _designname.split(".")[0]
_ctxt = ".".join([_designbase, "txt"])
_cpdf = ".".join([_designbase, "pdf"])
_chtml = ".".join([_designbase, "html"])
_trst = ".".join([_designbase, "rst"])
_tlog = ".".join([_designbase, "log"])
# laTex file names
_ttex1 = ".".join([_designbase, "tex"])
_auxfile = os.path.join(_designbase, ".aux")
_outfile = os.path.join(_designbase, ".out")
_texmak2 = os.path.join(_designbase, ".fls")
_texmak3 = os.path.join(_designbase, ".fdb_latexmk")
_cleantemp = (_auxfile, _outfile, _texmak2, _texmak3)
# flags and variables
_pdfflag = 0
_nocleanflag = 0
_verboseflag = 0
_defaultdec = "3,3"
_calcwidth = 80
_calctitle = "\n\nModel Title"  # default model title
_pdfmargin = "1.0in,0.75in,0.9in,1.0in"

# start checks and logs
# check config file and folder structure and start log
#_chk1 = chk.CheckRivet(_tlog)
#_chk1.logstart()
#_chk1.logwrite("< begin model processing >", 1

# design and report settings
with open(_designfile, 'r') as _df1:
     _dflist = _df1.readlines()
     for dfline in _dflist:
         if "|[design]|" in dfline:
             design_settings = dfline.split("|")
         if "|[report]|" in dfline:
             report_settings = dfline.split("|")

def _string_settings(first_line):
    """process string settings

    Method is called for each design string 
    
    """
    section_flg = -1
    design_descrip = " " 
    exec_flg = -1
    prt_state = 0  
    source_flg = -1
    str_source = "" 

    splt_string = first_line.split('|')
    if len(splt_string) > 0:
        try:
            for i in splt_string:        
                section_flg = i[0].find("[s]") 
                if section_flg > -1:
                    design_descrip = i[0][section_flg+3:].strip()
                else:
                    design_descrip = i[0].strip()

                exec_flg = i[1]
                if exec_flg.strip() == "[h]":
                    prt_state = 1
                elif exec_flg.strip() == "[x]":
                    prt_state = 2
        
                source = i[2] 
                if len(source).strip() > 0:
                    str_source = i[2].strip()
                else:
                    str_source = ""
        except:
            pass
            
    return [section_flg, design_descrip, prt_state, str_source]

def r__(fstr):
    """run python code

    """
    global eqnum, sectnum
    fstr1 = fstr.split("\n", 1)
    settings = _string_settings(fstr1[0])
    
    fstr2 = fstr1[1].splitlines()
    for i in fstr2:
        exec(i.strip())
    
    global_rivet_dict.update(locals())

def i__(fstr):
    """process insert string
    
    """
    global eqnum, sectnum
    fstr1 = fstr.split("\n", 1)
    settings = _string_settings(fstr1[0])
    if settings[2] == 2:
        return

    if settings[0] > 0:
        sectnum += 1

    fstr2 = fstr1[1].splitlines()
    
    if settings[2] == 0:
        for i in fstr2:
            print(i)

    global_rivet_dict.update(locals())

def v__(fstr):
    """process value string

    """
    global eqnum, sectnum
    fstr1 = fstr.split("\n", 1)
    fstr2 = fstr1[1].splitlines()
    str_set = _string_settings(fstr1[0])
    
    if str_set[2] == 2:
        return
    if str_set[2] == 1:
        vcalc = _utf.ExecV(fstr2)
        vdict1, vcalc1 = vcalc.vutf()
        global_rivet_dict.update(vdict1)
        return
    if str_set[2] == 0:
        vcalc = _utf.ExecV(fstr2)
        vdict1, vcalc1 = vcalc.vutf()
        global_rivet_dict.update(vdict1)
        if str_set[0] > -1:
            print("section: ", sectnum )
        for i in vcalc1:
            print(i)
    if "pdf" or "html" in design_settings[0]:
        rst_file = _rst.Write_rst()
            
def e__(fstr):
    """process equation string
    
    """
    global eqnum, sectnum
    settings = _string_settings(fstr[0])
    callv1 = vlist[0].split('|')
    for j in fstr.split("\n"):
        if len(j.strip()) > 0:
            if "=" in j:
                k = j.split("=")[1]
                nstr3 = str(j) + " = " + str(eval(k))
                print(nstr3)
                exec(j.strip(), globals())
            else:
                print(j)
    return global_rivet_dict.update(locals())

def t__(fstr):
    """process table string
    
    """
    global eqnum, sectnum
    settings = _string_setting(fstr[0])

    return global_rivet_dict.update(locals())

