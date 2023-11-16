import pandas as pd


class CsvProcessor:

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def run(self):
        if 'ID' not in self.data.columns:
            self.data = self.data.assign(ID=[x for x in range(1, len(self.data) + 1)])
        self.data = self.data.assign(year=self.data['time'].dt.year)
        years = sorted(set(self.data.year))
        return {
            'years': years,
            'yearly_data': {year: self.data[self.data['year'] == year] for year in years}
        }
