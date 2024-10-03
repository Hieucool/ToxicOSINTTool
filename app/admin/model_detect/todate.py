from datetime import datetime
import re

timeformat = {
    "%d/%m/%Y" : "\d{1,2}\/\d{1,2}\/\d{4}",  # "13/8/2024"
    "%b %d, %Y" : r"\w{3} \d{1,2}, \d{4}",  # "Sep 22, 2019"
    "%Y-%m-%d" : r"\d{4}-\d{2}-\d{2}",  # "2024-04-30"
    "%d %b %Y":  r"\d{1,2} \w{3} \d{4}",   # "02 May 2024",
    "%d %b %y": r"\d{1,2} \w{3} \d{2}" ,         # "03 May 24"
}


def todatetime(time_string):
    temp_string = ""
    for key, value in timeformat.items():
        match = re.search(value, time_string)
        if match:
            temp_string = match.group(0)
            datetime_object = datetime.strptime(temp_string, key)
            return datetime_object
            
    return None


# # Example usage:
# time_string = "13/8/2024"
# print(todatetime(time_string))

# time_string = "Sep 22, 2019,23,5,44"
# print(todatetime(time_string))

# time_string = "2023-02-08 00:00:00"
# print(todatetime(time_string))


time_bao = {
    "dantri.com.vn": "time.author-time",
    "cand.com.vn" : "div.box-date",
    "vnexpress.net" : "span.date",
    "bbc.com": "time.bbc-j3wi5n e1mklfmt0"
}
def getDomain(url):
    split_url = url.split('/')
    return split_url[2]

from bs4 import BeautifulSoup
import requests

def extract_time(url):
    domain = getDomain(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    if(domain in time_bao):
        temp = time_bao[domain].split(".")
        name_item, name_class = temp[0], temp[1]
        
        time_str = soup.find(name_item, class_=name_class).text
        if(time_str):
            print(time_str)
            val_date = todatetime(time_str)
            return val_date
    else:
        return None

# url = 'https://vnexpress.net/loat-du-an-o-tp-hcm-se-khoi-dong-nho-co-che-moi-4625260.html'

# print(extract_time(url))
