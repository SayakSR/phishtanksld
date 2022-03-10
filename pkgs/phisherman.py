import requests
from bs4 import BeautifulSoup as bs
import time
from utils.phishtank_utils import get_submitter_from_soup
from utils.check_active import check_url
from utils.base_utils import if_url_already_in_database

class Phisherman:
    def __init__(self, start, end, filename):
        self.__start = start
        self.__end = end
        self.__filename = filename
        self.__success = 0
    
    def __get_start(self):
        return self.__start

    def __set_start(self, start):
        self.__start = start

    def __get_end(self):
        return self.__end

    def __set_end(self, end):
        self.__end = end

    def __get_filename(self):
        return self.__filename

    def __set_filename(self,filename):
        self.__filename = filename

    def __make_page_url(self, page): 
        url_ = "https://www.phishtank.com/phish_archive.php?page={}".format(page)    
        return url_.format(page)

    def __make_detail_page_url(self, url_id):
        return "https://www.phishtank.com/phish_detail.php?\
            phish_id={}".format(url_id)

    def __get_ids(self, page):
        """This just gets the PHISH IDs from first page"""
        print("Gathering links from page [{}]... ".format(page), end="")
        response = requests.get(self.__make_page_url(page))
        
        if response.status_code == 200:
            soup = bs(response.content, "html.parser")
            
            elements = soup.select(".value:first-child > a")
            url_ids = [element.text for element in elements]
            print("Successfully retrieved IDs.")
            return url_ids
        else:
            print("Error! Could not get IDs.")
            return None

    def __get_data(self, url_id):

        print("Gathering data for url [id={}]... ".format(url_id), end="")

        phish_detail_page = self.__make_detail_page_url(url_id)
        response = requests.get(phish_detail_page)
        if response.status_code == 200: # 200 response 
            soup = bs(response.content, "html.parser") # create a soup of html response. 

            phish_url = soup.select_one(".padded > div:nth-child(4) > \
                span:nth-child(1) > b:nth-child(1)").text
            date = self.__parse_date_string(soup.select_one(".small").text)
            submitter = get_submitter_from_soup(soup)
            is_online = check_url(phish_url)
            self.__success += 1
            print("Successfully grabbed URL from Phishtank. \n")
            return {"url": phish_url, "date": date, "phish_id":url_id, "submitter":submitter,"phish_detail_url":phish_detail_page,"Is_online":is_online}
        else:   
            print("Did not get 200 Response, skipping... \n") 
            time.sleep(2)
            return None

    def __parse_date_string(self, date_str):
        return " ".join(date_str.split()[1:6])

    def crawl(self):
        print("Crawler started...Phisherman is gathering data... ")
        url_ids = []
        data = []
        
        for page in range(self.start, self.end + 1):
            result = self.__get_ids(page)
            
            if result:
    
                url_ids += result

        for url_id in url_ids:
            if(if_url_already_in_database("url_seen_list.txt",url_id)):
                pass
                print("Skip url"+url_id)
            else:
                result = self.__get_data(url_id)
                f = open("url_seen_list.txt",'a')
                f.write(url_id)
                f.write('\n')

                if result:
                    data.append(result)

        print("Crawling complete! Successfully gathered {} urls\n".format(
            self.__success))
        return data
    start = property(__get_start, __set_start)
    end = property(__get_end, __set_end)
