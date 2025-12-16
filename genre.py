import csv
import pandas as pd
import matplotlib.pyplot as plt 

class GenrePopularity:
    """
    Manages music genre listening counts, calculates popularity statistics,
    and handles persistence via a CSV file (Case Study 96).
    """
    def __init__(self, csv_file='genres.csv'):
        self.data = {}  # {genre: listens}
        self.csv_file = csv_file
        self.load_csv()
        print(f" Initialized. Loaded {len(self.data)} genres from {self.csv_file}")

    # --- Data Management Methods ---
    
    def load_csv(self):
        """Loads genre data from the CSV file into self.data."""
        try:
            with open(self.csv_file, mode='r', newline='') as file:
                reader = csv.reader(file)
                # Skip header if present (assuming format: Genre,Listens)
                next(reader, None) 
                for row in reader:
                    if len(row) == 2:
                        genre, listens = row
                        self.data[genre.strip()] = int(listens.strip())
        except FileNotFoundError:
            # File doesn't exist yet, start with empty data
            pass
        except Exception as e:
            print(f" Error loading CSV: {e}")

    def save_csv(self):
        """Writes current genre data from self.data to the CSV file."""
        try:
            with open(self.csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Genre', 'Listens']) # Write header
                for genre, listens in self.data.items():
                    writer.writerow([genre, listens])
            print(f"💾 Data saved successfully to {self.csv_file}")
        except Exception as e:
            print(f" Error saving CSV: {e}")

    def add_genre(self, name, count):
        """Adds or updates the listening count for a given genre."""
        name = name.strip().title()
        try:
            count = int(count)
            if name in self.data:
                self.data[name] += count
                print(f"🎶 Updated '{name}': +{count} listens. New total: {self.data[name]}")
            else:
                self.data[name] = count
                print(f"🆕 Added new genre '{name}' with {count} listens.")
            self.save_csv()
        except ValueError:
            print(" Error: Count must be a valid integer.")
            
    def delete_genre(self, name):
        """Deletes a genre from the data."""
        name = name.strip().title()
        if name in self.data:
            del self.data[name]
            print(f"🗑️ Genre '{name}' deleted successfully.")
            self.save_csv()
        else:
            print(f" Error: Genre '{name}' not found.")

    # --- Analytics Methods ---

    def get_statistics(self):
        """Calculates and displays popularity statistics."""
        if not self.data:
            print("📊 No data available to calculate statistics.")
            return

        # Use Pandas Series for easy calculation
        s = pd.Series(self.data)
        total_listens = s.sum()
        num_genres = len(s)

        # Calculations
        most_popular = s.idxmax()
        least_popular = s.idxmin()
        average_listens = s.mean()
        
        print("\n" + "="*40)
        print(" MUSIC POPULARITY STATISTICS")
        print("="*40)
        print(f"Total Listens: {total_listens}")
        print(f"Number of Genres: {num_genres}")
        print(f"Average Listens/Genre: {average_listens:.2f}")
        print(f"Most Popular Genre: {most_popular} ({s[most_popular]} listens)")
        print(f"Least Popular Genre: {least_popular} ({s[least_popular]} listens)")
        print("-" * 40)
        
        # Percentage Share Calculation
        print("Percentage Share:")
        for genre, count in s.items():
            percentage = (count / total_listens) * 100
            print(f"  {genre}: {percentage:.1f}%")
        print("="*40)


    # --- Visualization Methods (Requires Matplotlib) ---

    def plot_bar_chart(self):
        """Generates and saves a bar chart of genre popularity."""
        if not self.data:
            print(" Cannot generate chart: No data available.")
            return
            
        df = pd.DataFrame(list(self.data.items()), columns=['Genre', 'Listens'])
        df = df.sort_values(by='Listens', ascending=False)
        

        try:
            plt.figure(figsize=(10, 6))
            plt.bar(df['Genre'], df['Listens'], color='skyblue')
            plt.title('Genre Popularity by Listening Count')
            plt.xlabel('Genre')
            plt.ylabel('Listening Count')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            chart_filename = 'popularity.png'
            plt.savefig(chart_filename)
            print(f"\n Chart generated and saved as '{chart_filename}'. ")
        except ImportError:
            print("\n Matplotlib not installed. Chart generation skipped.")
            print("To generate the chart, run: pip install matplotlib. ")
        except Exception as e:
            print(f" Error generating chart: {e}")

    def display_current_data(self):
        """Helper to quickly show current loaded data."""
        if not self.data:
            print("Current Data: (Empty)")
        else:
            print("\n--- Current Data Dictionary ---")
            for genre, listens in self.data.items():
                print(f"  {genre}: {listens}")
            print("------------------------------")

# --- Sample Usage Examples ---

# 1. Initialize the system (loads existing data or starts empty)
tracker = GenrePopularity()

# 2. Add initial data (5 unique genres)
tracker.add_genre("Pop", 500)
tracker.add_genre("Rock", 350)
tracker.add_genre("Jazz", 150)
tracker.add_genre("Hip-Hop", 600)
tracker.add_genre("Classical", 200)

# 3. Update an existing genre (Pop)
tracker.add_genre("Pop", 150)

# 4. Add a new genre with a small count (Folk)
tracker.add_genre("Folk", 50)

# 5. Add a new genre with a medium count (Electronic)
tracker.add_genre("Electronic", 300)

# 6. Delete a genre (Classical)
tracker.delete_genre("sahil")

# 7. Display the current raw data
tracker.display_current_data()

# 8. Display all calculated summary statistics
tracker.get_statistics()

# 9. Generate and save the popularity bar chart
tracker.plot_bar_chart()

# 10. Attempt to add a genre with invalid input
tracker.add_genre("sahil", "")
