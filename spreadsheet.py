import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import json

worksheet = None

class Spreadsheet:
    oauth_key_file = ''
    spreadsheet_name = ''
    worksheet_name = ''
    worksheet = None

    def __init__(self, oauth_key_file, spreadsheet_name, worksheet_name):
        self.oauth_key_file = oauth_key_file
        self.spreadsheet_name =  spreadsheet_name
        self.worksheet_name = worksheet_name

    def login_open_sheet(self, oauth_key_file, spreadsheet, worksheet_name):
        print 'Logging into Google Docs'

        try:
            json_key = json.load(open(oauth_key_file))
            credentials = SignedJwtAssertionCredentials(json_key['client_email'],
                                                        json_key['private_key'],
                                                        ['https://spreadsheets.google.com/feeds'])
            gc = gspread.authorize(credentials)
            self.worksheet = gc.open(spreadsheet).worksheet(worksheet_name)
            return worksheet
        except Exception as ex:
            print 'Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!'
            print 'Google sheet login failed with error:', ex

    def check_login(self):
        # Login if necessary.
        if self.worksheet is None:
            self.login_open_sheet(self.oauth_key_file, self.spreadsheet_name, self.worksheet_name)

    def append_row(self, row):
        self.check_login()

        # Append the data in the spreadsheet, including a timestamp
        try:
            self.worksheet.append_row(row)
        except:
            # Error appending data, most likely because credentials are stale.
            # Null out the worksheet so a login is performed at the top of the loop.
            print 'Append error, logging in again'
            self.worksheet = None
            raise
        print 'Wrote a row to "{0}" spreadsheet'.format(self.spreadsheet_name)

    def get_cell_value(self, cell) :
        self.check_login()
        try:
            return self.worksheet.acell('B1').value
        except:
            # Error reading data, most likely because credentials are stale.
            # Null out the worksheet so a login is performed at the top of the loop.
            print 'Getting cell value error, logging in again'
            self.worksheet = None
            raise

    def update_cell_value(self, cell, value):
        self.check_login()
        try:
            self.worksheet.update_acell(cell, value)
        except:
            # Error updating data, most likely because credentials are stale.
            # Null out the worksheet so a login is performed at the top of the loop.
            print 'Updating cell value error, logging in again'
            self.worksheet = None
            raise