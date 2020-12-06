from datetime import datetime as dt
from dirs import OS_SEP
from tools import logger, MyLocalException
import pandas as pd
import json


class Parser():

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = file_path.split(OS_SEP)[-1]

    def make_json(self):
        '''
        Expects abspath to .csv file
        Returns json data
        '''
        flt = self.parse_filename()
        df = self.make_df()
        try:
            passengers = Parser.make_dict(df)
            flt['prl'] = passengers
            json_data = json.dumps(flt)
            logger.info(f'{self.file_name}; Convert to json - OK')
            return json_data
        except (AttributeError, TypeError):
            logger.error(f'{self.file_name}; Convert to json - Error')
            raise MyLocalException

    def make_df(self):
        '''
        Expects abspath to .csv file
        Returns pandas DataFrame
        '''
        try:
            with open(self.file_path, 'r') as csv_file:
                df = pd.read_csv(
                    csv_file,
                    sep=';',
                    header=0)
                df = df.applymap(str)
            if not df.empty:
                return df
            logger.error(f'{self.file_name}; Empty table')
            raise MyLocalException

        except FileNotFoundError:
            logger.error(f"{self.file_path}; Can't open file")
            raise MyLocalException

        except pd.errors.EmptyDataError:
            logger.error(f'{self.file_name}; Incorrect .csv')
            raise MyLocalException

    @staticmethod
    def make_dict(df) -> dict:
        '''
        Expects pandas DataFrame
        Returns python dict
        '''
        json_data = df.to_json(orient="table", index=False)
        dict_data = json.loads(json_data)['data']
        return dict_data

    def parse_filename(self) -> dict:
        '''
        Expects abspath to .csv file
        Parse .csv filename and put result to dict
        Returns python dict
        '''
        try:
            fields = self.file_name.replace('.csv', '').split('_')
            date = fields[0]
            date = dt.strptime(date, '%Y%m%d')
            date = dt.strftime(date, '%Y-%m-%d')
            flt = int(fields[1])
            dep = fields[2]
            summary = {'flt': flt,
                       'date': date,
                       'dep': dep}
            return summary
        except (IndexError, ValueError, TypeError):
            logger.error(f'{self.file_name}; Incorrect filename')
            raise MyLocalException
