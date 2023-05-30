import pandas as pd
import numpy as np
import datetime

# new functions to be used

def generate_data_description(form_name, df, limit):
    # form name : name of the form or the sheet
    # Df: Data frame
    # limit : to detect the limit of categories
    columns = df.columns

    dictionnaire = pd.DataFrame(
        columns=['Variable', 'Form Name', 'Total (records)', 'Nb of Unknown', 'Nb of na', 'Number of Empty',
                 'Missing rate', 'Col Type', 'Values collected',
                 'col_min', 'col_max', 'col_avg', 'quantile 25', 'quantile 50',
                 'quantile 75'])

    dictionnaire = pd.concat([describe_col(c, df, dictionnaire, form_name, limit) for c in columns])
    return dictionnaire

def describe_col(x, df, dictionnaire, form_name, limit):
    # print(x)
    # print('type')
    # print(df.dtypes[x])
    if (x != ''):
        col_type = ''
        col_vals = ''
        col_min = ''
        col_max = ''
        col_avg = ''
        col_name_source = x
        q1, q2, q3 = '', '', ''
        n_unknown = 0
        n_na = 0
        n_empty = 0
        col_missing = df[x].isna().sum()
        try:
            n_empty = df[x].str.lower().isin(['']).sum()
            col_missing = col_missing + n_empty
        except:
            pass
        try:
            n_unknown = df[x].str.lower().isin(['unknown', 'unk', 'uk']).sum()
        except:
            pass
        try:
            n_na = df[x].str.lower().isin(['N/A', '<NA>', 'na']).sum()
        except:
            pass
        # n_na = df[x].str.lower().isin(['N/A', '<NA>','na']).sum()

        #     col_missing.append(f'{n_nans} ({n_nans*100/len(df):.0f}%)')

        missing_rate = round(col_missing / len(df), 2)
        total = len(df)
        if (col_missing == total):
            col_type = 'Empty'
        else:
            try:
                # in case column is date
                df[x] = pd.to_datetime(df[x], format="%d/%m/%Y")
                col_type = 'Date'
                col_max = df[x].max()
                col_min = df[x].min()
            except ValueError:
                # Check if column can vbe integer
                try:
                    df[x] = df[x].astype('int')
                    col_type = 'Integer'
                    q1, q2, q3 = df[x].quantile(.25), df[x].quantile(.5), df[x].quantile(.75)
                    col_max = df[x].max()
                    col_min = df[x].min()
                    col_avg = df[x].mean()
                except:
                    # Check if column can be float
                    try:
                        df[x] = df[x].astype('float')
                        col_type = 'Float'
                        q1, q2, q3 = df[x].quantile(.25), df[x].quantile(.5), df[x].quantile(.75)
                        col_max=df[x].max()
                        col_min = df[x].min()
                        col_avg=df[x].mean()

                    except:
                        if df.dtypes[x] in ([np.dtype('object')], 'str', 'string', 'object'):
                            if df[x].nunique() > limit:
                                col_type = 'unstructured value'
                                col_vals = 'list of value is more than ' + str(limit)
                            else:
                                col_type = 'Category'
                                df[x] = df[x].astype(str)
                                #             col_vals.append('to create the list')
                                list_sous_menu = []
                                for k, v in df[x].value_counts().sort_index().to_dict().items():
                                    if (k != 'nan'):
                                        if (k == ''):
                                            k = 'Empty'
                                        pourcentage = round(v * 100 / len(df), 1)
                                        string_val = str(k + ' : ' + str(pourcentage) + '%' + ' (' + str(v) + ')')
                                        list_sous_menu.append(string_val)
                                col_vals = " <br> ".join(list_sous_menu)

        new_row = {'Variable': col_name_source,
                   'Form Name': form_name,
                   'Total (records)': total,
                   'Nb of Unknown': n_unknown,
                   'Nb of na': n_na,
                   'Number of Empty': col_missing,
                   'Missing rate': missing_rate,
                   'Col Type': col_type,
                   'Values collected': col_vals,
                   'col_min': col_min,
                   'col_max': col_max,
                   'col_avg': col_avg,
                   'quantile 25': q1,
                   'quantile 50': q2,
                   'quantile 75': q3}
        #    dictionnaire = dictionnaire.append(new_row)

        try:
            dictionnaire = pd.concat([dictionnaire, pd.DataFrame([new_row])], ignore_index=True)

        # dictionnaire = dictionnaire.append(new_row, ignore_index=True)
        # dictionnaire=dictionnaire.append(col_name,total,missing_rate,col_missing,col_type,col_vals,col_min,col_max,col_avg,col_perc)
        except:
            pass

    return dictionnaire


#Load your DatasEt in a DATA FRAME
file_loc='/Users/hfaour/Downloads/fake_dataset.csv'
df = pd.read_csv(file_loc, sep=';', keep_default_na=False, na_values=['_'])

#give a name to your Form Name ex: Patient, Treatment , Lab
#Use the the name of the sheet or the data collection form name
form_name='test_data'

#Give a limit to detect distinct values for string or object
#Example if the limit = 20 :  more than 20 distinct value the column  will be considered unstrubctured Data
limit_distinct=20
'''' 
    to use the Description funnction pass the 3 parameters
    form_name: Name of the Form 
    df: The Dataframe loaded 
    Limit : 
'''
desc=generate_data_description(form_name, df, 20)


desc.to_html('test_hassan.html')
