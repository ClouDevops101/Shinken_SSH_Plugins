#!/usr/bin/env python

# Copyright (C) 2013:
#     Gabes Jean, naparuba@gmail.com
#     Pasche Sebastien, sebastien.pasche@leshop.ch
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#


'''
 This script is a check for lookup at memory consumption over ssh without
 having an agent on the other side
'''
import optparse
import re
import json
import requests
import sys
# Ok try to load our directory to load the plugin utils.

try:
    import schecks
except ImportError:
    print "ERROR : this plugin needs the local schecks.py lib. Please install it"
    sys.exit(2)


VERSION = "0.1"
DEFAULT_WARNING = '10'
DEFAULT_CRITICAL = '60'

SYSTEMD_SRV=r"""systemctl is-active """


DEFAULT_SECUPDATE_WARNING = '1'
DEFAULT_OTHERUPDATE_WARNING = '100' # 100 ms
DEFAULT_SECUPDATE_CRITICAL = '3'
DEFAULT_OTHERUPDATE_CRITICAL = '300' # 100 ms



parser = optparse.OptionParser(
    "%prog [options]", version="%prog " + VERSION)
parser.add_option('-C', '--container',
                  dest="container", help='Service to check from systemd')

parser.add_option('-M', '--master',
                  dest="master", help='Service to check from systemd')
#parser.add_option('-w', '--warning',
#                  dest="warning",
#                  help='Warning delay for ntp, like 10. couple delay,offset value for chrony '
#                  '0.100,0.0025')
#parser.add_option('-c', '--critical',
#                  dest="critical",
#                  help='Warning delay for ntp, like 10. couple delay,offset value for chrony '
#                  '0.150,0.005')
#parser.add_option('-C', '--chrony',  action='store_true',
 #                 dest="chrony", help='check Chrony instead of ntpd')
#parser.add_option('-n', '--ntpq',
  #                dest="ntpq", help="remote ntpq bianry path")


if __name__ == '__main__':
    # Ok first job : parse args
    opts, args = parser.parse_args()
    if args:
        parser.error("Does not accept any argument.")

    container = opts.container or ''
    master = opts.master or ''
    

    url = "http://" + master +  "/marathon/v2/apps/" + container 
    try:
      myResponse = requests.get(url)
    except:
      print "Unknown: No response" 
      sys.exit(3)
    if(myResponse.ok):
    #chrony = opts.chrony
      Data = json.loads(myResponse.content)
      try:
        Task_Status = Data["app"]["tasks"][0]["state"]
      except:
        print "Critical: %s is in failed state" %(container)
        sys.exit(2)

      if Task_Status == "TASK_RUNNING" :
        print "OK: container %s is in running state" %(container)
        sys.exit(0)
  
      if Task_Status == "TASK_FAILED" :
        print "Critical: %s is in failed state" %(container)
        sys.exit(2)
  
      if Task_Status == "null" :
        print "Critical: %s is in failed state" %(container)
        sys.exit(2)
      else:
        print "Unknown %s:" %(container)
        sys.exit(3)
  
