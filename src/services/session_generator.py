
class SessionGenerator:
    def __init__(self, client, training_block, session_template):
        self.client = client
        self.training_block = training_block
        self.session_template = session_template

    def generate(self, program_week, week_session):
        block_number = self.training_block.block_number
        program_name = self.training_block.program_name

        title = f'{block_number}/{program_name}_{program_week}_{week_session}_yyyyMMdd'
        session_spreadsheet = self.client.copy(
            self.session_template.id, title, copy_permissions=True)

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
