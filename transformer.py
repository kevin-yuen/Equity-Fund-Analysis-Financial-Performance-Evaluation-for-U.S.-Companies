'''
Description:
    This class handles the data transformation process.

Parameters:
    orig_df (DataFrame): The Pandas DataFrame created by reading and loading the source csv data file.

Methods:
    - normalize_column_names(df): Standardizes source column names using snake_case.
    - cast_column_data_type(df): Casts data type of each column to an appropriate type.
    - identify_duplicate_rows(df): Finds duplicate records by all columns.
    - drop_column(df): Drops unnecessary column(s).
    - round_to_two_decimal_places(df): Rounds numeric columns into two decimal places.
'''

from utils.mapping import new_column_mapping, column_type

class Transformer:
    def normalize_column_names(self, orig_df):
        '''
        Standardize column names.

        :param orig_df: The Pandas DataFrame created by reading and loading the source csv data file.
        :return: The Pandas DataFrame with column names in standardized format.
        '''
        orig_df = orig_df.rename(columns=new_column_mapping)

        print('Column names are normalized')
        return orig_df

    def cast_column_data_type(self, orig_df):
        '''
        Cast data type of each column to an appropriate data type.

        :param orig_df: The Pandas DataFrame created by reading and loading the source csv data file.
        '''
        for column in orig_df.columns:
            if column in column_type.keys() and orig_df[column].dtypes != column_type[column]:
                orig_df[column] = orig_df[column].astype(column_type[column])

        print('The data type of each column is cast')

    def identify_duplicate_rows(self, orig_df):
        '''
        Find duplicate records by all columns by creating a new column, is_dup.
        The new column indicates whether the record is a duplicate record.
        Duplicate records will be stored in a new dataframe.

        :param orig_df: The Pandas DataFrame created by reading and loading the source csv data file.

        :returns:
         - The original Pandas DataFrame with the new column, is_dup.
         - The Pandas DataFrame that stores duplicate records.
        '''
        orig_df['is_dup'] = orig_df.duplicated()

        # copy duplicate records to dup_df dataframe
        dup_df = orig_df[orig_df['is_dup'] == True]
        return orig_df, dup_df

    def drop_column(self, orig_df):
        '''
        Drop the 'is_dup' column.

        :param orig_df: The Pandas DataFrame with the new column, is_dup.
        :return: The Pandas DataFrame without the 'is_dup' column.
        '''
        orig_df = orig_df.drop(columns='is_dup')
        return orig_df

    def round_to_two_decimal_places(self, orig_df):
        '''
        Round data value to two decimal places for all columns that are in float data type.

        :param orig_df: The Pandas DataFrame created by reading and loading the source csv data file.
        '''
        orig_df[orig_df.select_dtypes(include='float64').columns] = orig_df.select_dtypes(include='float64').round(2)