import re
import json
import validators
from newspaper import Article as BaiBao
from bs4 import BeautifulSoup
from .todate import *
from ..model_detectfakenews import detect_content,check_blacklist
from ..handle import *
from ..tomtatvanban import Summerizer
import datetime
from ..clustering.cluster_article import PhanCum

def is_url(url):
    return validators.url(url)

def clean_json(text):
    text = text.replace('"', '\\"').replace("\n"," ").replace("\t"," ").replace("\r"," ")
    text = re.sub(r'\s+', ' ', text)
    return text




# Function to extract the domain from a URL
def getDomain(url):
    split_url = url.split('/')
    return split_url[2]



import requests
from bs4 import BeautifulSoup, NavigableString
from fake_useragent import UserAgent

def crawler_viettan(url):
    ua = UserAgent()
    
    if("amp" not in url):
        url += "/amp"
        
    # url= "https://viettan.org/thu-di-tim-duong-cuu-nuoc/"
    while(True):
        try:
            headers = {
                'User-Agent': ua.random,
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            }
            response = requests.get(url, headers=headers)
            # print(response.status_code)
            code = response.status_code
            if(str(code) == "200"):
                break
        except :
            pass

    soup = BeautifulSoup(response.content, "html.parser")
    
        
    # with open("output.html", "w", encoding="utf-8") as f:
    #     f.write(str(soup))
    
    title = soup.find("h1", class_="amp-wp-title").text
    author = soup.find("div",class_="author").text.strip()
    art_time = soup.find("meta",{'property': 'article:published_time'})['content'].strip()
    try:
        image = soup.find("amp-img",class_="attachment-large")['src']
    except:
        image = ""
    content = soup.find("div",class_="amp-wp-article-content").text.strip()

            
    result = {
                'url': url,
                'title': title,
                'author': author,
                'category_id': 4,
                'keywords': "",
                "created_at": todatetime(art_time),
                "image_url": image,
                'content': content,
                'summerize': Summerizer(content,3)
            }
    print(result)
    return result


def start_crawl(url):
    checkexist = checkExist(url)
    if(checkexist is None):
        print("here")
        domain = getDomain(url)
        
        if not is_url(url):
            result = {
                'url': url,
                'error': 'Url không hợp lệ!',
                'success': False
            }

            return result

        result = {}
        if("viettan.org" in domain):
            print("detect viettan ", url)
            result =  crawler_viettan(url)
        else:
            print("detect bai viet thuong ", url)
            
            while(1):
                try:
                    article = BaiBao(url)
                    article.download()
                    article.parse()
                    if(article):
                        break
                except:
                    pass
            print("access 200")
            content = article.text
            
            if(content == ""):
                content = re.sub('\\n+', '</p><p>', '<p>' + clean_json(content) + '</p>')

            # tom tat van ban 
            content_sum = Summerizer(content,2)
            print(article.publish_date)
            # lay thoi gian dang bai
            pub_date = todatetime(str(article.publish_date) if article.publish_date else str(article.meta_data.get('pubdate', '')))
            if(pub_date is None):
                pub_date = extract_time(url)
                if(pub_date is None):
                    pub_date = datetime.now()
                    print("laytam now", pub_date)
                    
            result = {
                        'url': url,
                        'error': '',
                        'success': True,
                        'title': article.title,
                        'keywords': article.keywords if article.keywords else (
                            article.meta_keywords if article.meta_keywords else article.meta_data.get('keywords', [])),
                        "created_at": pub_date,
                        "image_url": article.top_image,
                        'content': content,
                        'summerize' : content_sum
                    }
        
        # them bai bao moi vao csdl
        
        result_isfake = detect_content(result["content"])
       

        data = {
                "title" : result["title"],
                "url" : result["url"],
                "image_url" : result["image_url"],
                "author" : "",
                "category_id": 1,
                "content" : result["content"],
                "summerize" : result["summerize"],
                "created_at" : result["created_at"],
                "sentiment" : "",
                "is_fake" : result_isfake
            }

        isInBlacklist = False
        if(check_blacklist(domain)):
            data["is_fake"] = True
            isInBlacklist= True
            
        
        # INSERT bài báo vào CSDL
        
        print(data)
        item_id = InsertArticle(data).id
        print("them bai bao", item_id)
        
        # them keyword
        print("them keyword")
        for key in result['keywords']:
            temp = key.lower().strip()
            ret = add_keyword_to_article(item_id, temp)
            print(f"{temp} => {ret}")
        
        if result_isfake or isInBlacklist:
            data['predicted_label'] = "Danger news"
        else : data['predicted_label']  = 'Safe news'
        data['keywords'] = result['keywords']
        return data
        
    else:
        data = {}
        data['title'] = checkexist.title
        data['is_fake'] = checkexist.is_fake
        data['author'] = checkexist.author
        data['image_url'] = checkexist.image_url
        data['created_at'] = checkexist.created_at
        data['summerize'] = checkexist.summerize
        data['content'] = checkexist.content
        data['keywords'] = [keyword.name for keyword in checkexist.keywords]

        if data['is_fake'] :
            data['predicted_label'] = "Danger news"
        else : data['predicted_label']  = 'Safe news'
        
        return data
    



def crawl_bbcnews(url):
    ua = UserAgent()

    while(True):
        try:
            headers = {
                'User-Agent': ua.random,
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            }
            response = requests.get(url, headers=headers)
            print(response.status_code)
            code = response.status_code
            if(str(code) == "200"):
                break
        except :
            pass


    soup = BeautifulSoup(response.content, "html.parser")
    with open("output.html", "w", encoding="utf-8") as f:
            f.write(str(soup))

    title = soup.find("h1", class_ = "bbc-e0ctyc e1p3vdyi0").text
    pub_time = soup.find("div", class_ = "bbc-19j92fr ebmt73l0").find("time")['datetime']
    tag_p = soup.find_all("p", class_ = "bbc-1y32vyc e17g058b0")
    top_img = soup.find("div", class_ = "bbc-j1srjl").find("img")['src']
    # author  = soup.find("span", class_ = "bbc-18ttg5u").text

    content = ""
    for pitem in tag_p:
        content += pitem.text

    data = {
        "title" : title,
        "url" : url,
        "image_url" : top_img,
        "author" : "phandong",
        "category_id": 1,
        "created_at": todatetime(pub_time),
        "content" : content,
        "summerize" : Summerizer(content,3),
        "is_fake" : True
    }

    return data

def crawl_vnexpress(url):
    article = BaiBao(url)
    article.download()
    article.parse()

    content = article.text
    headline = article.title
    url = article.url
    top_img = article.top_img
    

    data = {
        "title" : headline,
        "url" : url,
        "image_url" : top_img,
        "author" : "vnexpress",
        "content" : content,
        "category_id": 1,
        "created_at": extract_time(url),
        "summerize" : Summerizer(content,3),
        "is_fake" : detect_content(content)
    }
    print(data)
    
    return data


def crawl_unoffical():
    ua = UserAgent()
    

    url= "https://www.bbc.com/vietnamese/topics/ckdxnx1x5rnt?page="
    data = []
    count = 0
    for i in range(1,4):
        
        tempurl = url+ str(i)
        print("page = ", tempurl)
        while(True):
            try:
                headers = {
                    'User-Agent': ua.random,
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive'
                }
                response = requests.get(tempurl, headers=headers)
                print(response.status_code)
                code = response.status_code
                if(str(code) == "200"):
                    break
            except :
                pass
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        with open("output.html", "w", encoding="utf-8") as f:
            f.write(str(soup))

        all_art = soup.find_all("li", class_="bbc-t44f9r")
        
        for item in all_art:
            item_t = item.find("a")
            title = item_t.text
            url_item = item_t['href']
            if("articles" in url_item):
                print("Đang cào ", title, url_item)
                #neu ton tai roi -> thoi ko cao
                checkexist = checkExist(url_item)
                if(checkexist is not None):
                    temp_data  = crawl_bbcnews(url_item)
                    item_new = InsertArticle(temp_data)
                    print("Insert new acticle ", item_new)
                    data.append(item_new)
                    
                else:
                    temp_data = checkexist
                    data.append(temp_data)
                
                print(count)
                count += 1
                
                # if(count > 10):
                #     break
        
    return data
    
    

def cluster_data(data):
    crawl_unoffical()
    result = PhanCum(data)
    return result


def crawl_offical():
    ua = UserAgent()
    

    data = []
    url = "https://vnexpress.net/thoi-su/chinh-tri-p"
    
    count = 0
    for i in range(1,4):
        tempurl = url + str(i)
        print(f"---------------------------------Page {i}")
        
        while(True):
            try:
                headers = {
                    'User-Agent': ua.random,
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive'
                }
                response = requests.get(tempurl, headers=headers)
                code = response.status_code
                print(tempurl, code)
                if(str(code) == "200"):
                    break
            except :
                pass


        content = response.content

        soup = BeautifulSoup(content, "html.parser")

        # with open("output.html", "w", encoding="utf-8") as f:
        #         f.write(str(soup))
                
        all_art = soup.find_all("article", class_="item-news thumb-left item-news-common")
        
        for item in all_art:
            class_title = item.find("h2", class_="title-news")
            title = class_title.text
            url_item = class_title.find("a")['href']
            print("Đang cào ", title, url_item)
        
            checkexist = checkExist(url_item)
            if(checkexist is None):
                temp_data  = crawl_vnexpress(url_item)
                item_new = InsertArticle(temp_data)
                print("Insert new acticle ", item_new)
                data.append(item_new)
                
            else:
                temp_data = checkexist
                data.append(temp_data)
            
            print(count)
            count += 1
        
    if(len(data) > 0):
        result = PhanCum(data)
    else:
        result = None
    return result


def crawl_rss(url , cate_id):
    response = requests.get(url)
    print(response.status_code)
    content = response.content

    soup = BeautifulSoup(content, "html.parser")

    with open("output.html", "w", encoding="utf-8") as f:
            f.write(str(soup))
            
    all_art = soup.find_all("item")
    data = []
    for item in all_art:
        # item = all_art[0]
        title = item.find("title").text.strip()
        pub_time = item.find("pubdate").text.strip()
        print("time =>", pub_time)
        temp = BeautifulSoup(item.find("description").text, "html.parser")
        temp_url = temp.find('a')['href']
        description = temp.text.strip()
        top_img = temp.find('img')['src']

        temp_data = {
            "title" : title,
            "url" : temp_url,
            "image_url" : top_img,
            "author" : "",
            "category_id": cate_id,
            "created_at": todatetime(pub_time),
            "content" : description,
            "is_fake" : False
        }
        
                
        new_data = crawl_content_rss(temp_data)
        
        data.append(new_data)
    
    return data



def crawl_content_rss(data):
    checkexist = checkExist(data["url"])
    if(checkexist is None):
        domain = getDomain(data["url"])         
        n = 0
        while(1):
            try:
                article = BaiBao(data["url"])
                article.download()
                article.parse()
                n+=1
                if(article ):
                    break
                if(n > 10):
                    return {}
            except:
                pass

        content = article.text
        title = article.title
        
        if(content == ""):
            content = re.sub('\\n+', '</p><p>', '<p>' + clean_json(content) + '</p>')

        # tom tat van ban 
        content_sum = Summerizer(content,2)
        
        data["title"] = title
        data["content"] = content
        data["summerize"] = content_sum
        # them bai bao moi vao csdl
        
        data["is_fake"] = detect_content(data["content"])
     

        if(check_blacklist(domain)):
            data["is_fake"] = True
        
        # INSERT bài báo vào CSDL
        
        print(data)
        item_id = InsertArticle(data).id
        print("them bai bao", item_id)
        
        # them keyword
        print("them keyword")
        keyword =  article.keywords if article.keywords else article.meta_keywords if article.meta_keywords else article.meta_data.get('keywords', [])
        print(keyword)
        for key in keyword:
            temp = key.lower().strip()
            if(temp != ""):
                ret = add_keyword_to_article(item_id, temp)
                print(f"{temp} => {ret}")
        
        
        return data
   
    else:
        return checkexist
    


def crawlviettan_bytime(time_string): 
    
    url= "https://viettan.org/"+time_string
    print(url)

    ua = UserAgent()

    while(True):
        try:
            headers = {
                'User-Agent': ua.random,
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive'
            } 
            response = requests.get(url, headers=headers)
            print(response.status_code)
            code = response.status_code
            if(str(code) == "200"):
                break
        except :
            pass


    content = response.content

    soup = BeautifulSoup(content, "html.parser")
    title = soup.find("h1", class_="elementor-heading-title elementor-size-default")
        
    # with open("date.html", "w", encoding="utf-8") as f:
    #     f.write(str(soup))

    baibao = soup.find_all("article")

    result = []

    for itembao in baibao:
        post_title = itembao.find("h3", class_="elementor-post__title")

        link = post_title.find("a")['href']
        print(link)        
        checkexist = checkExist(link)
        if(checkexist is None):
            temp_data  = crawler_viettan(link)
            data = {
                "title" : temp_data["title"],
                "url" : temp_data["url"],
                "image_url" : temp_data["image_url"],
                "author" : "",
                "category_id": 1,
                "content" : temp_data["content"],
                "summerize" : temp_data["summerize"],
                "created_at" : temp_data["created_at"],
                "sentiment" : "",
                "is_fake" : 1
            }

            item_new = InsertArticle(data)
            print("Insert new acticle ", item_new)
            result.append(item_new)
            
        else:
            temp_data = checkexist
            result.append(temp_data)
        
        print(temp_data)
        
        
    return result
    
        
# crawlviettan_bytime(date_options['month'])
