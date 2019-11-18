
class SheetWriter:
    def __init__(self, service_provider):
        self.service_provider = service_provider

    def write(self, values, sheet_id, sheet_range=None):
        body = {
            'values': values
        }
        result = self.service_provider.sheets_service.values().update(
            spreadsheetId=sheet_id,
            range='A:Z',
            valueInputOption='RAW', 
            body=body
        ).execute()

        result = self.service_provider.sheets_service.values()
        return result
