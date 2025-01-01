import pandas as pd
import cv2
import csv
import numpy as np


def normalize_csv_data(filename):
    try:
        # Load the CSV file
        data = pd.read_csv(filename)
        
        # Check if necessary columns exist
        if 'X' not in data.columns or 'Y' not in data.columns:
            print("Error: CSV file must contain 'X' and 'Y' columns.")
            return None
        
        # Normalize the 'X' and 'Y' columns
        X_min, X_max = data['X'].min(), data['X'].max()
        Y_min, Y_max = data['Y'].min(), data['Y'].max()

        # Avoid division by zero in normalization
        if X_max == X_min or Y_max == Y_min:
            print("Error: Cannot normalize data; all X or Y values are identical.")
            return None
        
        # Normalize and round to 2 decimal places
        data['X'] = ((data['X'] - X_min) / (X_max - X_min)).round(2)
        data['Y'] = ((data['Y'] - Y_min) / (Y_max - Y_min)).round(2)
        
        # Drop any other columns if you only want the normalized data
        normalized_data = data[['Frame', 'X', 'Y']]
        
        # Overwrite the same file with the normalized data
        normalized_data.to_csv(filename, index=False)
        print(f"Normalized data saved to '{filename}' with values rounded to 2 decimal places.")

        return normalized_data
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def display_drawing_with_opencv(csv_file, name):
    # Canvas dimensions (adjust as needed)
    canvas_width = 640
    canvas_height = 480

    # Create a blank image to draw the path
    canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

    x_coords, y_coords = [], []

    # Read the coordinates from the CSV file
    try:
        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                x_coords.append(int(float(row['X']) * canvas_width))  # Scale normalized values to canvas width
                y_coords.append(int(float(row['Y']) * canvas_height))  # Scale normalized values to canvas height
    except FileNotFoundError:
        print(f"Error: File '{csv_file}' not found.")
        return
    except ValueError:
        print("Error: Invalid data in the CSV file.")
        return

    # Check if there are coordinates to plot
    if not x_coords or not y_coords:
        print("No data found in the CSV file to display.")
        return

    # Draw the path with arrows on the canvas
    for i in range(1, len(x_coords)):
        start_point = (x_coords[i - 1], y_coords[i - 1])
        end_point = (x_coords[i], y_coords[i])
        cv2.arrowedLine(canvas, start_point, end_point, (0, 255, 0), 2, tipLength=0.3)  # Green arrow

    # Highlight the start and end points
    cv2.circle(canvas, (x_coords[0], y_coords[0]), 5, (255, 0, 0), -1)  # Blue start point
    cv2.circle(canvas, (x_coords[-1], y_coords[-1]), 5, (0, 0, 255), -1)  # Red end point

    # Add a title to the canvas
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (255, 255, 255)  # White text
    thickness = 2
    text_position = (10, 30)  # Top-left corner (adjust as needed)
    cv2.putText(canvas, name, text_position, font, font_scale, color, thickness)
    
    # Display the canvas using OpenCV
    cv2.imshow(f"{name}", canvas)

    print("Press any key to close the window...")
    cv2.waitKey(0)  # Wait for a key press
    cv2.destroyAllWindows()


# Normalize the CSV data
normalize_csv_data('coordinates.csv')

# Display the drawing with OpenCV
display_drawing_with_opencv('coordinates.csv', "Drawing Title")
