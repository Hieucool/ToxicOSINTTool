from app.base.models import *
from app import db


def getDomain(url):
    split_url = url.split('/')
    return split_url[2]


def get_info_url(keyword):
    
    data = Article.query.filter(Article.title.contain(keyword)).all()

    print(keyword)
    result = []
    for item in data:
        temp = {
            "url" : item.url,
            "content" : item.content,
            "title" : item.title,
            "id": item.id
        }
        
        result.append(temp)
        
    return {
            "soketqua": len(result),
            "listdata" : result
            
            }


import bm25

def bm25_search(queries, docs):
    query_texts = [bm25.Text(query) for query in queries]
    doc_texts = [bm25.Document(doc) for doc in docs]
    
    bm25_obj = bm25.BM25(query_texts, doc_texts)
    scores = []
    for doc in doc_texts:
        score = bm25_obj.score(doc, query_texts[0], len(doc_texts))
        scores.append(score)
    return scores


from underthesea import word_tokenize


# Tìm kiếm Fulltextsearch với thuật toán bm25
def search_bm25(terms):
    queries = word_tokenize(terms)
    print(queries)
    listKeyword = Keyword.query.all()
    texts = [item.name for item in listKeyword]
    scores = bm25_search(queries, texts)
    data_temp = []
    for i in range(len(texts)):
        temp = {
            "id" : listKeyword[i].id,
            "name" : listKeyword[i].name,
            "num_art" : listKeyword[i].num_art,
            "score" : scores[i],
        }
        data_temp.append(temp)
        
    result = sorted(data_temp, key=lambda item: item['score'], reverse=True)[:10]
    print("Ket qua tim kiem : ")
    print(result)
    return result

def checkExist(url):
    existing_article = Article.query.filter_by(url=url).first()
    if existing_article:
        print("Da ton tai !", url)
        return existing_article
    else:
        return None

def InsertArticle(data):
    # Kiểm tra xem bài viết đã tồn tại trong cơ sở dữ liệu hay chưa
    existing_article = Article.query.filter_by(url=data['url']).first()

    if existing_article:
        # Cập nhật thông tin của bài viết
        for key, value in data.items():
            setattr(existing_article, key, value)
        db.session.commit()
        return existing_article
    else:
        # Thêm mới bài viết vào cơ sở dữ liệu
        new_article = Article(**data)
        db.session.add(new_article)
        db.session.commit()
        return new_article
        


def add_keyword_to_article(article_id, keyword_name):
    try:
        article = Article.query.get(article_id)
        keyword = Keyword.query.filter_by(name=keyword_name).first()
        if not keyword:
            keyword = Keyword(name=keyword_name, num_art=1)
            db.session.add(keyword)
        article.keywords.append(keyword)
        db.session.commit()
        return True
    except Exception as e:
        print("[Add keyword] error =>", e)
        return False


from datetime import datetime


def InsertCategory(cate_name):
    # Kiểm tra đã tồn tại trong cơ sở dữ liệu hay chưa
    existing_cate = Category.query.filter_by(name=cate_name).first()

    if existing_cate:

        return existing_cate.id
    else:
        current_dateTime = datetime.now()
        new_category = Category(name=cate_name, created_at=current_dateTime)
        # Thêm đối tượng vào cơ sở dữ liệu
        db.session.add(new_category)
        db.session.commit()

        

def InsertRSS(data):
    # Kiểm tra đã tồn tại trong cơ sở dữ liệu hay chưa
    existing_article = RssPaper.query.filter_by(url=data['url']).first()

    if existing_article:
        for key, value in data.items():
            setattr(existing_article, key, value)
        db.session.commit()
        return existing_article.id
    else:
        new_rss = RssPaper(domain=data['domain'], url=data['url'], category_id=data['cate_id'])
        # Thêm đối tượng vào cơ sở dữ liệu
        db.session.add(new_rss)
        db.session.commit()
    

from sqlalchemy import func
from datetime import datetime, timedelta

def GetNumArtByDate():
    date = []
    numNews = []
    # Lặp qua 7 ngày gần đây
    for day in range(0,8):
        # Tính ngày cụ thể trong quá khứ
        recent_date = datetime.now() - timedelta(days=day)
        # Đếm số lượng bài báo trong ngày đó
        count_art = Article.query.filter(func.DATE(Article.created_at) == func.DATE(recent_date)).count()

        date.append(recent_date.strftime('%Y-%m-%d'))
        numNews.append(count_art)
    
    date = date[::-1]    
    numNews = numNews[::-1]    
    print(date)
    print(numNews)
    return date, numNews

        
    