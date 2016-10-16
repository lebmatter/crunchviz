import csv
from macpath import split
import pandas as pd
import json
from geocoder import google
import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
print SITE_ROOT
acq_file = os.path.join(SITE_ROOT, 'static\\base_data\\acquisitions.csv')
com_file = os.path.join(SITE_ROOT, 'static\\base_data\\companies.csv')
inv_latest_file = os.path.join(SITE_ROOT, 'static\\base_data\\investments_latest.csv')

def get_category(csv_file):
    df = pd.read_csv(csv_file)
    saved_column = df['company_category_list']  # you can also use df['column_name']
    category = set([])
    for each in saved_column:
        each = str(each)
        values = each.split('|')
        for val in values:
            category.add(val)
    return category


def aggregate_acquisitions_based_on_category(csv_file,categoryName):
    df = pd.read_csv(csv_file,
                      usecols=["company_name", "company_category_list", "company_city"],
                      header=0)
    df=df.dropna(how='any')
    df = df[df['company_category_list'].str.contains(categoryName)]
    df = df.groupby('company_city').size()
    #print df
    return df

def aggregate_companies_based_on_category(csv_file,categoryName):
    df = pd.read_csv(csv_file,
                      usecols=["name", "category_list", "region"],
                      header=0)
    df=df.dropna(how='any')
    df = df[df['category_list'].str.contains(categoryName)]
    df = df.groupby('region').size()
    #print df
    return df


def read_csv(csvFile):
    with open(csvFile, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in csvreader:
            if csvreader.line_num != 1:
                print ', '.join(row)
    pass
def getRate(aqCount,compCount):
    if not 0 in (aqCount,compCount):
        return int((aqCount/float(compCount))*100)
    else:
        return 1
def get_city_wise_acquisition_rate_of_a_category(categoryName):
    print "calculating"
    import os.path
    aqDf = aggregate_acquisitions_based_on_category(
        acq_file, categoryName)
    compDf = aggregate_companies_based_on_category(
        com_file, categoryName)
    aqDict = dict(aqDf)
    compDict = dict(compDf)
    dictRate = {}
    for city in compDict:
        print city
        if aqDict.has_key(city):
            dictRate[city]= {}
            dictRate[city]['acquisitions'] = str(aqDict[city])
            dictRate[city]['total'] = str(compDict[city])
            dictRate[city]['health']= str(getRate(aqDict[city],compDict[city]))
            coordinates = google(city, key="AIzaSyDTodiKfrl8BWjpGCVdAR72VunifJQPtcI")
            dictRate[city]['coord']= coordinates.latlng
        else:
            dictRate[city]= {}
            dictRate[city]['acquisitions'] = '0'
            dictRate[city]['total'] = str(compDict[city])
            dictRate[city]['health']= '1'
            coordinates = google(city, key="AIzaSyDTodiKfrl8BWjpGCVdAR72VunifJQPtcI")
            dictRate[city]['coord']= coordinates.latlng


    return json.dumps(dictRate)


def get_company_list_based_on_catagoty_range_series(categoryName,range,ventureType):
    csv_file_investment = inv_latest_file
    csv_file_company = com_file
    df = pd.read_csv(csv_file_investment,
                     usecols=["company_name",
                     "company_category_list",
                     "company_city",
                     "raised_amount_usd",
                     "funding_round_code",
                     "funding_round_type",
                     "funded_at", "company_country_code"],
                     header=0)
    df = df.dropna(how='any')#series has to be omitted here
    df = df[df['company_category_list'].str.contains(categoryName, case=False)]
    #df = df[df['funding_round_code'].str.contains(series)]
    df = df[df['raised_amount_usd'] > range]
    df = df[df['funding_round_type'].str.contains(ventureType)]

    df2 = pd.read_csv(csv_file_company,usecols=['name', 'founded_at'],
                     header=0)
    df2 = df2.rename(columns={'name': 'company_name'})
    df3 = pd.merge(df,df2,on='company_name')
    df3 = df3.dropna(how='any')
    dict3 = df3.to_json()
    return dict3

def main():
    #get_category('C:\\Users\\sabeer_k\\Desktop\\DataHAck\\DataHack2K16\\base_data\\acquisitions.csv')companies
    #aggregate_based_on_category('C:\\Users\\sabeer_k\\Desktop\\DataHAck\\DataHack2K16\\base_data\\acquisitions.csv','E-Commerce')
    #aqDf=aggregate_acquisitions_based_on_category('C:\\Users\\sabeer_k\\Desktop\\DataHAck\\DataHack2K16\\base_data\\acquisitions.csv','E-Commerce')
    #compDf=aggregate_companies_based_on_category('C:\\Users\\sabeer_k\\Desktop\\DataHAck\\DataHack2K16\\base_data\\companies.csv','E-Commerce')
    get_city_wise_acquisition_rate_of_a_category('E-Commerce')
    pass
if __name__ == '__main__':
    main()