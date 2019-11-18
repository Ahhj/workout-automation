
from .authenticator import Authenticator
from .sheet_reader import SheetReader

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'


def main():
    """
    Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    auth = Authenticator('credentials.json', 'token.pickle')
    reader = SheetReader(auth)
    values = reader.read(SAMPLE_SPREADSHEET_ID, sheet_range=SAMPLE_RANGE_NAME)

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))

if __name__ == '__main__':
    main()
