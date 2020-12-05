import dirs
import logging
import os
import sys
import shutil

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

class MyLocalException(Exception):
    pass


def check_input_dir():
    try:
        with os.scandir(dirs.INPUT_DIR) as content:  
            files = [item.name for item in content
                        if item.is_file()]
            for file in files:
                logger.info(f'{file}; New file  detected in input directory')
        return files
    except FileNotFoundError:
        logger.info(f"Can't open input directory")
        raise MyLocalException


def move_input_file(file: str, new_dir: str):
    try:
        src = f'{dirs.INPUT_DIR}{file}'
        dst = f'{new_dir}{file}'
        shutil.move(src, dst)
        logger.info(f'{file}; File  moved to {new_dir}')
    except FileNotFoundError:
        logger.info(f"{file}; Can't move input file")
        raise MyLocalException


def init_dirs(*args):
    for directory in args:
        try:
            os.mkdir(directory)
            logger.info(f'Create {directory}')
        except FileExistsError:
            pass


def save_json(json_data, filename):
    try:
        json_filename = filename.split('/')[-1].replace('.csv', '.json')
        with open(dirs.OUTPUT_DIR + filename, 'w') as file:
            file.write(json_data)
    except FileNotFoundError:
        logger.info(f"{filename}; Can't save json file")
        raise MyLocalException
