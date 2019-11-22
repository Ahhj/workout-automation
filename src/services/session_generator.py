from retrying import retry

from gspread.exceptions import APIError
from gspread_pandas import Spread


class SessionGenerator:
    '''
    Create session files for training block
    '''
    def __init__(self, client, training_block, session_template):
        self.client = client
        self.training_block = training_block
        self.session_template = session_template

    def generate_block(self):
        '''
        Create files for all sessions in training block
        '''
        for week in range(1, self.training_block.duration+1):
            for session in range(1, self.training_block.sessions_per_week+1):
                if not self._session_exists(week, session):
                    self.generate_single(week, session)

    @retry(retry_on_exception=APIError, wait_fixed=1e4)  # Wait 10 seconds before hitting API again
    def generate_single(self, program_week, week_session, overwrite=False):
        '''
        Create file for session in training block
        '''
        block_number = self.training_block.block_number
        program_name = self.training_block.program_name

        sheet_name = f'{block_number}_{program_name}_{program_week}_{week_session}_yyyyMMdd'
        session_spreadsheet = self.client.copy(self.session_template.id, sheet_name)

        program_slots = self.training_block.get_slots(program_week, week_session)

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

        self.client.move_file(session_spreadsheet.id, self.training_block.path, create=True)

    def _session_exists(self, program_week, week_session):
        return False  # TODO: implement.