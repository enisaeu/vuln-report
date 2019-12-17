from itertools import chain
import pandas as pd
import numpy as np

CWE = pd.read_csv('../data/offline_data/cwe.csv')
TECH = pd.read_csv('../data/offline_data/techniques.csv', encoding ='latin1')
CAPEC = pd.read_csv('../data/offline_data/capec_2.csv', encoding ='latin1')

# return list from series of comma-separated strings
def chainer(s):
    return list(chain.from_iterable(s.str.split(',')))

def tidy_split(df, column, sep='|', keep=False):
    """
    Split the values of a column and expand so the new DataFrame has one split
    value per row. Filters rows where the column is missing.

    Params
    ------
    df : pandas.DataFrame
        dataframe with the column to split and expand
    column : str
        the column to split and expand
    sep : str
        the string used to split the column's values
    keep : bool
        whether to retain the presplit value as it's own row

    Returns
    -------
    pandas.DataFrame
        Returns a dataframe with the same columns as `df`.
    """
    indexes = list()
    new_values = list()
    df = df.dropna(subset=[column])
    for i, presplit in enumerate(df[column].astype(str)):
        values = presplit.split(sep)
        if keep and len(values) > 1:
            indexes.append(i)
            new_values.append(presplit)
        for value in values:
            indexes.append(i)
            new_values.append(value)
    new_df = df.iloc[indexes, :].copy()
    new_df[column] = new_values
    new_df[column] = new_df[column].str.strip()
    return new_df


def get_name_by_cwe(cweid):
    try:
        return CWE.Name[CWE['CWE-ID']==int(cweid)].iloc[0]
    except:
        return cweid

    
def get_name_by_capec(capecid):
	try:
		return CAPEC.Name[CAPEC['id']==int(capecid)].iloc[0]
	except:
		return capecid
    
def get_name_by_tech(techid):
    try:
        return TECH.name[TECH['attack_id']=='T'+str(techid)].iloc[0]
    except:
        return techid


#gets a product as an input and returns the num top weaknesses
def product_weaknesses(product, data, num):
	pdata = data[data['product'] == product]
	top10_cwe = pdata.cwe.groupby(pdata.cwe).count().sort_values(ascending=False).head(num)
	top10_cwe=top10_cwe.to_frame()
	top10_cwe.columns=['c']
	top10_cwe.reset_index(level=0, inplace=True)
	top10_cwe.columns=['cwe','c']

	return top10_cwe

#gets a product as an input and returns the top10 weaknesses's names
def get_cwes_by_vendor(data, vendor):
	vdata =data[data['vendor'] == vendor]
	vdata['Name']=vdata['cwe'].map(get_name_by_cwe)
	cwe_v = vdata.groupby('Name')['Name'].count().sort_values().tail(10)
	cwe_v = cwe_v.to_frame()
	cwe_v.columns = ['count']

	return cwe_v

def wrap(s, n=40):
    """
    A simple text wrapping function. If a string has length >40 (default), 
    it is split to two lines with a break inserted around the middle
    
    """
    ss=s
    if len(s)>n:
        i=int(len(s)/2)
        l=(s.find(' ',i))
        ss=s[:l]+'<br>'+ss[l+1:]
    return ss

