import cv2
import numpy as np
import time
import csv
import matplotlib.pyplot as plt
import matplotlib.image as imd
import warnings
import pandas as pd
warnings.filterwarnings('ignore')
import tensorflow as tf
warnings.filterwarnings('ignore')
import tensorflow as tf
import datetime
from tensorflow.keras.models import load_model

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"



spells = [
    "Alohomora",
    "Avada Kedavra",
    "Expelliarmus",
    "Expecto Patronum",
    "Lumos",
    "Nox",
    "Wingardium Leviosa",
    "Stupefy",
    "Library Lockus",
    "Professorious",
    "Mosquito Expellio",
    "Plagiarismus Detectio",
    "Basuri Melodico",
    "Giftus Appareus",
    "Manceps Bindio",
    "Ancestor Callium",
    "Dividius Zero",
    "Attendaceus Finalus",
    "Deadlineius Erasum",
    "Stressius",
    "Tempus Forwarius",
    "Tempus Reverisus",
    "Flyhigus Ascendo",
    "Flylowus Descendo",
    "Valentino" 
]


model = load_model('model_2.h5')

def display_video_in_hsv(video_path):
    # Open the video file or webcam
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Unable to open video.")
        return

    # Get the dimensions of the video
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a blank image to draw the path
    path_image = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

    # Variables to store the previous position of the green object
    prev_x, prev_y = None, None
    detected_positions = []  # Store recent positions for stability check

    # Drawing toggle flag
    is_drawing = True  # Starts with drawing enabled
    frame_counter = 0  # Counter to track frames per drawing
    max_frames = 100   # Maximum frames to save per drawing

    # Open the CSV file to save coordinates
    csv_file = "coordinates.csv"
    with open(csv_file, mode="w", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Frame", "X", "Y"])  # Write header row

        # Wait for 's' key to start
        print("Press 's' to start...")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Cannot read frame during wait.")
                break
            cv2.imshow('Press S to Start', frame)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                print("Starting video processing...")
                break

        # Variables for FPS calculation
        prev_time = time.time()

        while True:
            # Read each frame from the video
            ret, frame = cap.read()

            # Break the loop if no frame is returned (end of video)
            if not ret:
                print("End of video or cannot retrieve frame.")
                break

            # Calculate FPS
            current_time = time.time()
            fps = 1 / (current_time - prev_time)
            prev_time = current_time

            # Convert the frame to HSV format
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Define HSV range for green color
            lower_green = np.array([30, 25, 25])  # Adjust as needed
            upper_green = np.array([90, 255, 255])  # Adjust as needed

            # Create a mask for green color
            green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)

            # Apply morphological operations for noise reduction
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            green_open = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)  # Remove small noise
            green_close = cv2.morphologyEx(green_open, cv2.MORPH_CLOSE, kernel)  # Fill gaps

            # Find contours of the green object
            contours, _ = cv2.findContours(green_close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            valid_contour_found = False
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                if cv2.contourArea(largest_contour) > 500:  # Ignore small areas (e.g., noise)
                    valid_contour_found = True
                    x_min, y_min, width, height = cv2.boundingRect(largest_contour)
                    cv2.rectangle(frame, (x_min, y_min), (x_min + width, y_min + height), (0, 255, 0), 2)

                    center_x = x_min + width // 2
                    center_y = y_min + height // 2

                    # Draw a dot at the center of the bounding box
                    cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1) 
                    # Get the center of the green object
                    moments = cv2.moments(largest_contour)
                    if moments['m00'] != 0:
                        x = int(moments['m10'] / moments['m00'])
                        y = int(moments['m01'] / moments['m00'])

                        # Adjust x to account for the flipped frame
                        x = frame_width - x  # Flip the x-coordinate horizontally

                        # Only draw if position change is significant
                        if is_drawing and prev_x is not None and prev_y is not None:
                            # Draw line between previous and current position
                            cv2.line(path_image, (prev_x, prev_y), (x, y), (0, 255, 0), 2)

                        # Save the coordinates to the CSV file (if within frame limit)
                        if is_drawing and frame_counter < max_frames:
                            csv_writer.writerow([frame_counter, x, y])
                            frame_counter += 1

                        # Update the previous position
                        prev_x, prev_y = x, y

            if not valid_contour_found:
                # Reset previous positions if no valid green object is detected
                prev_x, prev_y = None, None

            # Display FPS on the original frame
            fps_text = f"FPS: {fps:.2f}"
            cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Display the original frame
            cv2.imshow('Original Frame', frame)

            # Display the path image
            cv2.imshow("Path Image", path_image)

            # Check for key presses
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # Exit on 'Esc'
                break
            elif key == ord('e'):  # Toggle drawing on 'E'
                is_drawing = not is_drawing
                print(f"Drawing {'enabled' if is_drawing else 'disabled'}.")
            elif key == ord('c'):  # Clear the canvas on 'C'
                path_image = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)  # Reset the canvas
                frame_counter = 0  # Reset frame counter
                print("Canvas cleared and drawing reset.")
                file.seek(0)  # Move to the start of the file
                file.truncate()  # Clear the CSV file
                csv_writer.writerow(["Frame", "X", "Y"])  # Rewrite the header

    # Release the video capture object and close all OpenCV windows after the loop finishes
    cap.release()
    cv2.destroyAllWindows()
def display_drawing_with_opencv(csv_file,name):
    import cv2
    import csv
    import numpy as np

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
                x_coords.append(int(row['X']))
                y_coords.append(int(row['Y']))
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


    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (255, 255, 255)  # White text
    thickness = 2
    text_position = (10, 30)  # Top-left corner (adjust as needed)
    cv2.putText(canvas, name, text_position, font, font_scale, color, thickness)
    

    # Display the canvas using OpenCV
    
    cv2.imwrite(f'output_image.jpg', canvas)
    cv2.imshow(f"{name}", canvas)

    print("Press any key to close the window...")
    cv2.waitKey(0)  # Wait for a key press
    cv2.destroyAllWindows()

# Display video and then draw with directions


def predict(filename):
    data = pd.read_csv(filename)
    df = pd.DataFrame(data)
    X_min, X_max = df['X'].min(), df['X'].max()  # Example values
    Y_min, Y_max = df['Y'].min(), df['Y'].max()
    df['X_normalized'] = (df['X'] - X_min) / (X_max - X_min)
    df['Y_normalized'] = (df['Y'] - Y_min) / (Y_max - Y_min)
    # X = []
    # X.append(df[['X', '           ']].values)
    normalized_data = df[['X_normalized', 'Y_normalized']].values
    normalized_data = np.expand_dims(normalized_data, axis=0)
    predictions = model.predict(normalized_data)
    predicted_class = np.argmax(predictions, axis=1)
    return spells[predicted_class[0]]


while True:
    display_video_in_hsv(0)
    name = predict('coordinates.csv')
    display_drawing_with_opencv('coordinates.csv',name)

