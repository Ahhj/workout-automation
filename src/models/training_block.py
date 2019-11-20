
class TrainingBlock:
    def __init__(self, block_number, program):
        self.block_number = block_number
        self.program = program

    @property
    def program_name(self):
        return self.program.name
        
    def get_slots(self, program_week, week_session):
        return self.program.get_slots(program_week, week_session)
