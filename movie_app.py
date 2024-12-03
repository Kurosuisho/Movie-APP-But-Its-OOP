import os
import time
from os.path import join
import requests

class MovieApp:
    def __init__(self, storage):
        """
        Initializes the MovieApp instance with a storage backend.

        Args:
            storage (IStorage): An object implementing the IStorage interface, 
            used to perform storage-related operations such as retrieving and updating movies.
        """
        self._storage = storage


    def _command_list_movies(self):
        """
        Retrieves and prints the list of movies in the database.

        Each movie is displayed along with its release year and rating.
        Waits for the user to press Enter before returning to the menu.
        """
        movies = self._storage.list_movies()
        print(f"There are {len(movies)} movies in total:")
        for movie, info in movies.items():
            rating = info["rating"]
            year = info["year"]
            print(f"{movie} ({year}): {rating}")

        # Wait for user to press Enter
        input("\nPress Enter to return to the menu...")
        

    def _command_movie_stats(self):
        """
        Computes and displays statistics about the movies in the database.

        The statistics include:
        - Average rating across all movies.
        - The title of the highest-rated movie.
        - The title of the lowest-rated movie.
        
        If no movies are available, a message indicating so is displayed.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movies to analyze.")
            return
        ratings = [float(details['rating']) for details in movies.values()]
        print(f"Average Rating: {sum(ratings) / len(ratings):.2f}")
        print(f"Highest Rated: {max(movies, key=lambda t: movies[t]['rating'])}")
        print(f"Lowest Rated: {min(movies, key=lambda t: movies[t]['rating'])}")
        

    import requests

    def _generate_website(self):
        """
        Generates a static HTML website displaying all movies in the storage.
        The movies are displayed with their title, year, and poster fetched from the OMDb API.
        """
        # Load the HTML template
        with open("_static/index_template.html", "r") as template_file:
            template_content = template_file.read()
        
        # Replace the __TEMPLATE_TITLE__ placeholder
        template_content = template_content.replace("__TEMPLATE_TITLE__", "My Movie App")
        
        # Generate the HTML for the movie grid
        movies = self._storage.list_movies()
        movie_items = []
        api_key = "6f0c3bf6"  # Replace with your actual API key
        base_url = "http://www.omdbapi.com/"
        
        for title, info in movies.items():
            try:
                # Fetch movie details from the OMDb API
                response = requests.get(base_url, params={"apikey": api_key, "t": title })
                response.raise_for_status()
                movie_data = response.json()
                
                # Use fetched data or fallback to storage data
                poster_url = movie_data.get("Poster", "https://via.placeholder.com/128x193?text=No+Image")
                year = movie_data.get("Year", info.get("year", "N/A"))
                
                # Create the HTML snippet for this movie
                movie_html = f"""
                <li>
                    <div class="movie">
                        <img class="movie-poster" src="{poster_url}" alt="{title}">
                        <div class="movie-title">{title}</div>
                        <div class="movie-year">{year}</div>
                    </div>
                </li>
                """
                movie_items.append(movie_html)
            except requests.RequestException as e:
                print(f"Error fetching data for {title}: {e}")
                continue
        
        movie_grid = "\n".join(movie_items)
        
        # Replace the __TEMPLATE_MOVIE_GRID__ placeholder
        template_content = template_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)
        
        # Write the final HTML to the output file
        output_file = "index.html"
        with open(output_file, "w") as f:
            f.write(template_content)
        
        print(f"Website generated successfully: {output_file}")

    

    def run(self):
        """
        Runs the main application loop.

        Displays a menu to the user with the following options:
        - List movies
        - Show movie statistics
        - Generate a website
        - Quit

        Executes the user's chosen command. If an invalid option is selected, 
        prompts the user to try again.
        """
        commands = {
            "1": self._command_list_movies,
            "2": self._command_movie_stats,
            "3": self._generate_website,
        }
        while True:
            print("\nMenu:")
            print("1. List movies")
            print("2. Movie statistics")
            print("3. Generate website")
            print("4. Quit")
            choice = input("Choose an option: ")
            print()
            if choice == "4":
                print("Goodbye!")
                break
            command = commands.get(choice)
            if command:
                command()
            else:
                print("Invalid option. Please try again.")