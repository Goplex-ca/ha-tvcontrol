#!/usr/bin/env python
# Author: Martin MAsson
# Created: 2025-11-15
# Description: This connects to a Sharp Aquos TV and sends it a command
'''Usage:

    /sharpaquos.py -H tv_hostname -c command 
                        {-u username} {-p password} 
                        {-P port} {-n} {-v} 

    -H : hostname of the remote TV to connect to.
    -c : Command to send 
            poweroff : POWR   0 - Power Off
            poweron  : POWR   1 - Power On
            hdmi1    : INPS   2 - Input HDMI1
            hdmi2    : INPS   3 - Input HDMI2
            hdmi3    : INPS   3 - Input HDMI3
            vol:XXX  : VOLM XXX - Volume to XXX%
            mute     : MUTE   1 - Mute sound
            unmute   : MUTE   0 - Unmute sound  
            etc.
    -u : username to user for login.  Defaults to USER
    -p : password to user for login.  Defaults to PWD
    -P : Remote port to connect to (defaults to 10008)
    -n : No mandatory login prompt on the TV (ie. 4P-B86EJ2U, not needed for 4P-B55EJ2U)
    -v : verbose - prints more info

Example:
    This will power off the TV
        ./sharpaquos.py -H mytv.mydomain.com -u USER -p PWD -c poweroff
'''

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pexpect
import sys
import os
import getopt

def exit_with_usage():

    print(globals()['__doc__'])
    os._exit(1)

def main():

    # Parse the options, arguments, etc.
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'h?vH:c:P:n', ['help','h','?','host'])
    except Exception as e:
        print(str(e))
        exit_with_usage()
    options = dict(optlist)

    if [elem for elem in options if elem in ['-h','--h','-?','--?','--help']]:
        print('Help:')
        exit_with_usage()
    if '-v' in options:
        verbose = True
    else:
        verbose = False
    if '-H' in options:
        hostname = options['-H']
        if verbose: print ("Hostname:", hostname)
    else:
        # if host was not specified then quit
        print('Help:')
        exit_with_usage()
    if '-c' in options:
        if options['-c'] == 'poweroff':
            commandtext = 'Power Off'
            command = 'POWR   0'
        if options['-c'] == 'poweron':
            commandtext = 'Power On'
            command = 'POWR   1'
        if options['-c'] == 'hdmi1':
            commandtext = 'HDMI1'
            command = 'INPS   2'
        if options['-c'] == 'hdmi2':
            commandtext = 'HDMI2'
            command = 'INPS   3'
        if options['-c'] == 'hdmi3':
            commandtext = 'HDMI3'
            command = 'INPS   4'
        if options['-c'].startswith('vol'):
            value = options['-c'].split(':',1)[1]
            commandtext = 'VOLUME' + value
            if int(value) == 100:
                command = 'VOLM ' + value
            if int(value) < 100:
                command = 'VOLM  ' + value
            if int(value) < 10:
                command = 'VOLM   ' + value
        if options['-c'] == 'mute':
            commandtext = 'Mute'
            command = 'MUTE   1'
        if options['-c'] == 'unmute':
            commandtext = 'Unmute'
            command = 'MUTE   0'
        if verbose: print ("Command:", command)
    else:
        # if host was not specified then quit
        print('Help:')
        exit_with_usage()
    if '-u' in options:
        username = options['-u']
    else:
        username = 'USER'
    if '-p' in options:
        password = options['-p']
    else:
        password = 'PWD'
    if '-P' in options:
        port = options['-P']
    else:
        port = '10008'
    if verbose: print ("Port:", port)
    if '-n' in options:
        login = False
    else:
        login = True
    if verbose: print ("Login:", login)


    netcat = "nc " + hostname + " " + port
    child = pexpect.spawnu(netcat)
    
    if login:
        child.expect('(?i)Login:')
        child.sendline(username)
        child.expect('(?i)Password:')
        child.sendline(password)
        child.expect('OK')
    child.sendline(command + " ")
    child.expect('OK')
    child.sendline("BYE ")

if __name__ == '__main__':
    main()
