'''
Description:
    This class handles the data extraction process from source files.

Parameters:
    src_file_path (str): Path to the source data file used by the Extractor.

Methods:
    - __convert_xlsx_to_csv(filename): Converts the raw excel data file to csv file format.
    - locate_data_file(): Finds the csv data file in the specified file path.
'''

import pandas as pd

class Extractor:
    def __init__(self, source_file_path):
        self.source_file_path = source_file_path
        self.is_file_converted = False

    def __convert_xlsx_to_csv(self, request_filename):
        '''
        Convert the raw excel data file to csv file format.

        :param request_filename: The filename entered by the user.
        '''
        try:
            df = pd.read_excel(f'{self.source_file_path}/{request_filename}.xlsx')
            df.to_csv(f'{self.source_file_path}/{request_filename}.csv', index=False)

            self.is_file_converted = True

            print(f'Successfully converted {request_filename}.xlsx to {request_filename}.csv')
        except FileNotFoundError:
            print(f'ERROR: File not found.')

    def locate_data_file(self):
        '''
        Find the csv data file.
        '''
        is_file_found = False

        while not is_file_found:
            request_filename = input("Please enter a filename (or type 'exit' to quit):\n").strip()

            if request_filename != '':
                if request_filename != 'exit':
                    self.__convert_xlsx_to_csv(request_filename)

                    if self.is_file_converted == True:
                        return f'{self.source_file_path}/{request_filename}.csv'
                    else:
                        # if file conversion fails, ask user enter a filename again
                        continue
                else:
                    # if 'exit', end program
                    break
            else:
                continue
