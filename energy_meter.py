#!/usr/bin/python

# Google Spreadsheet DHT Sensor Data-logging Example

# Depends on the 'gspread' and 'oauth2client' package being installed.  If you
# have pip installed execute:
#   sudo pip install gspread oauth2client

# Also it's _very important_ on the Raspberry Pi to install the python-openssl
# package because the version of Python is a bit old and can fail with Google's
# new OAuth2 based authentication.  Run the following command to install the
# the package:
#   sudo apt-get update
#   sudo apt-get install python-openssl

# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
import time
import datetime
import yaml
from spreadsheet import Spreadsheet
from garo_gm3d import Garo

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

print 'Listening to energy meter on gpio pin {0}'.format(cfg['gpio_pin'])
print 'Loading oauth info from the file "{0}"'.format(cfg['gdocs_oauth_json'])
print 'Logging energy meter to spreadsheet  "{0}" every {1} seconds.'.format(cfg['gdocs_spreadsheet_name'], cfg['frequency_seconds'])
print 'Press Ctrl-C to quit.'

# Initialize the spreadsheet
spreadsheet = Spreadsheet(cfg['gdocs_oauth_json'], cfg['gdocs_spreadsheet_name'], cfg['gdocs_spreadsheet_worksheet'])

# Get the current energy meter standing from the spreadsheet on cell B1
current_watt_hours = spreadsheet.get_cell_value('B1')
current_watt_hours = int(current_watt_hours)
print 'Current energy meter standing (as read from the spreadsheet in column B1) is {}Wh'.format(current_watt_hours)

# Initialize the Garo GM3D
garo = Garo(cfg['gpio_pin'], current_watt_hours)
garo.listen()

while True:
    current_watt_hours = garo.get_watt_hours()
    spreadsheet.append_row((datetime.datetime.now(), current_watt_hours))
    spreadsheet.update_cell_value('B1', current_watt_hours)
    time.sleep(cfg['frequency_seconds'])