from datetime import datetime as dt
from dirs import OS_SEP
from tools import logger, MyLocalException
import csv
import json


class Parser():

    expected_header = ['num', 'surname', 'firstname', 'bdate']

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = file_path.split(OS_SEP)[-1]

    def make_json(self):
        '''
        Expects abspath to .csv file
        Returns json data
        '''
        flt = self.parse_filename()
        passengers = self.csv_to_dict()
        flt['prl'] = passengers
        try:
            json_data = json.dumps(flt)
            logger.info(f'{self.file_name}; Convert to json - OK')
            return json_data
        except (AttributeError, TypeError):
            logger.error(f'{self.file_name}; Convert to json - Error')
            raise MyLocalException

    def csv_to_dict(self) -> list:
        '''
        Expects abspath to .csv file
        Returns list of dicts with passengers
        '''
        with open(self.file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')
            header = reader.fieldnames
            list_of_dicts = list(reader)

            if not Parser.expected_header == header:
                logger.error(f'{self.file_name}; Incorrect .csv')
                raise MyLocalException

            elif not list_of_dicts:
                logger.error(f'{self.file_name}; Empty table')
                raise MyLocalException

            for item in list_of_dicts:
                if None in item.values():
                    logger.error(f'{self.file_name}; Invalid data in .csv')
                    raise MyLocalException
            
        return list_of_dicts

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
