
from pkgs.phisherman import Phisherman
from utils.base_utils import write_base_data_to_csv,add_verifier_info_from_soup,process_args
import time,json 
import threading 

interval = 1800 # 30 min interval.
day_interval = 36200 # change it to 24 hours later. 
count = day_interval/interval +1

"""
    get new URLs from phishtank every 30 mins. 
    get Vtotal reports at the end of the day.  -- for now. 
    get verifiers reports at the end of the day. 
"""
"""
    base_data: URL, Date_Submitted, Submitter, PhishID, Submitter, Domain
    verifier_data: verifiers, is_phish_valid
    vtotal_data: vtotal_score, vtotal_engines
    url_status_data: is_online
"""

def get_base_data(url_tracker_file):
    print("Getting data from phishtank...\n")
    time.sleep(1)
    start, end = process_args()
    phisherman = Phisherman(start, end,url_tracker_file)
    return phisherman.crawl()

if __name__ =="__main__":

    # open config file
    config_file = open('config.json')
    config_data = json.load(config_file)

    # get configurations from config file. 
    url_tracker_file = config_data["url_tracker"]
    base_data_file = config_data["base_data_collection"]
    phish_detail_url_from_base_data_file = config_data["phish_detail_column_name"]
    phish_id_from_base_data_file = config_data["URL_ID_column_name"]
    f = open(url_tracker_file,"w")
    f.close() 
    

    counter = 0
    while(True): # collect URL forever. 
        counter+=1 
        base_data = get_base_data(url_tracker_file)
        if(len(base_data)>0):
            write_base_data_to_csv(base_data,base_data_file)
        else:
            print("No new data to write.\n")

        if(counter == count ): # one day. 
            print("\nGetting verification report for the day...")
            t1 = threading.Thread(target=add_verifier_info_from_soup,name='t1',args=(base_data_file,))
            t1.start()
            #add_verifier_info_from_soup(base_data_file)

            #print("\nRunning virustotal module in thread...")
        print("\nSleeping "+str(interval)+" seconds...")
        time.sleep(interval) # sleep for 30 mins.
        t1.join()

