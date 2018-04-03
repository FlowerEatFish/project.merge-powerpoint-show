'''Main database fetcher'''
import json
import os


def fetch_data():
    '''Load config data from external file config.json'''
    local_directory = os.path.dirname(os.path.abspath(__file__))
    database_name = "config.json"
    database_path = os.path.join(local_directory, database_name)
    result = json.load(open(database_path))
    return result


def update_and_save_database(database):
    '''Save config data to external file config.json'''
    local_directory = os.path.dirname(os.path.abspath(__file__))
    database_name = "config.json"
    database_path = os.path.join(local_directory, database_name)
    with open(database_path, 'w') as outfile:
        json.dump(database, outfile)
