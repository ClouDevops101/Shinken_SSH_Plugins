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
import os
import sys
import optparse
import re
# Ok try to load our directory to load the plugin utils.
my_dir = os.path.dirname(__file__)
sys.path.insert(0, my_dir)

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


def get_systemd_service_status(client):
     
    # patern : 
    """20 package(s) needed for security, out of 510 available#
    No packages needed for security; 279 packages available#
    """
    #raw = r"""/usr/sbin/ntpq -p"""
    raw = "%s" % SYSTEMD_SRV
    stdin, stdout, stderr = client.exec_command("export LC_LANG=C && unset LANG && export PATH=$PATH:/usr/bin:/usr/sbin && %s" % raw)
    errs = ''.join(l for l in stderr)
    output = stdout.channel.recv_exit_status()
    print '------'
    print output
    print '------'
    if errs:
        print "Error: %s" % errs.strip()
        client.close()
        sys.exit(2)

#    for line in stdout:
#        line = line.strip()
#        # We want the line of the reference only
#        if not line:
#            continue
#        #print line
#        update_needed = []
#        for update_needed in re.findall('(\d+) package(s) needed for security, out of (\d+) available', line):
#          print "output1----" + update_needed
#        noupdate_needed = []
#        for noupdate_needed in re.findall('No packages needed for security; (\d+) packages available', line):
#          print "output2-----" + noupdate_needed
#    # Before return, close the client
#    if update_needed:
#      output = update_needed
#    else:
#      output = noupdate_needed 
#    print output
        
    client.close()
        
    return output

parser = optparse.OptionParser(
    "%prog [options]", version="%prog " + VERSION)
parser.add_option('-H', '--hostname',
                  dest="hostname", help='Hostname to connect to')
parser.add_option('-p', '--port',
                  dest="port", type="int", default=22,
                  help='SSH port to connect to. Default : 22')
parser.add_option('-i', '--ssh-key',
                  dest="ssh_key_file",
                  help='SSH key file to use. By default will take ~/.ssh/id_rsa.')
parser.add_option('-u', '--user',
                  dest="user", help='remote use to use. By default shinken.')
parser.add_option('-P', '--passphrase',
                  dest="passphrase", help='SSH key passphrase. By default will use void')
parser.add_option('-S', '--service',
                  dest="service", help='Service to check from systemd')
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

    port = opts.port
    hostname = opts.hostname or ''
    service = opts.service or ''

   # ntpq = opts.ntpq

    ssh_key_file = opts.ssh_key_file or os.path.expanduser('~/.ssh/id_rsa')
    user = opts.user or 'shinken'
    passphrase = opts.passphrase or ''

    #chrony = opts.chrony

#    if not chrony:
#        # Try to get numeic warning/critical values
#        s_warning  = opts.warning or DEFAULT_WARNING
#        s_critical = opts.critical or DEFAULT_CRITICAL
#        warning, critical = schecks.get_warn_crit(s_warning, s_critical)
#    else:
#    if opts.warning:
#      warning_sec_update = int(opts.warning.split(',')[0])
#      warning_other_update = int(opts.warning.split(',')[1])
#    else:
#      warning_sec_update = int(DEFAULT_SECUPDATE_WARNING)
#      warning_other_update = int(DEFAULT_OTHERUPDATE_WARNING)
#    if opts.critical:
#      critical_sec_update = int(opts.critical.split(',')[0])
#      critical_other_update = int(opts.critical.split(',')[1])
#    else:
#      critical_sec_update = int(DEFAULT_SECUPDATE_CRITICAL)
#      critical_other_update = int(DEFAULT_OTHERUPDATE_CRITICAL)
#        if opts.critical:
#            critical_delay = float(opts.critical.split(',')[0])
#            critical_offset = float(opts.critical.split(',')[1])
#        else:
#            critical_delay = float(DEFAULT_DELAY_CRITICAL)
#            critical_offset = float(DEFAULT_OFFSET_CRITICAL)

    
        
    # Ok now connect, and try to get values for memory
    client = schecks.connect(hostname, port, ssh_key_file, passphrase, user)
    #if not chrony:
    SYSTEMD_SRV = SYSTEMD_SRV + service.encode('string-escape')
    raw = "%s" % SYSTEMD_SRV
    print raw
    output = get_systemd_service_status(client)
    re_security_summary = re.compile(r'Needed (\d+) of (\d+) packages, for security')
    re_summary_rhel6 = re.compile(r'(\d+) package\(s\) needed for security, out of (\d+) available')
    re_no_sec_updates = re.compile(r'No packages needed,? for security[;,] (\d+) (?:packages )?available')
    summary_line_found = False
    for line in output:
        _ = re_summary_rhel6.match(line)
        if _:
            summary_line_found = True
            number_security_updates = _.group(1)
            number_total_updates = _.group(2)
            break
        _ = re_no_sec_updates.match(line)
        if _:
            summary_line_found = True
            number_security_updates = 0
            number_total_updates = _.group(1)
            break
        _ = re_security_summary.match(line)
        if _:
            summary_line_found = True
            number_security_updates = _.group(1)
            number_total_updates = _.group(2)
            break

    if not summary_line_found:
        end(WARNING, "Cannot find summary line in yum output. " + support_msg)

    try:
        number_security_updates = int(number_security_updates)
        number_total_updates = int(number_total_updates)
    except ValueError:
        end(WARNING, "Error parsing package information, yum output " \
                   + "may have changed. " + support_msg)

    number_other_updates = number_total_updates - number_security_updates

    from_excluded_regex = re.compile(' from .+ excluded ')
    if len([_ for _ in output if not from_excluded_regex.search(_)]) > number_total_updates + 25:
        end(WARNING, "Yum output signature is larger than current known "  \
                   + "format. " + support_msg) 
    #print "-----------" + str(number_security_updates)
    #print "+++++++++++" + str(number_other_updates)
#        if not output:
#            print "Warning : no response for the server"
#            sys.exit(1)
#
    perfdata = "sec_package=%s;%s;%s;;" % (number_security_updates, warning_sec_update, critical_sec_update)
    perfdata = perfdata + " other_package=%s;%s;%s;;" % (number_other_updates, warning_other_update, critical_other_update)
    message = str(number_security_updates) + " Security Updates, " +  str(number_other_updates)  + " Other Updates"

    if number_security_updates >= critical_sec_update:
      print "Critical: number of security packages is high, %s | %s" %(message, perfdata)
      sys.exit(2)

    if number_other_updates >= critical_other_update:
      print "Critical: number of packages to be updated is high, %s | %s" %(message, perfdata)
      sys.exit(2)

    if number_security_updates >= warning_sec_update:
      print "Warning: number of security packages worth attention, %s | %s" %(message, perfdata)
      sys.exit(1)

    if number_other_updates >= warning_other_update:
      print "Warning: number of packages to be updated worth attention, %s | %s" %(message, perfdata)
      sys.exit(1)

    if number_security_updates < critical_sec_update and number_other_updates < warning_other_update:
      print "OK: %s | %s" %(message, perfdata)
      sys.exit(0)
    else:
      print "Unknown: %s | %s" %(message, perfdata)
      sys.exit(3)

#        if ref_delay > warning:
#            print "Warning: ntp delay is %.2fs | %s" %(ref_delay, perfdata)
#            sys.exit(2)
#        print "OK: ntp delay is %.2fs | %s" %(ref_delay, perfdata)
#        sys.exit(0)
#
#    else:
#        delay, offset = get_chrony_sync(client)
#
#        if not delay or not offset:
#            print "Warning : cannot get delay or offset value"
#            sys.exit(1)
#
#        perfdata =  "delay=%.2fs;%.2fs;%.2fs;;" % (delay, warning_delay, critical_delay)
#        perfdata += "offset=%.4fs;%.4fs;%.4fs;;" % (offset, warning_offset, critical_offset)
#
#        if delay > critical_delay:
#            print "Critical: ntp/chrony delay is %.2fs | %s" % (delay, perfdata)
#            sys.exit(2)
#
#        if offset > critical_offset:
#            print "Critical: ntp/chrony offset is %.4fs | %s" % (offset, perfdata)
#            sys.exit(2)
#
#        if delay > warning_delay:
#            print "Warning: ntp/chrony delay is %.2fs | %s" % (delay, perfdata)
#            sys.exit(2)
#
#        if offset > warning_offset:
#            print "Warning: ntp/chrony offset is %.4fs | %s" % (offset, perfdata)
#            sys.exit(2)
#
#        print "OK: ntp delay is %.2fs offset is %.4fs | %s" %(delay, offset, perfdata)
#        sys.exit(0)
#        
