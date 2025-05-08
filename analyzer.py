'''
Description:
    This class handles the data analysis process.

Methods:
    - compute_desc_stats(df): Computes descriptive statistics (mean, median, min, max) by business_state.
    - filter_rows(df): Filters records with negative debt_to_equity.
    - compute_debt_to_income_ratios(df): Computes for debt_to_income ratios.
'''

class Analyzer:
    def compute_desc_stats(self, orig_df):
        '''
        Compute descriptive statistics (mean, median, min, max) by business_state for all columns that are in int or float data type.

        :param orig_df: The Pandas dataframe created by reading and loading the source csv data file.
        :return: The Pandas dataframe with descriptive statistics by business_state for all columns that are in int or float data type.
        '''
        # get numeric data type columns
        numeric_columns = (orig_df[orig_df.select_dtypes(include=['int64', 'float64']).columns]
                           .drop(columns=['business_id']).columns)

        stats_df = orig_df.groupby('business_state')[numeric_columns].agg(['mean', 'median', 'min', 'max'])
        return stats_df

    def filter_rows(self, orig_df):
        '''
        Filter records with negative debt_to_equity.

        :param orig_df: The Pandas dataframe created by reading and loading the source csv data file.
        :return: The Pandas dataframe with negative debt_to_equity.
        '''
        return orig_df[orig_df['debt_to_equity'] < 0]

    def compute_debt_to_income_ratios(self, orig_df):
        '''
        Compute debt_to_income ratios by dividing total_long_term_debt by total_revenue.

        :param orig_df: The Pandas dataframe created by reading and loading the source csv data file.
        :return: The Pandas dataframe with the result of dividing total_long_term_debt by total_revenue.
        '''
        debt_to_income_df = orig_df[['business_id', 'total_long_term_debt', 'total_revenue']].copy()
        debt_to_income_df['debt_to_income_ratio'] = debt_to_income_df['total_long_term_debt'] / debt_to_income_df['total_revenue']

        return debt_to_income_df