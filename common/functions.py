import yaml
import os
import shutil
import logging as logger
import datetime

from os.path import dirname, abspath, join
from csv_to_yaml_convertor.csv_to_yaml_convertor import CsvToYamlConvertor

current_dir = dirname(dirname(abspath(__file__)))


def get_config(appliance, param, yaml_file_path):
    """This function gives the yaml value corresponding to the parameter
    sample Yaml file
        xstream_details:
            xtm_host: 10.100.26.90
    :param appliance: The header name as mentioned in the yaml file (ex:xstream_details)
    :param param: The parameter name who's value is to be determined (ex: xtm_host)
    :param yaml_file_path: Path of yaml file, Default will the config.yaml file
    :return: value corresponding to the parameter in yaml file
    :except: Exception while opening or loading the file
    """
    try:
        with open(yaml_file_path, 'r') as f:
            doc = yaml.load(f)
        if param is None:
            param_value = doc[appliance]
        else:
            param_value = doc[appliance][param]
        if param_value == "":
            message = 'Value is not updated for the parameter:{} in the yaml config file'\
                .format(param)
            raise Exception(message)
        return param_value
    except Exception as ex:
        message = "Exception: An exception occured: {}".format(ex)
        raise Exception(message)


def print_results(result_dict):
    """
    Print the results in required format
    :param result_dict: results dict
    :return: output in user readable  format
    """
    print('\nResult Summary:')
    print("----------------------------------------------")
    print("Component" + 20 * " " + "Status")
    print("----------------------------------------------")
    for result in result_dict:
        gap = 29 - len(result)
        space = ' ' * gap
        print(result, space, result_dict[result])
        print("\n")
    count = 0
    passed = [i for i in result_dict.values() if i == "PASS"]
    print("----------------------------------------------")
    print("Total Testcases: {}  PASSED:  {}  FAILED: {}".format(len(result_dict), len(passed),
                                                                len(result_dict) - len(passed)))
    print('\n')


def list_of_yaml_files(dir_path):
    """
    List of yaml file in a dir
    :param dir_path: location of dir where yaml files are located
    :return:
    """
    return [item for item in os.listdir(dir_path) if '.yaml' in item and 'base_config.yaml' not in item]


def copy_file(source_filename, source_dir = 'deployment', des_filename = 'config.yaml'):
    """
    Copy the file in a destination dir
    :param source_filename: file name
    :param source_dir: source dir
    :param des_filename: Destination dir
    :return:
    """
    source_dir_path = join(current_dir, 'config', source_dir, source_filename)
    destination_dir_path = join(current_dir, 'config', des_filename)
    try:
        shutil.copy(source_dir_path, destination_dir_path)
    except:
        raise Exception("Unable to copy the file - {} to the destination folder {}".format(source_filename,
                                                                                           destination_dir_path))


def convert_csv_to_yaml(service, csv_files_path, base_yaml_name='config.yaml', file_name=None):
    """
    Convert CSV to Yaml format
    :param service: deployment or tas or middleware or worker
    :param csv_files_path: Location of CSV stored
    :param base_yaml_name: Base yaml file name
    :param file_name: save the yaml file with the specific name, default will be None
    (If the file_name is none, name will be picked from the csv's first element of every row)
    :return:
    """
    if service == 'deployment':
        base_yaml_path = join(current_dir, 'config', base_yaml_name)

    else:
        base_yaml_path = join(current_dir, 'config', service, base_yaml_name)

    path_to_save_yaml = join(current_dir, 'config', service)
    csv_path = join(csv_files_path, '{}_configuration_data.csv'.format(service))

    # Create object to convert csv to yaml
    yaml_obj = CsvToYamlConvertor(service=service,
                                  base_yaml_file_path=base_yaml_path,
                                  csv_file_path=csv_path,
                                  dir_to_store_yaml=path_to_save_yaml,
                                  filename=file_name)

    # Convert CSV to YAML and save the yaml files
    yaml_obj.convert_csv_to_yaml()

    yaml_file_list = list_of_yaml_files(path_to_save_yaml)

    if not len(yaml_file_list):
        raise Exception('Unable to generate {} yaml files'.format(service))
    return yaml_file_list


def save_execution_log(file_name):
    """
    Save the execution log in a file
    :param file_name: Name of the file, where log need to be saved
    :return:
    """
    logfile = datetime.datetime.now().strftime('{}_%H_%M_%d_%m_%Y.log'.format(file_name))
    logpath = '{}/{}'.format(current_dir, logfile)
    logger.basicConfig(level=logger.INFO,
                       format='%(asctime)s %(levelname)-8s %(message)s',
                       datefmt='%m-%d %H:%M',
                       filename=logpath,
                       filemode='w')

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logger.StreamHandler()
    console.setLevel(logger.INFO)
    formatter = logger.Formatter('%(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logger.getLogger('').addHandler(console)

def remove_yaml_files():
    """
    Remove Yaml files from the list of directories
    """
    dir_list = ['deployment', 'middleware', 'tas', 'worker']
    for directory in dir_list:
        dir_path  = os.path.join(current_dir, 'config', directory)
        yaml_files_list = list_of_yaml_files(dir_path)
        for item in yaml_files_list:
            filepath = os.path.join(dir_path, item)
            os.remove(filepath)
