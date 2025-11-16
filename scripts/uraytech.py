#!/usr/bin/env python
# Author: Martin Masson
# Created: 2025-11-15
# Description: This connects to a URayTech decoder and sends it a command

# Can use "curl http://admin:admin@<host ip>/getpro.cgi" to get status info

'''Usage:

    ./uraytech.py -H decoder_hostname -c command 
                        {-u username} {-p password} 
                        {-P port} {-v} 

    -H : hostname of the URayTech decoder to connect to.
    -c : Command to send 
            channelup   :   Channel Up
            channeldown :   Channel Down
            channel:XXX :   Go to channel ID XXX (eg. channel:2)
            reboot      :   Reboot the decoder
            etc.
    -u : username to user for login.  Defaults to "admin"
    -p : password to user for login.  Defaults to "admin"
    -P : Remote port to connect to (defaults to 80)
        -v : verbose - prints more info

Example:
    This will change go channel 2 off the TV
        ./uraytech.py -H decoder.mydomain.com -u USER -p PWD -c channel:2
'''

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pexpect
import sys
import os
import getopt
import requests

def exit_with_usage():

    print(globals()['__doc__'])
    os._exit(1)

def main():

    # Parse the options, arguments, etc.
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'h?vH:c:P:u:p:', ['help','h','?','host'])
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

    path = '/setpro.cgi?'
    if '-c' in options:
        if options['-c'] == 'channelup':
            commandtext = 'Channel Up'
            command = 'channelup'
        if options['-c'] == 'channeldown':
            commandtext = 'Channel Down'
            command = 'channeldown'
        if options['-c'].startswith('channel:'):
            value = options['-c'].split(':',1)[1]
            commandtext = 'Channel ' + value
            command = 'playindex=' + str(int(value)-1)
        if options['-c'] == 'reboot':
            commandtext = 'Reboot'
            command = 'reboot'
            path = '/set.cgi?'
        if verbose: print ("Command:", command)
    else:
        # if command was not specified then quit
        print('Help:')
        exit_with_usage()
    if '-u' in options:
        username = options['-u']
    else:
        username = 'admin'
    if '-p' in options:
        password = options['-p']
    else:
        password = 'admin'
    if '-P' in options:
        port = options['-P']
    else:
        port = '80'
    if verbose: print ("Port:", port)


    url = 'http://' + hostname + ':' + port + path + command
    if verbose: print ("URL:", url)

    response = requests.get(url, auth=(username, password))
    if verbose: print("Response:", response.text)


if __name__ == '__main__':
    main()
