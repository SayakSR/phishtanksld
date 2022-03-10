__status__ = "dev"
import sys 
import os
import pandas as pd
import requests 
from bs4 import BeautifulSoup as bs
from datetime import datetime
from utils.phishtank_utils import get_verifiers_and_if_phish_is_valid

# define functions.
def get_time_difference(start_dt,end_dt) -> float:
    try:
        start_datetime = datetime.strptime(str(start_dt),'%Y-%m-%dT%H:%M:%S+00:00')
        end_datetime = datetime.strptime(str(end_dt),'%Y-%m-%dT%H:%M:%S+00:00')
        
        time_difference = end_datetime-start_datetime # timedelta object.
        return float(abs(time_difference.total_seconds())) # return time difference.
    except ValueError as ve:
        print(ve+"\n\n")
        print("Date format must be in : '%Y-%m-%dT%H:%M:%S+00:00'     \n" )
        return float(-99999)

def add_column_to_dataframe(dataframe, column, column_header):
    dataframe[column_header] = column
    return dataframe

def process_args():

    try:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
    except:
        print("Warning! No agruments entered, reverting to defaults")
        start = 0
        end = 0

    return start, end

def if_url_already_in_database(url_tracker_file,url):
    urls = [] 
    f = open(url_tracker_file,"r")
    for line in f:
        urls.append(line.strip('\n'))
    if(url.strip('\n') in urls):
        return True 
    else:
        return False 

def write_base_data_to_csv(data,path):

    print("Writing data to [{}]... \n".format(path), end="")

    if(os.path.exists(path)):
        pass
    else: # create csv with headers. 
        f = open(path,"w")
        f.write("PhishID"+","+"URL"+","+"Phish_Detail_URL"+","+"Date_Submitted"+","+"Submitter"+","+"Is_online")
        f.close()

    # read the csv file in dataframe. 
    df = pd.read_csv(path)
   
    for item in data:
        print(item)
        
        df = df.append(
            {
                "PhishID":item['phish_id'],
                "URL":item['url'],
                "Phish_Detail_URL":item['phish_detail_url'],
                "Date_Submitted":item['date'],
                "Submitter":item['submitter'],
                "Is_online":item['Is_online'],
            },ignore_index=True,sort=False
            
        )
        
    df.to_csv(path,index = False)

def extract_column_of_csv_to_list(file,column):
    df = pd.read_csv(file,usecols=[column])
    phish_detail_urls = [] 
    for index, row in df.iterrows():
        phish_detail_urls.append(row[column])
    return phish_detail_urls

def add_verifier_info_from_soup(file):
    df = pd.read_csv(file)
    phish_detail_urls = [] 
    verifiers_list=[]
    is_valid_list=[]
    print(df)
    for index, row in df.iterrows():
        response = requests.get(row["Phish_Detail_URL"])
        import time
        time.sleep(0.5)
        if response.status_code == 200: # 200 response 
            print("200 OK")
            soup = bs(response.content, "html.parser") # create a soup of html response. 
            verifiers,is_valid = get_verifiers_and_if_phish_is_valid(soup)
            verifiers_list.append(verifiers)
            is_valid_list.append(is_valid)
        else:
            print("HTTP error")
            #print(verifiers_list)
            #print(is_valid_list)
        
    dataframe_after_adding_verifiers = add_column_to_dataframe(df,verifiers_list,"verifiers")
    dataframe_after_adding_is_valid = add_column_to_dataframe(dataframe_after_adding_verifiers,is_valid_list,"is_valid")
    
    dataframe_after_adding_is_valid.to_csv(file,index=False)
    print("Verifiers added...")
















    

