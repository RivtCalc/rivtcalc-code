from __future__ import print_function
import os
import time
import oncepy.oconfig as cfg

class ModCheck(object):

    def __init__(self):
        """ open log file of events and errors"""
        # calc log
        lname = cfg.mfile
        logn = lname.split('.')
        self.logname = '.'.join(['log' + logn[0], logn[1], logn[2]])

    def ewrite1(self):
        """delete log file and initialize new file"""
        try:
            os.remove(self.logname)
        except:
            pass
        #print('log', estrng)
        ef = open(self.logname, 'w')
        ef.write("< start log - todo: write error logs >\n")
        ef.write("< time.strftime('%c') >\n")
        ef.close()

    def ewrite2(self, estrng):
        """write processes"""
        #print('log', estrng)
        ef = open(self.logname, 'a')
        estrng += '\n'
        ef.write(estrng)
        ef.close()
    def ewclose(self):
        """close log file """
        try:
            ef = open(self.logname, 'a')
            ef.write("<" + time.strftime('%c') + ">\n")
            ef.write("< close log >")
            ef.close()
        except IOError:
            print('error: log file not closed')