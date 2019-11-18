
class SheetReader:
    def __init__(self, service_provider):
        self.service_provider = service_provider

    def read(self, sheet_id, sheet_range=None):
        result = self.service_provider.sheets_service.values().get(
            spreadsheetId=sheet_id, range=sheet_range).execute()
        values = result.get('values', [])
        return values
