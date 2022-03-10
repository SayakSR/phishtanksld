__status__ = "dev"

# dependencies: 
from urllib.error import HTTPError
import requests


# start function declarations
def scan_urls(url,key):

    # Virustotal API endpoint. 
    URL_ = 'https://www.virustotal.com/vtapi/v2/url/scan'
    #key = '659148aa9d211ce114a89ca8d11c94445c18181718a71915243a0fdd5d973268'

    params = {'apikey': key, 'url': url}  # params.
    print("Scanning URL: "+url)

    try:
        resp = requests.post(URL_, data=params)
        print(resp)
    except Exception as e:
        print(e)

def get_reports(url,key):
    
    # Virustotal API endpoint. 
    URL_r = 'https://www.virustotal.com/vtapi/v2/url/report'  # to get report.
    #key = '659148aa9d211ce114a89ca8d11c94445c18181718a71915243a0fdd5d973268'
   
    threat_count = -1  # initiate to -1 
    params = {'apikey': key, 'resource': url}  # params.

    print("Getting vtotal report for: "+url)


    try:
        resp = requests.get(URL_r, params=params)
        response = resp.json()  # getting the scan report.
    except ConnectionError as CE:
        print("Connection Error... Trying again.")
        print (CE) 
    except TimeoutError as TE:
        print("Timeout Error... Trying again.")
        print(TE)
    except HTTPError as HE:
        print("HTTP Error... Trying again.")
        print(HE)

    try:
        threat_count = response['positives']  # get the detection number.
    except Exception as e:
        print("Error occured while parsing JSON vtotal response. ")
        print(e)

        # get the engines that detected URL as malicious.
        try:
            scan_details = str(response['scans'])
            scan_details_dict = eval(scan_details)  # convert to dictionary.
            detecting_engines = ''

            for item in scan_details_dict:
                y = scan_details_dict[item]

                for key, v in y.items():  # key is engine name,
                    if (key == 'detected'):
                        value = y[key]
                        if value == True:
                            detecting_engines = detecting_engines + item + ', '
        except:
            detecting_engines = 'ERROR'
        if(threat_count == 0):
            detecting_engines = 'NONE'

    return threat_count, detecting_engines

    