import csv

from istorage import IStorage


class StorageCsv(IStorage):
    def __init__(self, filepath):
        self.filepath = filepath

    @staticmethod
    def pr_red(skk):
        """
        Make a print statement in red color
        """
        print("\033[91m {}\033[00m".format(skk))

    def add_movie(self, title, year, rating, poster, imdb_page):
        pass

    def list_movies(self):
        with open(self.filepath, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            # Convert CSV data to a list of dictionaries
            data = [dict(row) for row in csvreader]
        result = {}
        print(data)
        for row in data:
            title = row['Title']
            rating = int(float(row['Rating']))  # Convert rating to integer
            result[title] = {
                'Rating': rating,
                'Year': row['Year']
            }

    def update_movie(self, title, notes):
        pass

    def delete_movie(self, title):
        pass


