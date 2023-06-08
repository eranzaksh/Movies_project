import csv

import requests

from istorage import IStorage

API_KEY = "711e7593"
URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="


class StorageCsv(IStorage):
    def __init__(self, filepath):
        self.filepath = filepath

    @staticmethod
    def pr_red(skk):
        """
        Make a print statement in red color
        """
        print("\033[91m {}\033[00m".format(skk))

    def add_movie(self, title, rating, year, poster, imdb_page):
        """
        Adding a movie to the json file if it exists on the api database
        """
        try:
            res = requests.get(URL + title)
            movie_data = res.json()
            if 'Error' in movie_data:
                raise Exception(self.pr_red("Movie not found!"))
            movie_title = movie_data['Title']
            movie_rating = movie_data[rating]
            movie_year = movie_data[year]
            movie_poster = movie_data[poster]
            movie_page = movie_data[imdb_page]
            with open(self.filepath, 'a', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([movie_title, movie_rating, movie_year, movie_poster, movie_page])
            return
        except requests.exceptions.ConnectionError:
            self.pr_red("There is no internet connection!")

    def list_movies(self):
        with open(self.filepath, 'r', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)
            # Convert CSV data to a list of dictionaries
            data = [dict(row) for row in csvreader]
        movies = {}
        for row in data:
            title = row['Title']
            # rating = int(float(row['Ratings']))  # Convert rating to integer
            movies[title] = {
                'Ratings': row['Ratings'],
                'Year': row['Year'],
                'Poster': row['Poster'],
                'Page': row['Page'],
                'Notes': row['Notes']
            }
        return movies

    def update_movie(self, title, notes):
        movie_list = self.list_movies()
        movie_list[title]["Notes"] = notes
        with open(self.filepath, 'r') as csvfile:
            reader = csv.reader(csvfile)
            header_row = next(reader)
        with open(self.filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header_row)
        with open(self.filepath, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for movie, details in movie_list.items():
                row = [movie] + list(details.values())
                writer.writerow(row)
        return





    def delete_movie(self, title):
        pass
