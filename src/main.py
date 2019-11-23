import pandas as pd
from gspread_pandas import Spread, Client


from .models import Program, Block
from . import configure
from .services import SessionGenerator

client = Client()

# TODO: clarify naming convention e.g. training/block/sessions
session_template_name = 'session_template'
program_name = 'powerbuilding1'
block_number = 2

# TODO: cleanup getting data into DataFrames
program = client.open(program_name)
program_summary = dict(program.worksheet('Summary').get_all_values())

# Parse program header
num_weeks = int(program_summary['NumberOfWeeks'])
sessions_per_week = int(program_summary['SessionsPerWeek'])
slots_per_session = int(program_summary['SlotsPerSession'])
gpp_slots_per_session = int(program_summary['GppSlotsPerSession'])

program_data = pd.DataFrame(program.worksheet('Program').get_all_records())
program_data.set_index(['Week', 'Session', 'Slot'], inplace=True)

program = Program(program_name, num_weeks, sessions_per_week, slots_per_session, data=program_data)
block = Block(block_number, program, root_path='Training/Blocks')

# Session template
session_template = client.open(session_template_name)

session_generator = SessionGenerator(client, block, session_template)
session_generator.generate_block()