# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import namedtuple


class Exploration_data:
    def __init__(self, df):
        self.df = df


    def get_float_columns(self):
        """
        Get float columns
        """
        list_floats = list(self.df.select_dtypes(include=['float']).columns)
        return list_floats


    def get_int_columns(self):
        """
        Get integer columns
        """
        list_int = list(self.df.select_dtypes(include=['int']).columns)
        return list_int


    def get_object_columns(self):
        """
        Get object columns
        """
        list_objects = list(self.df.select_dtypes(include=['O']).columns)
        return list_objects


    def get_count_of_missing_values(self):
        """
        Get count of missing values in DataFrame
        """
        missing_df = pd.DataFrame(
            self.df.isnull().sum().sort_values(ascending=False))
        return missing_df


    def get_columns_with_missing_values(self):  #df dataframe
        """
        Get columns with missing values
        """
        missing_df = self.get_count_of_missing_values()
        missing_data = missing_df[missing_df[0] != 0]
        return missing_data


    def get_columns_without_missing_values(self):  #df dataframe
        """
        Get columns with out missing values
        """
        missing_df = self.get_count_of_missing_values()
        clean_data = missing_df[missing_df[0] == 0]
        return clean_data


    def get_count_missing_vals_in_1column(self, col_name):  #df dataframe & col_name : name of column
        """
        Get the count of missing values in one column
        """
        missing_df = self.get_count_of_missing_values()
        ds_missing_values = self.df.shape[0] - missing_df.loc[col_name][0]
        return ds_missing_values


    def visualize_feature_types(self):
        """
        Visualize a plot bar with the different types of features
        """
        list_floats = self.get_float_columns()
        list_objects = self.get_object_columns()
        list_int = self.get_int_columns()

        dx = pd.DataFrame({
            'lab': ['Object', 'int64', 'float64'],
            'count': [len(list_objects),
                      len(list_floats),
                      len(list_int)]
        })
        dx.plot.bar(x='lab',
                    y='count',
                    rot=0,
                    color=plt.cm.Paired(np.arange(3)))


    def visualize_type_local(self):
        """
        Visualize a plot bar with the number of each different types of local
        """
        fig, ax = plt.subplots(figsize=(10, 4))

        sns.countplot(y='type_local',
                      data=self.df,
                      order=self.df['type_local'].value_counts().index)
        plt.ylabel('Local type', size=18, color='red')
        ax.xaxis.set_ticks_position('top')
        ax.set_xlabel('')
        plt.title(' Distribution', size=15, weight=600, pad=60, loc='left')

        plt.show()


    def visualize_lot_surface_columns(self):
        """
        Visualize a plot bar with the number of lot for columns "lot_number1-5"
        """
        L = [
            'lot1_surface_carrez', 'lot2_surface_carrez',
            'lot3_surface_carrez', 'lot4_surface_carrez', 'lot5_surface_carrez'
        ]
        K = []
        for i in L:
            m = self.get_count_missing_vals_in_1column(col_name=i)
            K.append(m)

        dx = pd.DataFrame({
            'lot_surface_carrez': list(np.arange(1, 6)),
            'count real values': K
        })
        dx.plot.bar(x='lot_surface_carrez',
                    y='count real values',
                    rot=0,
                    color=plt.cm.Paired(np.arange(5)))


    def visualize_lot_numero_columns(self):

        L = [
            'lot1_numero', 'lot2_numero', 'lot3_numero', 'lot4_numero',
            'lot5_numero'
        ]
        K = []
        for i in L:
            m = self.get_count_missing_vals_in_1column(col_name=i)
            K.append(m)

        dx = pd.DataFrame({
            'lot_numero': list(np.arange(1, 6)),
            'count real values': K
        })
        dx.plot.bar(x='lot_numero',
                    y='count real values',
                    rot=0,
                    color=plt.cm.Paired(np.arange(5)))
