'''
Description:
    This class coordinates the core ETL (Extract, Transform, Load) analysis pipeline for processing business data.
    The full data pipeline is executed in the correct sequence via the 'run()' method.

Parameters:
    src_file_path (str): Path to the source data file used by the Extractor.

Methods:
    run(): Executes the full ETL and analysis pipeline.

Functions:
    - locate_data_file(): Finds the specified data file.
    - load_src_into_dataframe(file_path): Loads data from the csv file into a dataframe.
    - normalize_column_names(df): Standardizes source column names using snake_case.
    - cast_column_data_type(df): Casts data type of each column to an appropriate type.
    - identify_duplicate_rows(df): Finds duplicate records by all columns.
    - drop_column(df): Drops unnecessary column(s).
    - round_to_two_decimal_places(df): Rounds numeric columns into two decimal places.
    - filter_rows(df): Filters records with negative debt_to_equity.
    - compute_desc_stats(df): Computes for descriptive statistics (mean, median, min, max).
    - compute_debt_to_income_ratios(df): Computes for debt_to_income ratios.
    - merge_dataframes(df, debt_to_income_df): Merges df with debt_to_income_df dataframe.
     - create_bar_chart(df): Create a bar chart showing the top 5 states with the highest total liabilities.
    - create_pie_chart(df): Create a pie chart showing the top 5 states with the highest sum of total_revenue.
    - create_scatter_plot(df): Create a scatter plot showing the relationship between average total_revenue and
        average debt_to_income ratio for each state.
    - create_horizontal_bar_chart(df): Create a horizontal bar chart showing the total count of businesses for
        each state.
'''

from extractor import Extractor
from transformer import Transformer
from loader import Loader
from analyzer import Analyzer
from visualizer import Visualizer

src_file_path = 'source_data'

class Main:
    def __init__(self, src_file_path):
        self.extractor = Extractor(src_file_path)
        self.transformer = Transformer()
        self.loader = Loader()
        self.analyzer = Analyzer()
        self.visualizer = Visualizer()

    def run(self):
        '''
        Execute functions that extract, transform, load, and analyze business data.
        '''
        src_file_path = self.extractor.locate_data_file()

        if src_file_path == None:
            return      # end program

        # load source csv data into a dataframe
        original_df = self.loader.load_src_into_dataframe(src_file_path)

        # ----- data pre-processing starts here ------
        # normalize column names
        original_df = self.transformer.normalize_column_names(original_df)

        # cast data types for columns
        self.transformer.cast_column_data_type(original_df)

        # identify duplicate rows
        original_df, dup_df = self.transformer.identify_duplicate_rows(original_df)

        print('\n----- DUPLICATE RECORDS -----')
        print(f'{dup_df.to_string()}\n')

        # get count of unique and duplicate records in original_df
        print('----- TOTAL COUNT OF UNIQUE & DUPLICATE RECORDS -----')
        cnt_of_is_dup = original_df.groupby('is_dup').count().to_string()
        print(f'{cnt_of_is_dup}\n')

        # drop is_dup column from orig_df dataframe
        original_df = self.transformer.drop_column(original_df)

        # check null values
        print('----- TOTAL COUNT OF NON-NULL VALUES -----')
        for column in original_df.columns:
            cnt_of_non_null_values = original_df[column].count()

            print(f'Count of non-null values for {column}: {cnt_of_non_null_values}')

        # round to nearest n decimal places
        self.transformer.round_to_two_decimal_places(original_df)
        # ----- data pre-processing ends here ------

        # ----- analysis starts here -----
        # filter all businesses with negative debt-to-equity ratios
        print('\n----- BUSINESSES WITH NEGATIVE DEBT-TO-EQUITY RATIOS -----')
        neg_debt_to_equity_df = self.analyzer.filter_rows(original_df)
        print(f"{neg_debt_to_equity_df[['business_id', 'business_state', 'debt_to_equity']].to_string()}\n")

        # get descriptive statistics by state
        print('----- DESCRIPTIVE STATISTICS BY STATE -----')
        stats_df = self.analyzer.compute_desc_stats(original_df)
        print(f'{stats_df.to_string()}\n')

        # get debt-to-income ratio for all rows
        print('----- DEBT-TO-INCOME RATIO FOR EVERY BUSINESS -----')

        debt_to_income_df = self.analyzer.compute_debt_to_income_ratios(original_df)
        print('----- DEBT-TO-INCOME DATAFRAME-----')
        print(f'{debt_to_income_df.to_string()}\n')

        # merge debt_to_income_df dataframe with original_df dataframe by business_id
        print('----- MERGE OF DEBT_TO_INCOME_DF AND ORIGINAL_DF DATAFRAME-----')
        merged_df = self.loader.merge_dataframes(original_df, debt_to_income_df)
        print(merged_df.to_string())
        # ----- analysis ends here -----

        # ----- visualization starts here -----
        self.visualizer.create_bar_chart(merged_df)

        self.visualizer.create_pie_chart(merged_df)

        self.visualizer.create_scatter_plot(merged_df)

        self.visualizer.create_horizontal_bar_chart(merged_df)
        # ----- visualization ends here -----

if __name__ == '__main__':
    main = Main(src_file_path)

    main.run()
