
class SheetCreator:
    def __init__(self, service_provider):
        self.service_provider = service_provider

    def create(self, sheet_name):
        body = {
            'properties': {
                'title': sheet_name
            }
        }
        spreadsheet = self.service_provider.sheets_service.create(
            body=body, 
            fields='spreadsheetId'
        ).execute()
        return spreadsheet.get('spreadsheetId')
