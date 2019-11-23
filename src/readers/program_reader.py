from gspread_pandas import Spread
from ..models import Program


class ProgramReader:
    def __init__(self, client):
        self.client = client

    def read(self, name):
        program_spread = Spread(name, client=self.client)
        meta = self._read_meta(program_spread)
        content = self._read_content(program_spread)
        return Program(name, *meta, content)

    def _read_meta(self, spread):
        df = spread.sheet_to_df(sheet='Meta')
        duration = int(df.loc['DurationWeeks'][0])
        sessions_per_week = int(df.loc['SessionsPerWeek'][0])
        slots_per_session = int(df.loc['SlotsPerSession'][0])
        # gpp_per_session = df.loc['GppSlotsPerSession']
        return duration, sessions_per_week, slots_per_session

    def _read_content(self, spread):
        content = spread.sheet_to_df(sheet='Content', index=None)
        content = content.astype({'Week': int, 'Session': int, 'Slot': int})
        content.set_index(['Week', 'Session', 'Slot'], inplace=True)
        return content
