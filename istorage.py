import json
import requests
from abc import ABC, abstractmethod

class IStorage(ABC):
    API_URL = "http://www.omdbapi.com/"
    API_KEY = "6f0c3bf6"

    @abstractmethod
    def list_movies(self):
        """
        Lists all movies in the database.
        """
        try:
            with open('movies_list.json', 'r') as file:
                movies = json.load(file)

            print(f"There are {len(movies)} movies in total:")
            for movie, info in movies.items():
                year = info.get("year", "Unknown")
                rating = info.get("rating", "Unknown")
                print(f"{movie} ({year}): {rating}")
        except FileNotFoundError:
            print("Movie database file not found. Please add a movie to initialize the database.")
        except json.JSONDecodeError:
            print("Error reading the movie database file. It might be corrupted.")

        input("\nPress Enter to return to the menu...")

    @abstractmethod
    def add_movie(self):
        """
        Adds a movie to the database using OMDb API.
        """
        movie_title = input("Enter the movie title you want to add: ").strip()
        try:
            # Fetch movie data from OMDb API
            response = requests.get(self.API_URL, params={"t": movie_title, "apikey": self.API_KEY})
            response.raise_for_status()
            movie_data = response.json()

            # Handle case where movie is not found
            if movie_data.get("Response") == "False":
                print(f"Error: {movie_data.get('Error', 'Movie not found.')}")
                return

            # Extract required details
            title = movie_data.get("Title")
            year = movie_data.get("Year")
            rating = movie_data.get("imdbRating", "N/A")
            poster = movie_data.get("Poster", "N/A")

            # Save to database
            try:
                with open('movies_list.json', 'r') as file:
                    movies = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                movies = {}

            movies[title] = {"year": year, "rating": rating, "poster": poster}

            with open('movies_list.json', 'w') as file:
                json.dump(movies, file, indent=4)

            print(f"Movie '{title}' added successfully!")
        except requests.exceptions.RequestException:
            print("Error: Unable to connect to the OMDb API. Please check your internet connection.")

    @abstractmethod
    def delete_movie(self, title):
        """
        Deletes a movie from the database.
        """
        try:
            with open('movies_list.json', 'r') as file:
                movies = json.load(file)

            title = input("Enter the movie title you want to delete: ").strip()
            if title in movies:
                del movies[title]
                with open('movies_list.json', 'w') as file:
                    json.dump(movies, file, indent=4)
                print(f"Movie '{title}' deleted successfully.")
            else:
                print(f"Error: Movie '{title}' not found in the database.")
        except FileNotFoundError:
            print("Error: Movie database file not found. Cannot delete movie.")
        except json.JSONDecodeError:
            print("Error reading the movie database file. It might be corrupted.")

        input("\nPress Enter to return to the menu...")

    @abstractmethod
    def update_movie(self, title, rating):
        """
        Updates a movie's rating in the database.
        This method is kept as-is, per the specification.
        """
        pass
