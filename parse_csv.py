from datetime import datetime as dt
from tools import logger, MyLocalException
import pandas as pd
import json


def make_json(file_path: str):
    flt = parse_filename(file_path)
    df = make_df(file_path)
    filename = file_path.split('/')[-1]
    try:
        passengers = make_dict(df)
        flt['prl'] = passengers
        json_data = json.dumps(flt)
        logger.info(f'{filename}; Convert to json - OK')
        return json_data
    except (AttributeError, TypeError):
        logger.error(f'{filename}; Convert to json - Error')
        raise MyLocalException
    

def make_df(file_path: str):
    filename = file_path.split('/')[-1]
    try:
        df = pd.read_csv(
            open(file_path, 'r'),
            sep=';',
            header=0)
        df = df.applymap(str)

        if not df.empty:
            return df
        logger.error(f"{filename}; Empty table")
        raise MyLocalException

    except FileNotFoundError:
        logger.error(f"{file_path}; Can't open file ")
        raise MyLocalException

    except pd.errors.EmptyDataError:
        logger.error(f"{filename}; Incorrect .csv ")
        raise MyLocalException


def make_dict(df):
    json_data = df.to_json(orient="table", index=False)
    dict_data = json.loads(json_data)['data']
    return dict_data


def parse_filename(file_path: str) -> dict:
    try:
        filename = file_path.split('/')[-1]
        fields = filename.replace('.csv', '').split('_')
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
        logger.error(f'{filename}; Incorrect filename ')
        raise MyLocalException
