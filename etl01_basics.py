# -------------------------------------------------------------------------
# Script for gathering functions for basic functions for Kaggle datasets
#
# (©) 2022 Juan Antonio Cabeza Sousa, Spain
# email juaancabsou@gmail.com
# -------------------------------------------------------------------------

import datatable as dtable
import pandas as pd

def read_data(path_data, dataset):
    """Function that reads data using fread function and transform it later to pandas format

    Args:
        path_data (String): Path where the data is located
        dataset (String): Name of the dataset to read

    Returns:
        Pandas DataFrame: DataFrame with the data
    """
    df_fread = dtable.fread(path_data+dataset, fill=True, na_strings=[''])
    df_pandas = df_fread.to_pandas()
    return (df_pandas)


def quickstats_df(df):
    """Function that generates quick stats as:
        - 1. Shape of the dataset
        - 2. % not nan values
        - 3. First 5 rows of the dataset

    Args:
        Pandas DataFrame: DataFrame with the data
    """
    
    # Statistic: Calculate nan values and cardinality
    rows_na =df.isna().sum().reset_index().rename(columns={0:'valuesNa'})
    rows_notna = df.notna().sum().reset_index().rename(columns={0:'valuesNotNa'})
    rows_analysis = pd.merge(rows_na, rows_notna, on='index', how='outer')
    rows_analysis['completeRatio'] = round((rows_analysis['valuesNotNa']) / (rows_analysis['valuesNotNa']+rows_analysis['valuesNa'])*100,2)
    
    cardinality = df.nunique().reset_index().rename(columns={0:'cardinality'})
    rows_analysis = pd.merge(rows_analysis, cardinality)
    

    # Statistic: Shape and number of duplicates of the dataframe
    print('Shape:',df.shape)
    dup_raw = df.duplicated().sum()
    dup_per = round(    (dup_raw*100)/df.shape[0],2)
    print('Duplicates: ', dup_raw, '->', dup_per, '%')

    # Statistic: Not nan values
    display(rows_analysis)
    
    # First 5 rows
    display(df.head())

    return None

# Check categorical data information
def pd_categories_trans(df, col):
    """Function that plots the different categories of a feature
    Args:
        Pandas DataFrame: DataFrame with the data
    """
    df = df[col].value_counts().reset_index().T
    new_header = df.iloc[0]
    df = df.iloc[1:]
    df.columns = new_header
    return df