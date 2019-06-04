csv-yaml

A python project to convert CSV file into a series of YAML files

The specialty of this project is, it will take care of list, dictionary objects as well while converting into yaml format.

Example:

Sample Input in csv format:

networker_server_details.DATADOMAIN_SERVERS.0.hostname	networker_server_details.DATADOMAIN_SERVERS.0.ip networker_server_details.DATADOMAIN_SERVERS.1.hostname	networker_server_details.DATADOMAIN_SERVERS.1.ip
dd.hostname	1.1.1.4 dd2.hostname 1.1.1.5

Sample Output in yaml format:

networker_server_details:
    DATADOMAIN_SERVERS:
    - hostname: "dd.hostname"
      ip: "1.1.1.4"
    - hostname: "dd2.hostname"
      ip: "1.1.1.5"

#Prerequisites:

    - Python 3.5 or above need to be installed

    - Set the PATH environmental variables:

        Example:  Path: C:\python3.5\;C:\python3.5\Lib;C:\python3.5\Lib\site-packages
    
    Note: If permissions are not there to set the environmental variables use the absolute path of python to execute the script:
    
    Example: C:\python3.5\python sample.py

### Python Virtual Environment

1. Create Python virtual environment

        $ virtualenv <name-of-folder>

2. Activate virtual environment

        $ source <path-to-folder>/bin/activate

3. Deactivate virtual environment

        $ deactivate

### Install requirements

* Install python project dependencies for dev environment


        $ pip3 install -r requirements.txt


## Script execution

#Assuming using this in your working directory

   Step1: Go to the workflow directory and execute convert_csv_to_yaml.py

   Step2:

   Option1:
        python convert_csv_to_yaml.py -csv some/file/csvFile.csv

        # Usage:

        -csv: CSV file location

   Option2:

        If we place the csv under the location: (<base_dir>\csv_yaml_convertor\config\csv_files),
        no need to pass the argument of -csv, directly we can execute the script as below

        python convert_csv_to_yaml.py


   Step3: Once script is executed yaml files will be stored in below path

        path: (<base_dir>\csv_yaml_convertor\config\deployment).

   Step4:

      Cleanup, if you want to delete yaml files, which are generated, execute remove_yaml_files() function,
      which is located under common/functions.py file


