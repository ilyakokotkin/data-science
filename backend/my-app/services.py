import pandas as pd
import numpy as np
from scipy.stats import norm, f

class CSVReader:
    @staticmethod
    def read_csv(file):
        df = pd.read_csv(file)
        return df

class ShapiroWilkTest:
    @staticmethod
    def perform_test(dataframe):
        """Performs the Shapiro-Wilk test on each column of a DataFrame.

        Args:
            dataframe: The DataFrame to test.

        Returns:
            A dictionary with the results for each column.
        """

        result = {}
        for column in dataframe.columns:
            data = dataframe[column].dropna()
            if len(data) > 3:  
                W = ShapiroWilkTest.calculate_W(data)
                p_value = ShapiroWilkTest.calculate_p_value(W, len(data))
                result[column] = {'W': W, 'p_value': p_value}
            else:
                result[column] = {'Error': 'Sample size too small'}
        return result

    @staticmethod
    def calculate_W(data):
        """Calculates the W statistic for the Shapiro-Wilk test.

        Args:
            data: The data to test.

        Returns:
            The W statistic.
        """

        n = len(data)
        # Sort data in ascending order
        sorted_data = np.sort(data)
        # Calculate mean and standard deviation
        mean = np.mean(data)
        std_dev = np.std(data)
        # Standardize the sorted data  
        standardized_data = (sorted_data - mean) / std_dev
        coefficients = ShapiroWilkTest.get_coefficients(n)
        # Compute W statistic using coefficients, standardized data, sums and means
        W = (np.sum(coefficients * standardized_data))**2 / np.sum((standardized_data - np.mean(standardized_data))**2)
        return W

    @staticmethod
    def get_coefficients(n):
        """Returns the coefficients for the Shapiro-Wilk test for a given sample size.

        Args:
            n: The sample size.

        Returns:
            The coefficients.
        """

        coefficients = [0.0] * n
        # Set first coefficient based on sample size
        coefficients[0] = np.sqrt(n)
        for i in range(1, n):
            # Calculate other coefficients recursively
            coefficients[i] = coefficients[i-1] * (n - i)
        coefficients = np.array(coefficients)
        # Normalize coefficients  
        coefficients /= np.sum(coefficients**2)
        return coefficients  
    
    @staticmethod
    def calculate_p_value(W, n):
        """Approximates the p-value for the Shapiro-Wilk test using a linear approximation.

        Args:
            W: The W statistic.
            n: The sample size.

        Returns:
            The approximate p-value.
        """

        # TODO: implementation of the linear approximation for p-value calculation
        pass

class FTestForEqualVariance:
    @staticmethod
    def perform_test(dataframe, column1, column2):
        """Performs the F-Test for equal variance between two columns of a DataFrame.

        Args:
            dataframe: The DataFrame containing the data.
            column1: The name of the first column to test.
            column2: The name of the second column to test.

        Returns:
            A dictionary with the F statistic and the p-value.
        """

        data1 = dataframe[column1].dropna()
        data2 = dataframe[column2].dropna()

        # Calculate variances
        var1 = np.var(data1, ddof=1)
        var2 = np.var(data2, ddof=1)

        # Ensure var1 is the larger variance to maintain F > 1
        if var1 < var2:
            var1, var2 = var2, var1
            data1, data2 = data2, data1

        # Calculate F statistic
        F = var1 / var2

        # Calculate degrees of freedom for each dataset
        df1 = len(data1) - 1
        df2 = len(data2) - 1

        # Calculate p-value
        p_value = 1 - f.cdf(F, df1, df2)

        return {'F': F, 'p_value': p_value}