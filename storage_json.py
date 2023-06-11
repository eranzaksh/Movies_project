import json
import os

import requests

from istorage import IStorage

API_KEY = "711e7593"
URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="


class StorageJson(IStorage):
    def __init__(self, filepath):
        self.filepath = filepath

    @staticmethod
    def pr_red(skk):
        """
        Make a print statement in red color
        """
        print("\033[91m {}\033[00m".format(skk))

    def list_movies(self):
        with open(self.filepath, 'r') as handle:
            if os.path.getsize(self.filepath) == 0:
                return
            movies_data = json.load(handle)
        return movies_data

    def add_movie(self, title, rating, year, poster, imdb_page):
        """
        Adding a movie to the json file if it exists on the api database
        """
        movies_list = self.list_movies()
        if movies_list is None:
            movies_list = {}
        try:
            res = requests.get(URL + title)
            movie_data = res.json()
            if 'Error' in movie_data:
                raise Exception(self.pr_red("Movie not found!"))
            new_movie = {movie_data['Title']: {'Ratings': float(movie_data[rating]), 'Year': movie_data[year],
                                               'Poster': movie_data[poster], "Page": movie_data[imdb_page]}}
            movies_list.update(new_movie)
            json_data = json.dumps(movies_list)
            with open(self.filepath, 'w') as handle:
                handle.write(json_data)
            return
        except requests.exceptions.RequestException:
            self.pr_red("There is no internet connection!")

    def delete_movie(self, title):
        """
        Deletes a movie from the json file
        """
        movies_list = self.list_movies()
        del movies_list[title]
        json_data = json.dumps(movies_list)
        with open(self.filepath, 'w') as handle:
            handle.write(json_data)
        return

    def update_movie(self, title, notes):
        """
        Updating notes on a chosen movie in the json file
        """
        movies_list = self.list_movies()
        movies_list[title]["Notes"] = notes
        json_data = json.dumps(movies_list)
        with open(self.filepath, 'w') as handle:
            handle.write(json_data)
        return
