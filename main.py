from storage_json import StorageJson
from movie_app import MovieApp

def main():
    """Main function of the program."""
    # Create a StorageJson object with the path to the JSON file
    storage = StorageJson("movies_list.json")

    # Create a MovieApp object with the StorageJson object
    app = MovieApp(storage)

    # Run the application
    app.run()

if __name__ == "__main__":
    main()

