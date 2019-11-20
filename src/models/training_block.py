
class TrainingBlock:
    def __init__(self, block_number, program, root_path):
        self.block_number = block_number
        self.program = program
        self.root_path = root_path

    @property
    def program_name(self):
        return self.program.name

    @property
    def path(self):
        return f'{self.root_path}/{self.block_number}'
        
    def get_slots(self, program_week, week_session):
        return self.program.get_slots(program_week, week_session)

