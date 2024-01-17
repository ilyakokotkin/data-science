import pandas as pd
import numpy as np

class CSVReader:
    @staticmethod
    def read_csv(file):
        df = pd.read_csv(file)
        return df

class ShapiroWilkTest:
    @staticmethod
    def perform_test(dataframe):
        result = {}
        for column in dataframe.columns:
            data = dataframe[column].dropna()
            if len(data) > 3:  # Simplified check for sample size
                W = ShapiroWilkTest.calculate_W(data)
                result[column] = {'W': W}
            else:
                result[column] = {'Error': 'Sample size too small'}
        return result

    @staticmethod
    def calculate_W(data):
        n = len(data)
        sorted_data = np.sort(data)
        mean = np.mean(data)
        std_dev = np.std(data)
        standardized_data = (sorted_data - mean) / std_dev

        # Coefficients for Shapiro-Wilk (this is a simplification)
        # In reality, these are derived from the expected values of order statistics
        coefficients = ShapiroWilkTest.get_coefficients(n)

        W = (np.sum(coefficients * standardized_data))**2 / np.sum((standardized_data - np.mean(standardized_data))**2)
        return W

    @staticmethod
    def get_coefficients(n):
        # This is a placeholder; actual coefficients depend on n and are quite complex
        # Normally, these would be looked up from a table or calculated with a complex formula
        return np.array([0.5] * n)  # Simplified placeholder coefficients

