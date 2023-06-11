import random
import matplotlib.pyplot as plt
import platform
import os
import movies_website

API_KEY = "711e7593"
URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    @staticmethod
    def sorting_movies(movies):
        """
        Sorting according to value from the highest to the lowest
        """
        return sorted(movies, key=lambda movie: movies[movie]["Ratings"], reverse=True)

    @staticmethod
    def pr_red(skk):
        """
        Make a print statement in red color
        """
        print("\033[91m {}\033[00m".format(skk))

    @staticmethod
    def clr_scr():
        """
        Check if the platform is Windows or linux
        If Platform is Windows then run command os.system(‘cls’) else os.system(‘clear’)
        """
        if platform.system().lower() == "windows":
            cmdtorun = 'cls'
        else:
            cmdtorun = 'clear'
        os.system(cmdtorun)

    @staticmethod
    def close_program():
        """
        Closing the program
        """
        raise SystemExit("Bye!")

    def _command_list_movies(self):
        """
        Prints a list of all movies and their ratings.
        """
        movies = self._storage.list_movies()
        if movies is None:
            print("No movies currently in the database")
            return
        total = len(movies)
        print(f"\n{total} movies in total")
        for key in movies:
            print(key, movies[key]["Ratings"])

    def _command_movie_stats(self):
        """
        Calculating average, median, worst and best movies and printing them.
        """
        movies = self._storage.list_movies()
        average_rating = 0
        median_rating = 0
        best_movies = ""
        worst_movies = ""
        sorted_movies_dict = {}
        for movie in self.sorting_movies(movies):
            sorted_movies_dict[movie] = movies[movie]["Ratings"]
        values_list = list(sorted_movies_dict.values())
        movies_count = len(movies)
        # calculating Average of movie ratings.
        for val in movies.values():
            average_rating += float(val["Ratings"])
        average_rating = average_rating / len(movies)
        # calculating median for even and odd overall movies
        if movies_count % 2 == 1:
            median_rating = values_list[movies_count // 2]
        if movies_count % 2 == 0:
            median_rating = (float(values_list[movies_count // 2]) + float(values_list[movies_count // 2 - 1])) / 2
        # String with the best movies and their ratings
        for key, val in sorted_movies_dict.items():
            if val >= values_list[0]:
                best_movies = best_movies + key + ", " + str(val) + ". "
        # String with the worst movies and their ratings
        for key, val in sorted_movies_dict.items():
            if val <= values_list[-1]:
                worst_movies = worst_movies + key + ", " + str(val) + ". "
        print("""\nAverage rating: {:.2f}""".format(average_rating))
        print(f"Median rating: {median_rating}")
        print(f"Best movies: {best_movies}")
        print(f"Worst movies: {worst_movies}\n")

    def _generate_website(self):
        """
        From the movie list, takes each movie and pass it on to serialize_movies func to write it on the output variable
        then writing the website with it
        """
        output = ""
        movies = self._storage.list_movies()
        for movie, stats in movies.items():
            output += movies_website.serialize_movies(movie, stats)
        movies_website.writing_webpage(output)
        print("Website generated successfully!")

    def _command_add_movie(self):
        """
        Checking if a movie isn't on the database then adds it
        """
        movies_list = self._storage.list_movies()
        movie_name = input("\nEnter new movie name: \033[33m")
        if movies_list is not None:
            if movie_name in movies_list:
                self.pr_red(f"Movie {movie_name} already exist!\n")
                return
        try:
            self._storage.add_movie(movie_name, "imdbRating", "Year", "Poster", "imdbID")
            print(f"\033[00mMovie {movie_name} successfully added\n")
        except Exception:
            return

    def _command_delete_movie(self):
        """
        Check if movie is in the database and delete it
        """
        movie_name = input("\nEnter a movie name to delete: \033[33m")
        movies = self._storage.list_movies()
        if movie_name not in movies:
            self.pr_red(f"Movie {movie_name} doesn't exist!\n")
            return
        self._storage.delete_movie(movie_name)
        print(f"Movie {movie_name} successfully deleted\n")

    def _command_update_movie(self):
        """
        Adding notes to a movie
        """
        movie_name = input("\nEnter a movie name: \033[33m")
        movies = self._storage.list_movies()
        if movie_name not in movies:
            self.pr_red(f"mMovie {movie_name} doesn't exist!\n")
            return
        user_notes = input("Enter movie notes: ")
        self._storage.update_movie(movie_name, user_notes)
        print(f"Movie {movie_name} successfully updated\n")

    def _command_random_movie(self):
        """
        Prints a random movie and it's stats
        """
        movies = self._storage.list_movies()
        movie, rating = random.choice(list(movies.items()))
        print(f"\nYour movie for tonight: {movie}, it's rated {rating['Ratings']}\n")

    def _command_search_movie(self):
        """
        Searching for a movie on the database
        """
        movies = self._storage.list_movies()
        user_search = input("\nEnter part of a movie name: \033[33m ")
        # checking if user input is in each key. if it is - print it.
        for movies_name, stats in movies.items():
            if user_search.lower() in movies_name.lower():
                print('\033[00m' + movies_name, stats["Ratings"])

    def _command_sorted_movies(self):
        """
        Send all the movies on the database to sorting_movies function and printing them.
        """
        movies = self._storage.list_movies()
        total = len(movies)
        print(f"\n{total} movies in total")
        for movie in self.sorting_movies(movies):
            print(f"{movie} {movies[movie]['Ratings']} {movies[movie]['Year']}")

    def _command_rating_histogram(self):
        """
        Creating a histogram based on database
        """
        movies = self._storage.list_movies()
        histogram_ratings = []
        for val in movies.values():
            histogram_ratings.append(val["Ratings"])
        plt.subplots(1, figsize=(8, 6))
        plt.title("Movie Ratings Histogram")
        plt.xlabel("Rating")
        plt.ylabel("Frequency")
        plt.hist(histogram_ratings)
        file_name = input("Enter the name of your histogram file: \033[33m")
        plt.savefig(file_name)
        print("\033[00mHistogram file was saved successfully!")

    def _command_generate_website(self):
        """
        From the movie list, takes each movie and pass it on to serialize_movies func to write it on the output variable
        then writing the website with it
        """
        output = ""
        movies = self._storage.list_movies()
        for movie, stats in movies.items():
            output += movies_website.serialize_movies(movie, stats)
        movies_website.writing_webpage(output)
        print("Website generated successfully!")

    @staticmethod
    def menu():
        print("""\033[32m
Menu:
0. Exit
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Create Rating Histogram
10. Generate website

Enter your choice (0-10):\033[0m""")

    def run(self):
        movie_choices = {
            0: self.close_program,
            1: self._command_list_movies,
            2: self._command_add_movie,
            3: self._command_delete_movie,
            4: self._command_update_movie,
            5: self._command_movie_stats,
            6: self._command_random_movie,
            7: self._command_search_movie,
            8: self._command_sorted_movies,
            9: self._command_rating_histogram,
            10: self._command_generate_website
        }
        print("\033[32m*" * 10 + " "'My Movies Database'" " + "*" * 10)
        while True:
            self.menu()
            try:
                user_choice = int(input('\033[33m'))
                print('\033[00m')
                movie_choices[user_choice]()
            except (KeyError):
                self.clr_scr()
                continue
            input("\nPlease press Enter to continue")
