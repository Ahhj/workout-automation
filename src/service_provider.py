from googleapiclient.discovery import build


class ServiceProvider:
    def __init__(self, authenticator):
        self.authenticator = authenticator
        self._sheets_service = self._get_sheets_service()

    @property
    def sheets_service(self):
        return self._sheets_service

    def _get_sheets_service(self):
        creds = self.authenticator.credentials
        resource = build('sheets', 'v4', credentials=creds)
        # Call the Sheets API
        sheets_service = resource.spreadsheets()
        return sheets_service

