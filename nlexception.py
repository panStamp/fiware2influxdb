#########################################################################
# Copyright (c) 2018 panStamp <contact@panstamp.com>
# 
# This file is part of the panStamp project.
# 
# panStamp  is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
# 
# panStamp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with panStamp; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 
# USA
#
# Author: Daniel Berenguer
# Date: Nov 22 2018
#########################################################################

from config.config import NlConfig
import time, datetime, os

class NlException(Exception):
    """
    Main exception class for pySwap
    """

    ## Path to the log file
    LOGFILE = "log/exceptions.log"

    ## Exception reasons
    WRONG_PACKET_FORMAT = "Incorrect packet format"

    def show(self):
        """
        Print short exception description
        """
        print (self.description)
        

    def log(self):
        """
        Write exception in log file
        """
        f = open(NlException.LOGFILE, 'a')
        f.write(datetime.datetime.fromtimestamp(self.timestamp).strftime("%d-%m-%Y %H:%M:%S") + ": " + self.description + "\n")
        f.close()
        

    @staticmethod
    def clear():
        """
        Clear error file
        """
        # Remove existing error file
        if os.path.exists(NlException.LOGFILE):
            os.remove(NlException.LOGFILE)


    def __init__(self, value):
        """
        Class constructor
        
        @param value: Description about the error
        """
        self.timestamp = time.time()
        # Exception description
        self.description = "NlException occurred: " + value

        # Log exception
        if NlConfig.LOG_ENABLE:
            self.log()
  
