
class TrainingBlock:
    '''
    Block of training, either in progress or completed
    '''
    def __init__(self, block_number, program, root_path):
        self.block_number = block_number
        self.program = program
        self.root_path = root_path

    @property
    def program_name(self):
        return self.program.name

    @property
    def sessions_per_week(self):
        return self.program.sessions_per_week

    @property
    def duration(self):
        return self.program.duration

    @property
    def path(self):
        return f'{self.root_path}/{self.block_number}'
        
    def get_slots(self, program_week, week_session):
        return self.program.get_slots(program_week, week_session)


