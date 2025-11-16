#!/usr/bin/env python
# Author: Martin Masson
# Created: 2025-11-15
# Description:  This connects to a Samsung TV and sends it a command.  
#               It uses pexpect to open a netcat connection to the TV even 
#               if there are no interactive prompts to standardise the code 
#               structure with other TV scripts.

'''Usage:

    ./samsung.py -H tv_hostname -c command 
                        {-P port} {-v} 

    -H : hostname of the remote TV to connect to.
    -c : Command to send 
            poweroff : \\xAA\\x11\\xFE\\x01\\x00\\x10 - Power Off
            poweron  : \\xAA\\x11\\xFE\\x01\\x01\\x11 - Power On
            hdmi1    : \\xAA\\x14\\xFE\\x01\\x21\\x34 - Input HDMI1
            hdmi2    : \\xAA\\x14\\xFE\\x01\\x23\\x36 - Input HDMI2
            hdmi3    : \\xAA\\x14\\xFE\\x01\\x31\\x44 - Input HDMI3
            vol:0    : \\xAA\\x12\\x01\\x01\\x00\\x14 - Volume to 0 (MIN)
            vol:32   : \\xAA\\x12\\x01\\x01\\x32\\x46 - Volume to 32 (50%)
            vol:64   : \\xAA\\x12\\x01\\x01\\x64\\x78 - Volume to 64 (MAX)
            mute     : \\xAA\\x13\\xFE\\x01\\x01\\x1 - Mute sound
            unmute   : \\xAA\\x13\\xFE\\x01\\x00\\x12 - Unmute sound  
            etc.
    -P : Remote port to connect to (defaults to 1515)
    -v : verbose - prints more info

Example:
    This will power off the TV
        ./samsung.py -H mytv.mydomain.com -c poweroff
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

def decimal_to_hex(n):
    if n == 0:
        return "0"
    hex_digits = "0123456789abcdef"
    hex_val = ""
    while n > 0:
        remainder = n % 16
        hex_val = hex_digits[remainder] + hex_val
        n = n // 16
    return hex_val

def main():

    # Parse the options, arguments, etc.
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'h?vH:c:P:', ['help','h','?','host'])
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
            command = '\xAA\x11\xFE\x01\x00\x10'
        if options['-c'] == 'poweron':
            commandtext = 'Power On'
            command = '\xAA\x11\xFE\x01\x01\x11'
        if options['-c'] == 'hdmi1':
            commandtext = 'HDMI1'
            command = '\xAA\x14\xFE\x01\x21\x34'
        if options['-c'] == 'hdmi2':
            commandtext = 'HDMI2'
            command = '\xAA\x14\xFE\x01\x23\x36'
        if options['-c'] == 'hdmi3':
            commandtext = 'HDMI3'
            command = '\xAA\x14\xFE\x01\x31\x44'
        if options['-c'].startswith('vol:'):
            value = options['-c'].split(':',1)[1]
            if verbose: print ("Value:", value)
            command = '\xAA\x12\x01\x01' + chr(int(value, 16)) + chr(int(str(int(value)+14), 16)) # Damn Samsung and Python!
            commandtext = 'VOLUME ' + value + ' (' + ' '.join(hex(ord(c)) for c in command) + ')'
        if options['-c'] == 'mute':
            commandtext = 'Mute'
            command = '\xAA\x13\xFE\x01\x01\x01'
        if options['-c'] == 'unmute':
            commandtext = 'Unmute'
            command = '\xAA\x13\xFE\x01\x00\x12'
        if verbose: print ("Command Text:", commandtext)
        if verbose: print ("Command:", command)
    else:
        # if host was not specified then quit
        print('Help:')
        exit_with_usage()

    if '-P' in options:
        port = options['-P']
    else:
        port = '1515'
    if verbose: print ("Port:", port)

    netcat = "nc " + hostname + " " + port
    child = pexpect.spawnu(netcat)
    
    child.sendline(command)

if __name__ == '__main__':
    main()
