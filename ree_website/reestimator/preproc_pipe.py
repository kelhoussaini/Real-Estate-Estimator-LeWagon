
# Import libraries
import pandas as pd


class Preproc:
    def __init__(self, df):
        self.df = df


    def remove_dom_tom(self):
        """
        Function to remove DOM-TOM : 971 = Guadeloupe, 972=Martinique, 973=Guyane,
        974=Réunion, 975=Saint Pierre et Miquelon, 976=Mayotte

        parameters
        ----------
        df : pandas dataframe
            raw data ()

        returns:
        --------
        df : pandas dataframe
            filtered data set without DOM-TOM
        """

        self.df=self.df[(self.df['code_departement']!=976)
                        & (self.df['code_departement']!=975)
                        & (self.df['code_departement']!=974)
                        & (self.df['code_departement']!=973)
                        & (self.df['code_departement']!=972)
                        & (self.df['code_departement']!=971)]
        return self.df

    def remove_18_appart(self):
        """
        Function to remove Flats in departments 18 (Cher)
        => Incohérence des données d'appartements par rapport aux maisons
        """

        self.df=self.df[(self.df['code_departement'] != 18 & self.df['type_local']!='Maison')]
        return self.df


    def create_pricemeter(self):
        """
        Function to calculate the price/squared meters
        """

        self.df.loc[:, 'prixmetre'] = self.df[
            'valeur_fonciere'].values / self.df['surface_reelle_bati'].values
        # pd.options.display.float_format = '{:.2f}'.format  # pour remettre en format non scientifique
        return self.df



    def drop_2quant(self, target='prixmetre', quant_inf=0.05, quant_sup=0.05):
        """
        cuts a dataframe df values quantiles
        """
        inf = self.df[target].quantile(q=quant_inf)
        sup = self.df[target].quantile(q=quant_sup)
        filter = (self.df[target] <= inf) | (self.df[target] >= sup)
        return self.df.drop(self.df[filter].index, axis=0)

    def remove_outliers_1(self, target='prixmetre', area='code_departement', quant_inf = 0.05, quant_sup = 0.85):
        """
        Function used to choose the method to limit the min and max outliers
        """
        df_cut = pd.DataFrame()
        for i in self.df[area].unique():
            dropped = self.drop_2quant(self.df[self.df[area] == i], target, quant_inf = quant_inf, quant_sup = quant_sup)
            df_cut = pd.concat([df_cut, dropped])
            del dropped

        return df_cut


    def remove_outliers_2(self, target='prixmetre', area='code_departement', quant_inf = 0.25, quant_sup = 0.75):

        df_outliers = pd.DataFrame()

        for i in self.df[area].unique():
            df_temp = self.df[self.df[area] == i]
            quant_inf = df_temp[target].quantile(0.25)
            quant_sup = df_temp[target].quantile(0.75)
            IQR = quant_sup - quant_inf  #IQR is interquartile range.
            filter = (df_temp[target] >= quant_inf - 1.5 * IQR) & (df_temp[target]
                                                           <= quant_sup + 1.5 * IQR)
            filtered = df_temp.loc[filter]
            df_outliers = pd.concat([df_outliers, filtered], axis=0)
        return df_outliers

    def preproc_pipe(self):
>>>>>>> a7842853c339dc650d357f77ef0b592d3460f780
        """
        Method that saves the model into a .joblib file
        and uploads it on Google Storage /models folder
        """
        self.remove_dom_tom()
        self.remove_18_appart()
        self.create_pricemeter()
        df_outliers = self.remove_outliers_1()
    return df_outliers
