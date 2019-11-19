import gspread
from oauth2client.service_account import ServiceAccountCredentials

import pandas as pd


scope = [
    'https://spreadsheets.google.com/feeds', 
    'https://www.googleapis.com/auth/drive'
]

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

session_template_name = 'session_template'
program_name = 'powerbuilding1'
block = 1

client = gspread.authorize(credentials)

# Program
program = client.open(program_name)
program_summary = dict(program.worksheet('Summary').get_all_values())
program_df = pd.DataFrame(program.worksheet('Program').get_all_records())
program_df.set_index(['Week', 'Session', 'Slot'], inplace=True)

# Parse program header
num_weeks = int(program_summary['NumberOfWeeks'])
sessions_per_week = int(program_summary['SessionsPerWeek'])
slots_per_session = int(program_summary['SlotsPerSession'])
gpp_slots_per_session = int(program_summary['GppSlotsPerSession'])

# Session template
template = client.open(session_template_name)

def generate_session(week, session):
    title = f'{block}/{program_name}_{week}_{session}_yyyyMMdd'
    session_spreadsheet = client.copy(
        template.id, title, copy_permissions=True)

    for slot in range(1, slots_per_session+1):
        if slot == 1:
            slot_worksheet = session_spreadsheet.worksheet('Slot1')
        else:
            # Duplicate slot
            slot1_worksheet_id = session_spreadsheet.worksheet('Slot1').id
            slot_worksheet = session_spreadsheet.duplicate_sheet(
                slot1_worksheet_id, insert_sheet_index=slot, new_sheet_name=f'Slot{slot}')

        program_slot = program_df.loc[week, session, slot].to_dict()
        slot_worksheet.update_acell('B1', program_slot['Exercise'])
        slot_worksheet.update_acell('B2', program_slot['Prescription'])
        slot_worksheet.update_acell('B3', program_slot['Notes'])

generate_session(7, 3)

# Generate program session
# for week in range(1, num_weeks+1):
#     for session in range(1, sessions_per_week+1):
#         generate_session(week, session)
