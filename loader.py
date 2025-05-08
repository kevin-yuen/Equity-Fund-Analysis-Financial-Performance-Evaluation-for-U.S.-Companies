'''
Description:
    This class handles the data loading process.

Parameters:
    relative_src_file_path (str): The relative file path where the source csv data file is stored.

Methods:
    - load_src_into_dataframe(filepath): Reads and loads the source csv data file into a Pandas dataframe.
    - merge_dataframes(df, debt_to_income_df): Merges df with debt_to_income_df dataframe.
'''

import pandas as pd

class Loader:
    def load_src_into_dataframe(self, relative_src_file_path):
        '''
        Read and load the source csv data file into a Pandas dataframe.

        :param relative_src_file_path: The relative file path where the source csv data file is stored.
        :return: The Pandas dataframe created by reading and loading the source csv data file.
        '''
        df = pd.read_csv(f'{relative_src_file_path}', sep=',')
        return df

    def merge_dataframes(self, orig_df, debt_to_income_df):
        '''
        Merge the original Pandas dataframe with debt_to_income_df dataframe.

        :param orig_df: The Pandas dataframe created by reading and loading the source csv data file.
        :param debt_to_income_df: The Pandas dataframe with the result of dividing total_long_term_debt by total_revenue.
        :return: The combination of the original pandas dataframe and debt_to_income_df dataframe.
        '''
        debt_to_income_df = debt_to_income_df[['business_id', 'debt_to_income_ratio']]      # remove unnecessary columns
        merged_df = orig_df.merge(right=debt_to_income_df, how='inner', on='business_id')
        return merged_df