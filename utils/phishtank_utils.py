__status__ = "dev"

from bs4 import BeautifulSoup as bs
import xmltodict
import base64
import requests
import json 

# Define Header for Phishtank API.
headers = {
        'format': 'json',
        'app_key': '25807792c8a233a7bd552369cbee05d469608451334c58123082f022028ee3c7',
        }

# Define Functions: 
def get_submitter_from_soup(soup):
    try:
        submitter = "" 
        # find the username who submitted phish. 
        for link in soup. find_all('a'):
            if ("user.php?username=" in str(link)):
                username = str(link)
                start = username.find("username=")+9
                end = username.find(">")
                submitter = (username[start:end-1])
                break
    except:
        submitter = "ERROR"
    return submitter


def get_verifiers_and_if_phish_is_valid(soup):    
    try:
        phish_details_header = soup.find("table", {"class": "phish-detail"})
        verifiers=[]
        is_valid = False 
        header_info = (phish_details_header.find("h3", text=""))
        if("Sign in" not in str(header_info) and "Voting disabled" not in str(header_info)): # The phish is  verified. 
            is_valid = True
            for link in phish_details_header.find_all('a'):
                if ("user.php?username=" in str(link)):
                    username = str(link)
                    start = username.find("username=")+9
                    end = username.find(">")
                    user = (username[start:end-1])
                    verifiers.append(user) 
        
        return str(verifiers),str(is_valid)
    except:
        return "ERROR", "ERROR"

def get_url_with_ip(URI):
    """Returns url with added URI for request"""
    url = "http://checkurl.phishtank.com/checkurl/"
    new_check_bytes = URI.encode()
    base64_bytes = base64.b64encode(new_check_bytes)
    base64_new_check = base64_bytes.decode('ascii')
    url += base64_new_check
    return url

def send_the_request_to_phish_tank(url, headers):
    """This function sends a request."""
    response = requests.request("POST", url=url, headers=headers)
    return response


def get_verification_details(URL,verifiers):
    url = get_url_with_ip(URL)
    r = requests.request("POST",url = url, headers=headers)    
    if(r.status_code == 200):
        data = json.loads(json.dumps(xmltodict.parse(r.text)))   
        try:
            is_in_database=data['response']['results']['url0']['in_database']# Checks if URL in database
        except UnboundLocalError:
            is_in_database = "ERROR"
        try:
            is_verified=data['response']['results']['url0']['verified'] # Checks if URL is verified
        except UnboundLocalError as ube:
            if(len(verifiers>1)):
                is_verified = True 
            else:
                is_verified = False 
        #phish_id=data['response']['results']['url0']['phish_id']# Checks if URL in database

        if(is_verified=='true'):
            verified_time=data['response']['results']['url0']['verified_at'] # Checks at what time URL is verified
            is_valid=data['response']['results']['url0']['valid'] # Checks if URL is valid i.e. valid phishing
        else:
            verified_time = None
            is_valid = None 
         
    else :
        is_verified = "Error "+str(r.status_code)
        is_in_database = "Error "+str(r.status_code)
        is_valid = "Erorr "+str(r.status_code)
        verified_time = "Error "+str(r.status_code)
        print("Error while getting verification details: "+str(r.status_code))
    return [is_verified,is_in_database,verified_time]

       

            