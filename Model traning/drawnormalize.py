import pandas as pd
import csv
url = 'datasets/3/j.csv'
import matplotlib.pyplot as plt

def plot_normalized_data(filename):

    try:
        # Load the CSV file
        data = pd.read_csv(filename)
        
        # Check if necessary columns exist
        if 'x' not in data.columns or 'y' not in data.columns:
            print("Error: CSV file must contain 'x' and 'y' columns.")
            return
        
        # Plot the path
        plt.figure(figsize=(8, 6))
        plt.plot(data['x'], data['y'], marker='o', color='b', label='Path')
        
        # Highlight the start and end points
        plt.scatter(data['x'].iloc[0], data['y'].iloc[0], color='green', label='Start Point', s=100, zorder=5)
        plt.scatter(data['x'].iloc[-1], data['y'].iloc[-1], color='red', label='End Point', s=100, zorder=5)
        
        # Add labels and title
        plt.title("Normalized Path Visualization", fontsize=16)
        plt.xlabel("x (Normalized)", fontsize=12)
        plt.ylabel("y (Normalized)", fontsize=12)
        plt.legend()
        plt.grid(True)
        plt.savefig("plot.png")  # Save the plot to a file for debugging
        print("Plot saved as 'plot.png'.")
        plt.show()
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")




# plot_drawing_from_csv(url)
plot_normalized_data(url)