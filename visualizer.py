'''
Description:
    This class creates data visualization charts.

Methods:
    - __save_figure(filename): Saves the chart figure in the specified directory.
    - __clear_figure(): Clears the chart figure.
    - create_bar_chart(df): Create a bar chart showing the top 5 states with the highest total liabilities.
    - create_pie_chart(df): Create a pie chart showing the top 5 states with the highest sum of total_revenue.
    - create_scatter_plot(df): Create a scatter plot showing the relationship between average total_revenue and
        average debt_to_income ratio for each state.
    - create_horizontal_bar_chart(df): Create a horizontal bar chart showing the total count of businesses for
        each state.
'''

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

output_filepath = 'output'

class Visualizer:
    def __save_figure(self, output_filename):
        '''
        Save the chart figure in the specified directory.

        :param output_filename: The file name output.
        '''
        plt.savefig(f'{output_filepath}/{output_filename}.jpeg', bbox_inches='tight')

    def __clear_figure(self):
        '''
        Clear the chart figure.
        '''
        plt.clf()
        plt.close()

    def create_bar_chart(self, df):
        '''
        Create a bar chart showing the top 5 states with the highest total liabilities.

        :param df: The merge of the original Pandas dataframe and debt_to_income_df dataframe.
        '''
        # get the unique business state with the highest total liabilities
        top_liabilities_df = (df
                                  .sort_values(by='total_liabilities', ascending=False)
                                  .drop_duplicates(subset='business_state', keep='first')
                                  .head(5))

        # convert to billions
        top_liabilities_df['total_liabilities_billion'] = df['total_liabilities'] / 1e9

        # get the max total liabilities for setting max value for the y-axis
        max_liabilities = int(np.ceil(np.max(top_liabilities_df['total_liabilities_billion'])))
        yticks = [n for n in range(0, max_liabilities+1)]

        # format labels for y-axis
        yticks_labels = [f'${n}B' for n in yticks]

        sns.barplot(data=top_liabilities_df, x='business_state', y='total_liabilities_billion', color='orange', width=0.5)

        plt.xlabel('U.S. States', fontdict={'fontweight': 'bold'})
        plt.ylabel('Total Liabilities (in Billions)', fontdict={'fontweight': 'bold'})

        plt.xticks(rotation=45)
        plt.yticks(ticks=yticks, labels=yticks_labels)

        plt.title('TOTAL LIABILITIES BY STATE',
                  fontdict={
                      'fontsize': 12,
                      'fontweight': 'bold'
                  })

        # plt.show()
        self.__save_figure('bar_chart')
        self.__clear_figure()

    def create_pie_chart(self, df):
        '''
        Create a pie chart showing the top 5 states with the highest sum of total_revenue.

        :param df: The merge of the original Pandas dataframe and debt_to_income_df dataframe.
        '''
        # compute the sum of total_revenue and get the top 5 states
        sum_revenue_top_five_states_df = (df
                          .sort_values(by='business_state')
                          .groupby(by='business_state')
                          .agg({'total_revenue': 'sum'})
                          .head(5))

        plt.pie(
            x=sum_revenue_top_five_states_df['total_revenue'],
            labels=sum_revenue_top_five_states_df.index.tolist(),
            autopct='%1.1f%%')

        plt.legend(sum_revenue_top_five_states_df.index.tolist(), loc='lower left')

        plt.title(
            'TOTAL REVENUE DISTRIBUTION AMONG TOP 5 STATES',
            fontdict={
                'fontweight':'bold',
                'fontsize': 12
            })

        # plt.show()
        self.__save_figure('pie_chart')
        self.__clear_figure()

    def create_scatter_plot(self, df):
        '''
        Create a scatter plot showing the relationship between average total_revenue and average debt_to_income ratio
        for each state.

        :param df: The merge of the original Pandas dataframe and debt_to_income_df dataframe.
        '''
        df = (df
              .groupby('business_state')
              .agg(
            avg_revenue=('total_revenue', 'mean'),
            avg_debt_to_income_ratio=('debt_to_income_ratio', 'mean')
        ))

        # convert to millions
        df['avg_revenue_million'] = df['avg_revenue'] / 1e9

        # generate 10 yticks
        max_avg_revenue = np.max(df['avg_revenue_million'])
        temp_yticks = np.linspace(0, max_avg_revenue, 10)
        yticks = [f'${round(n, 2)}M' for n in temp_yticks]      # format yticks

        sns.scatterplot(df, x='avg_debt_to_income_ratio', y='avg_revenue_million', hue=df.index.tolist())

        plt.title(
            'AVERAGE REVENUE V.S. DEBT-TO-INCOME-RATIO BY STATE',
            fontdict={
                'fontweight':'bold',
                'fontsize': 12
            })

        plt.ylabel('Average Revenue', fontdict={'fontweight': 'bold'})
        plt.xlabel('Average Debt-to-Income Ratio', fontdict={'fontweight': 'bold'})

        plt.yticks(ticks=temp_yticks, labels=yticks)

        plt.legend(prop={'size': 8}, bbox_to_anchor=(1.05, 1), loc='upper left', ncol=2)
        plt.tight_layout()

        # plt.show()
        self.__save_figure('scatterplot')
        self.__clear_figure()

    def create_horizontal_bar_chart(self, df):
        '''
        Create a horizontal bar chart showing the total count of businesses for each state.

        :param df: The merge of the original Pandas dataframe and debt_to_income_df dataframe.
        '''
        df = df.groupby('business_state')['business_state'].value_counts().reset_index(name='cnt_of_businesses')

        sns.barplot(df, x='cnt_of_businesses', y='business_state', hue='business_state', width=0.5)

        plt.ylabel('States of the U.S.', fontdict={'fontweight': 'bold'})
        plt.xlabel('Count of Businesses', fontdict={'fontweight': 'bold'})

        plt.title(
            'COUNT OF BUSINESSES BY STATES',
                  fontdict={
                      'fontweight':'bold',
                      'fontsize': 12
                  })

        plt.tight_layout()

        # plt.show()
        self.__save_figure('hor_bar_chart')
        self.__clear_figure()
