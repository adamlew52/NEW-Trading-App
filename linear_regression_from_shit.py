import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import json

def compare_normalized_data(ticker_price, normalized_data, date):
    """
    Compare normalized data against a ticker price using linear regression.

    Args:
    ticker_price (float): The ticker price for the corresponding date.
    normalized_data (list): The normalized data points for the corresponding date.
    date (str): The date of the data points.

    Returns:
    float: The slope of the regression line, indicating the relationship.
    float: The intercept of the regression line.
    float: The R^2 score of the regression model.
    """
    # Convert normalized data to a numpy array and reshape for linear regression
    X = np.array(normalized_data).reshape(-1, 1)  # Features
    y = np.array([ticker_price] * len(normalized_data))  # Target variable (ticker price)

    # Create and fit the linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Get slope (coefficient), intercept, and R^2 score
    slope = model.coef_[0][0]
    intercept = model.intercept_[0]
    r_squared = model.score(X, y)

    print(f"Date: {date}")
    print(f"Slope: {slope}")
    print(f"Intercept: {intercept}")
    print(f"R^2 Score: {r_squared}")

    return slope, intercept, r_squared

def read_normalized_data(file_path):
    """
    Read normalized data from a text file.

    Args:
    file_path (str): Path to the text file containing normalized data.

    Returns:
    list: List of normalized data points.
    """
    with open(file_path, 'r') as file:
        data = file.read()
        # Convert the string representation of the list to an actual list
        normalized_data = eval(data)  # Use eval to convert string list to a list
        return normalized_data

# Example usage
if __name__ == "__main__":
    # Assuming the text file 'normalized_data.txt' contains the normalized data as a string list
    file_path = 'normalized_data.txt'
    
    # Read the normalized data from the file
    normalized_data = read_normalized_data(file_path)

    # Set your ticker price and date
    ticker_price = 50.0  # Example ticker price
    date = "2024-10-13"   # Example date

    # Compare the normalized data against the ticker price
    compare_normalized_data(ticker_price, normalized_data, date)
