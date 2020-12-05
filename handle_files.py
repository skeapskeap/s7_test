
from db import save_to_db, init_db
from parse_csv import make_json
from time import sleep
import argparse
import dirs
import logging
import os
import shutil
import sys
import tools

arg_parser = argparse.ArgumentParser(
            description='python handle_files.py -i <POLL_INTERVAL_SECONDS>')
arg_parser.add_argument('-i', '--interval', nargs='?', default=10, type=int)
args = arg_parser.parse_args(sys.argv[1:])
POLL_INTERVAL = args.interval


def main_pipeline():
    '''
    Base logic here
    '''
    new_files = tools.check_input_dir()
    for file in new_files:
        try:
            json_data = make_json(dirs.INPUT_DIR + file)
            tools.save_json(json_data, file)
            save_to_db(json_data)
            tools.move_input_file(file, dirs.OK_DIR)
        except tools.MyLocalException:
            tools.move_input_file(file, dirs.ERR_DIR)

def init():
    '''
    Init db and create default directories
    '''
    init_db()
    tools.init_dirs(
        dirs.INPUT_DIR,
        dirs.OK_DIR,
        dirs.ERR_DIR,
        dirs.OUTPUT_DIR)


if __name__ == '__main__':
    try:
        init()
        while True:
            main_pipeline()
            sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except tools.MyLocalException:
        tools.logger.error('Error while initialising')
