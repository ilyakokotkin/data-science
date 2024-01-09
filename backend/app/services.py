import pandas as pd
from scipy.stats import shapiro

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
            stat, p = shapiro(dataframe[column].dropna())
            result[column] = {'statistic': stat, 'p_value': p}
        return result
