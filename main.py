import os
import sys
from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv
import argparse

parser = argparse.ArgumentParser(description='A parser to pick which storage to use.')

parser.add_argument('-f', '--file', help='Specify the file name and .csv or .json extensions!')
args = parser.parse_args()
file_name = args.file
if not file_name.endswith('json') and not file_name.endswith('csv'):
    sys.exit("Incorrect file type!")
if not os.path.exists(file_name):
    with open(file_name, 'w') as fp:
        pass
if file_name.endswith('json'):
    storage = StorageJson(file_name)
else:
    storage = StorageCsv(file_name)
movie_app = MovieApp(storage)
movie_app.run()
