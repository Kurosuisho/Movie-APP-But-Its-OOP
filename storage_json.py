import json
from istorage import IStorage


class StorageJson(IStorage):
    def __init__(self, file_path):
        """
        Initialize the storage with the given file path.
        Args:
            file_path (str): The path to the JSON file storing movies.
        """
        self.file_path = file_path

    def list_movies(self):
        """
        Returns a dictionary of dictionaries containing the movies information.

        Loads the data from the JSON file. If the file doesn't exist,
        returns an empty dictionary.

        Returns:
            dict: A dictionary with movie titles as keys and details as values.
        """
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Error decoding JSON file: {e}"
            )

        return data

    def add_movie(self, title, year, rating, poster=None):
        """
        Adds a movie to the database.

        Args:
            title (str): The movie title.
            year (int): The release year of the movie.
            rating (float): The movie's rating.
            poster (str, optional): Path or URL to the movie's poster.

        Raises:
            ValueError: If the movie already exists or input data is invalid.
        """
        if not title or not isinstance(year, int) or not isinstance(rating, (int, float)):
            raise ValueError(
                "Invalid input for movie details."
            )

        movies = self.list_movies()
        if title not in movies:
            movies[title] = {
                "year": year,
                "rating": rating,
                "poster": poster
            }
            self._save_movies(movies)
            print(
                f"Movie '{title}' added successfully!"
            )
        else:
            raise ValueError(
                "The movie is already in the database."
            )

    def delete_movie(self, title):
        """
        Deletes a movie from the database.

        Args:
            title (str): The title of the movie to delete.
        """
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)
            print(
                f"Movie '{title}' was removed from the database!"
            )
        else:
            print(
                "The movie does not exist in the database."
            )

    def update_movie(self, title, rating):
        """
        Updates a movie's rating in the database.

        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating for the movie.
        """
        movies = self.list_movies()
        if title in movies:
            movies[title]["rating"] = rating
            self._save_movies(movies)
            print(
                f"Movie '{title}' successfully updated."
            )
        else:
            print(
                "The movie is not in the database."
            )

    def _save_movies(self, movies):
        """
        Saves the updated movies dictionary to the JSON file.

        Args:
            movies (dict): The dictionary containing all movie details.
        """
        try:
            with open(self.file_path, 'w') as file:
                json.dump(
                    movies,
                    file,
                    indent=4
                )
        except IOError as e:
            raise IOError(
                f"Failed to save the movies database: {e}"
            )
