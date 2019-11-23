import re

from retrying import retry

from gspread.exceptions import APIError
from gspread_pandas import Spread


class SessionGenerator:
    '''
    Create session files for training block
    '''
    def __init__(self, client, block, session_template):
        self.client = client
        self.block = block
        self.session_template = session_template
        self._created_sessions = self._get_sessions()

    def generate_block(self, overwrite=False):
        '''
        Create files for all sessions in training block
        '''
        for week in range(1, self.block.duration+1):
            for session in range(1, self.block.sessions_per_week+1):
                self.generate_single(week, session, overwrite=overwrite)

    @retry(retry_on_exception=APIError, wait_fixed=1e4)  # Wait 10 seconds before hitting API again
    def generate_single(self, program_week, week_session, overwrite=False):
        '''
        Create file for session in training block
        '''
        block_number = self.block.block_number
        program_name = self.block.program_name

        sheet_name = f'{block_number}_{program_name}_{program_week}_{week_session}_yyyyMMdd'

        if self._session_exists(sheet_name) and not overwrite:
            print(f'Session ({program_week}, {week_session}) exists and overwrite=False, skipping')
            return

        session_spreadsheet = self.client.copy(self.session_template.id, sheet_name)
        program_slots = self.block.get_slots(program_week, week_session)

        for i, slot in enumerate(program_slots):
            j = i + 1
            if j == 1:
                slot_worksheet = session_spreadsheet.worksheet('Slot1')
            else:
                # Duplicate slot
                slot1_worksheet_id = session_spreadsheet.worksheet('Slot1').id
                slot_worksheet = session_spreadsheet.duplicate_sheet(
                    slot1_worksheet_id, insert_sheet_index=j, new_sheet_name=f'Slot{j}')

            # TODO: remove dependency on template sheet, create programmatically
            slot_worksheet.update_acell('B1', slot['Exercise'])
            slot_worksheet.update_acell('B2', slot['Prescription'])
            slot_worksheet.update_acell('B3', slot['Notes'])

        self.client.move_file(session_spreadsheet.id, self.block.path, create=True)
        self._created_sessions.append(sheet_name)
        print(f'Created session: {sheet_name}')

    def _session_exists(self, session_name):
        return bool(list(filter(lambda s: re.match(session_name.rstrip('_yyyyMMdd'), s), self._created_sessions)))

    def _get_sessions(self):
        files = self.client.list_spreadsheet_files()
        session_files = filter(lambda d: re.match(self.session_name_pattern, d['name']), files)
        session_file_names = map(lambda d: d['name'], session_files)
        return list(session_file_names)

    @property
    def session_name_pattern(self):
        return f'{self.block.block_number}_{self.block.program_name}'