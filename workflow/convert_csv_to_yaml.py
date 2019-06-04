import logging as logger
import sys

from os.path import dirname, abspath, join
from argparse import ArgumentParser
from time import sleep

current_dir = dirname(dirname(abspath(__file__)))

sys.path.append(current_dir)

from common.functions import convert_csv_to_yaml, save_execution_log, remove_yaml_files


def main(csv_files_path):

    logger.info("###############START#########################")

    convert_csv_to_yaml(service='deployment', csv_files_path=csv_files_path)
    logger.info('Converted deployment CSV input to yaml format')

    logger.info("###############END###########################\n")
    sleep(2)


if __name__ == '__main__':
    save_execution_log('csv_to_yaml_console')
    parser = ArgumentParser(description='Arguments for convert csv to yaml')
    parser.add_argument('-csv', '--csv_path',
                        default=join(current_dir, 'config', 'csv_files'),
                        action='store',
                        help='Deployment CSV file location')
    args = parser.parse_args()
    main(args.csv_path)
    # remove_yaml_files()
