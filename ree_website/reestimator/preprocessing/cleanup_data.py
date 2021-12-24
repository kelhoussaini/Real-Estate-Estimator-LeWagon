from reestimator.Mysql_mgmt.get_data import Data_loading
import pandas as pd

class Cleaning_data:
    def __init__(self, df):
        self.df = df

    # commentée car a priori non utilisée, garée de côté au cas où
    # def conv_int(self,col):
    #     """
    #     Convert a column 'col' dtype (str, float, int)
    #     to the smallest type integer according to data
    #     """
    #     # to do : check if column mixed str (ex. '2A') and int. col.str.isnumeric()==False
    #     return pd.to_numeric(col, downcast='integer')


    def conv_downcast(self):
        """
        Downcast numeric dtypes in dataframe df to save memory
        """
        float_cols = self.df.select_dtypes('float').columns
        int_cols = self.df.select_dtypes('integer').columns

        self.df[float_cols] = self.df[float_cols].apply(pd.to_numeric, downcast='float')
        self.df[int_cols] = self.df[int_cols].apply(pd.to_numeric, downcast='integer')


    def conv_date(self, col_name):
        """
        Convert a date str column 'col' to datetime format MM/DD/YYYY
        """
        self.df[col_name] = pd.to_datetime(self.df[col_name], format='%m/%d/%Y')


    def drop_rows_of_specific_column(self, col_name):  #df dataframe
        """
        Drop rows of specific columns with Nan
        """
        self.df.dropna(how='any', subset=[col_name], inplace = True)


    # NORMALEMENT A ÉTÉ FAIT DANS REQUETE SQL DONC INITULE
    # def remplacement_mutation(self):
    #     """
    #     Remplace Sale by 1 and Others type of mutation data by 0 in nature_mutation column of df
    #     """
    #     replacement_mutation_dict = {
    #         'Vente': "1",
    #         'Vente terrain à bâtir': "0",
    #         'Echange': "0",
    #         "Vente en l'état futur d'achèvement": "0",
    #         'Adjudication': "0",
    #         'Expropriation': "0"
    #     }
    #     self.df['nature_mutation'] = self.df['nature_mutation'].replace(
    #         replacement_mutation_dict)


    def cadastral_sector(self):
        """
        Get secteur_cadastral from id_parcelle and add a column to df
        """
        self.df["secteur_cadastral"] = self.df["id_parcelle"].str.slice(5, 10)


    def filter_dependency(self, n_line='all'):
        """
        parameters
        ----------
            data: initial dataframe

        returns
        -------
            series with type_local filtered by dependency (downcoast to int8)
        """
        df_gr = self.df[self.df['type_local'] == 'Dépendance']

        if n_line == 'all':
            self.df['Dependency']=self.df.apply(lambda x: 1 if x.id_mutation in df_gr.id_mutation.values else 0, axis=1)
            self.df = self.df[(self.df['type_local'] != 'Dépendance')]

        else:
            self.df['Dependency']=self.df.head(n_line).apply(lambda x: 1 if x.id_mutation in df_gr.id_mutation.values else 0, axis=1)
            self.df = self.df[(self.df['type_local'] != 'Dépendance')]


    def drop_duplicates(self, col_name):
        self.df.drop_duplicates(subset=[col_name])


    def cut_price(self, appart_max, mais_max, col_name):

        cd_app = self.df[col_name] <= appart_max
        sel_app = self.df['type_local'] == 'Appartement'
        cd_mais = self.df[col_name] <= mais_max
        sel_mais = self.df['type_local'] == 'Maison'

        self.df = self.df[ (cd_app & sel_app) | (cd_mais & sel_mais)]


    def cleaning(self):

        self.conv_downcast()
        self.conv_date('date_mutation')
        self.filter_dependency()
        self.drop_duplicates('id_mutation')
        self.cut_price(50000, 160000, 'Prixm2') # 50000 prix m2 record constaté à Paris, 160000 prix m2 record pour villa
        return self.df

if __name__ == '__main__':
    dataloader = Data_loading()
    df = dataloader.load_data_chunk('data_working_update', 100000)
    cleaner = Cleaning_data(df)
    cleaner.cleaning()
    cleaner.df.shape
    cleaner.df.head(10)
    cleaner.df.tail(10)
    dataloader.data_to_sql(cleaner.df, data_cleaned, 'replace')
