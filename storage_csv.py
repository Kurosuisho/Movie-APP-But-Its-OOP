import csv
from istorage import IStorage


class StorageCsv(IStorage):
    def __init__(self, file_path):
        """
        Initialize the storage with the given file path.
        Args:
            file_path (str): The path to the CSV file storing movies.
        """
        self.file_path = file_path

    def _save_movies(self, movies):
        """
        Saves the movies data to a CSV file.

        Args:
            movies (dict): A dictionary where the keys are movie titles
                           and the values are dictionaries with movie details.
        """
        try:
            with open(self.file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                # Write the header row
                writer.writerow(["title", "rating", "year", "poster"])

                # Write each movie's details
                for title, details in movies.items():
                    writer.writerow([
                        title,
                        details.get("rating"),
                        details.get("year"),
                        details.get("poster", "")  # Default to empty string if no poster
                    ])
        except IOError as e:
            raise IOError(f"Failed to save the movies database: {e}")