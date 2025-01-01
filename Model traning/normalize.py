# import pandas as pd

# def normalize_csv_data(filename):
#     try:
#         data = pd.read_csv(filename)
        
#         if 'X' not in data.columns or 'Y' not in data.columns:
#             print("Error: CSV file must contain 'X' and 'Y' columns.")
#             return None
#         X_min, X_max = data['X'].min(), data['X'].max()
#         Y_min, Y_max = data['Y'].min(), data['Y'].max()
#         if X_max == X_min or Y_max == Y_min:
#             print("Error: Cannot normalize data; all X or Y values are identical.")
#             return None
        
#         # Add normalized columns
#         data['X'] = (data['X'] - X_min) / (X_max - X_min)
#         data['Y'] = (data['Y'] - Y_min) / (Y_max - Y_min)
        
#         normalized_data = data[['Frame', 'X', 'Y']]
        
#         normalized_data.to_csv(filename, index=False)
#         print(f"Normalized data saved to '{filename}'.")

#         return normalized_data
    
#     except FileNotFoundError:
#         print(f"Error: File '{filename}' not found.")
#         return None
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None




import pandas as pd

def normalize_csv_data(filename):
    """
    Opens a CSV file, normalizes the 'X' and 'Y' columns,
    rounds the values to 2 decimal places, and overwrites the file.

    Args:
        filename (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame with normalized and rounded data.
    """
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
        data['X'] = ((data['X'] - X_min) / (X_max - X_min)).round(3)
        data['Y'] = ((data['Y'] - Y_min) / (Y_max - Y_min)).round(3)
        
        # Drop any other columns if you only want the normalized data
        data.rename(columns={'X': 'x', 'Y': 'y'}, inplace=True)
        normalized_data = data[['Frame', 'x', 'y']]
        
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



url = './datasets'
import os
folde_1 = os.listdir(url)
for i in folde_1:
    path_2 = os.path.join(url,i)
    path_3 = os.listdir(path_2)
    for j in path_3:
        path_4 = os.path.join(path_2,j)
        print(path_4)
        normalize_csv_data(path_4)