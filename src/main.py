import pandas as pd
from gspread_pandas import Spread, Client

from . import configure
from .models import Block
from .readers import ProgramReader
from .services import SessionGenerator

client = Client()
program_reader = ProgramReader(client)

# TODO: clarify naming convention e.g. training/block/sessions
session_template_name = 'session_template'
program_name = 'powerbuilding1'
block_number = 2

program = program_reader.read(program_name)
block = Block(block_number, program, root_path='Training/Blocks')

# Session template
session_template = client.open(session_template_name)

session_generator = SessionGenerator(client, block, session_template)
session_generator.generate_block()
