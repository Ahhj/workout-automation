from googleapiclient.discovery import build


class SheetReader:
    def __init__(self, authenticator):
        self.authenticator = authenticator

    def read(self, sheet_id, sheet_range=None):
        creds = self.authenticator.get_credentials()
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        return values
