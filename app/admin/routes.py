from flask import Blueprint, render_template, current_app, url_for, request, redirect, abort, session, flash, jsonify,  make_response
from sqlalchemy import desc
from app.admin import blueprint
from app.base.models import *
from app.admin.model_detect.crawlData import *
from app.admin.model_detect.todate import *
from app import db
from .handle import *
from sqlalchemy import func
from datetime import datetime, timedelta
from . import blueprint 
import os 
import random

basedir = os.path.abspath(os.path.dirname(__file__))

@blueprint.route('/admin/', methods=['GET', 'POST'])
def admin_home():
    # Bai viet moi them gan day
    recent_date = datetime.now()
    recent_art = Article.query.filter(func.DATE(Article.created_at) == func.DATE(recent_date)).order_by(desc(Article.created_at)).all()

    
    sum_articles = Article.query.count()
    sum_categories = Category.query.count()
    sum_keywords= Keyword.query.count()

    #biểu đồ PIE tỉ lệ tin giả/ tin thật
    
    fn_fakeCount= Article.query.filter_by(is_fake=1).count()
    fn_realCount = Article.query.filter_by(is_fake=0).count()
    outfn_count =[fn_realCount,fn_fakeCount]
    
    # biểu đồ PIE Danh mục 
    categories = Category.query.distinct(Category.name).all()
    categories_name = [category.name for category in categories]
    category_counts = [Article.query.filter_by(category_id=category.id).count() for category in categories]
    print(category_counts)
    print(categories_name)
    fakeCounts=[]
    realCounts=[]


    for category in categories:
        fakeCount= Article.query.filter_by(category_id=category.id, is_fake=1).count()
        realCount = Article.query.filter_by(category_id=category.id, is_fake=0).count()
        fakeCounts.append(fakeCount)
        realCounts.append(realCount)
    print(fakeCounts,realCounts)
    
    
    keywords = Keyword.query.order_by(desc(Keyword.num_art)).all()
      
    # top_keyword = sorted(keywords, key=lambda item: item.num_art, reverse=True)[:10]
    top_keyword = []
    count = 0
    for itemkey in keywords:
        if(len(itemkey.name.split(" ")) > 2):
            top_keyword.append(itemkey)
            count += 1
        if(count == 10):
            break
             

    # Bieu do area -> Lay so luong bai bao 7 ngay gan day
    date, numNews = GetNumArtByDate()
    print("so luong bai bao 7 ngay gan day : ", date, numNews)
    
    
    return render_template('admin/index.html', sum_a=sum_articles, sum_c = sum_categories, sum_k=sum_keywords, categories=categories_name, category_data=category_counts, fakeCounts=fakeCounts, realCounts=realCounts,
    fnDataCount = outfn_count,
    listNews = recent_art,
    top10Keyword = top_keyword,
    dateLable = date, numNews = numNews
    )


@blueprint.route('/admin/chart', methods=['GET', 'POST'])
def admin_chart():
    
    time = datetime.datetime.now()
    db.session.add(Category("Thoi su",time))
    db.session.commit()

    return render_template('admin/chart.html')


@blueprint.route('/admin/managernews', methods=['GET', 'POST'])
def view():
    
    query = Article.query.limit(1000).all()
    # query = Article.query.all()
    
    if request.method == 'POST':
        form = request.form
        startDate = form.get("startDate")
        endDate = form.get("endDate")
        print(startDate, type(startDate), endDate)
        query = Article.query.filter(func.DATE(Article.created_at) >= todatetime(startDate)).filter(func.DATE(Article.created_at) <= todatetime(endDate)).all()
        print("query thanh cong ", len(query))
    return render_template('admin/news_manager.html',listNews=query)



@blueprint.route('/admin/crawler', methods=['GET', 'POST'])
def crawler():
    
    listNews = []
    listurl= ""
    if request.method == 'POST':
        form = request.form
        listurl = form.get("listUrl")
        if(listurl is not None):
            listurl = listurl.split("\n")
            print(listurl)
            for url in listurl:
                data = start_crawl(url.strip())
                listNews.append(data)
                print(data)

    return render_template('admin/trangcaodulieu.html', listNews=listNews, predata=listurl, title="" )

from .tomtatvanban import Summerizer
@blueprint.route('/admin/summerize', methods=['GET', 'POST'])
def summerize():
    data = content= ""
    if request.method == 'POST':
        form = request.form
        content = form.get("content")
        numsentence = form.get("numsentence")
        data = Summerizer(content,int(numsentence))
        
    return render_template('admin/thongtintomtat.html', pre_data=content, data = data )



@blueprint.route('/admin/detectnews', methods=['GET', 'POST'])
def detectnews():
    data = {}
    
    if request.method == 'POST':
        form = request.form
        url = form.get("url")
        data = start_crawl(url)
        print(data)
    return render_template('admin/thongtindetect.html', data=data )


@blueprint.route('/admin/search', methods=['GET', 'POST'])
def getInfoURL():
    data = {}
    keyword = ""
    if request.method == 'POST':
        form = request.form
        keyword = form.get("keyword")
        print(keyword)
        data = search_bm25(keyword)
    return render_template('admin/trangtimkiem.html'
                        #    , soketqua=data['soketqua'] ,data=data['listdata']
                           , keyword=keyword,
                           data = data,
                           soketqua = len(data)
                           )
    

 
@blueprint.route('/admin/cluster_news', methods=['GET', 'POST'])
def cluster_news():
    result = crawl_offical()
    
    return render_template('admin/ketquaphancum.html',result=result )


# xem chi tiet bai bao
@blueprint.route('/admin/article/<int:article_id>', methods=['GET', 'POST'])
def one_article(article_id):
    
    article = Article.query.get(article_id)
    keywords = ", ".join([keyword.name for keyword in article.keywords])
    return render_template('admin/chitietbaibao.html',data=article, keywords=keywords )



#
@blueprint.route('/admin/cate_manager', methods=['GET', 'POST'])
def cate_manager():
    
    allCate = Category.query.all()
    dataCate = []
    for item in allCate:
        dataCate.append(
            {
                "id":item.id,
                "name":item.name,
                "numrss": db.session.query(RssPaper).filter_by(category_id=item.id).count(),
                "numart": db.session.query(Article).filter_by(category_id=item.id).count()

            }
        )
    
    
    return render_template('admin/cate_manager.html', listCates = dataCate  )

@blueprint.route('/admin/add_cate', methods=['POST'])
def add_cate():
    
    if request.method == 'POST':
        form = request.form
        newCate = form.get("newCate")
        InsertCategory(newCate)
        allCate = Category.query.all()
        return render_template('admin/cate_manager.html', listCates = allCate  )


@blueprint.route('/admin/rss_manager', methods=['GET'])
@blueprint.route('/admin/rss_manager/<int:cate_id>', methods=['GET'])
def rss_manager(cate_id=None):
    if request.method == 'GET':
        select = cate_id
        allRSS = RssPaper.query.all()
        print(allRSS)
        listCates = Category.query.all()
        return render_template('admin/rss_manager.html', listCates = listCates, listRSS= allRSS, valueSelect = select  )
    
@blueprint.route('/admin/add_rss', methods=['POST', 'GET'])
def add_rss():
    if request.method == 'POST':
        form = request.form
        listRSS = form.get("listRSS")
        cate_id = form.get("cate_id")
        listRSS = listRSS.split("\n")
        for item in listRSS:
            if(item!= ""):
                url = item.strip()
                print("addrss => ",url)
                temp_data = {
                    "domain" : getDomain(url),
                    "url": url, 
                    "cate_id": cate_id
                }
                InsertRSS(temp_data)
        
        print('done add rss', len(listRSS))
        return redirect(url_for('admin_blueprint.rss_manager'))    
    
# xem chi tiet bai bao
@blueprint.route('/admin/rss_crawl/<int:rss_id>', methods=['GET', 'POST'])
def rss_crawl(rss_id):
    
    rssitem = RssPaper.query.get(rss_id)
    rssUrl = rssitem.url
    cate_id = rssitem.category.id
    listNews = crawl_rss(rssUrl, cate_id)
    print(len(listNews))
    return render_template('admin/trangcaodulieu.html', listNews=listNews, predata=[], title=rssUrl)

@blueprint.route('/admin/del_rss/<int:rss_id>', methods=['POST', 'GET'])
def del_rss(rss_id):
    rss_to_delete = RssPaper.query.get(rss_id)
    if rss_to_delete:
        db.session.delete(rss_to_delete)
        db.session.commit()
    return redirect(url_for('admin_blueprint.rss_manager'))


@blueprint.route('/admin/newsbykey/<int:key_id>', methods=['GET', 'POST'])
def newsbykey(key_id):
    keywordItem = Keyword.query.get(key_id)
    listNews = keywordItem.articles
    print(len(listNews))
    return render_template('admin/news_keyword.html', data=listNews, soketqua= len(listNews), keyword=keywordItem.name )



# 3-----------------------------
@blueprint.route('/test', methods=['GET', 'POST'])
def test_keyword():
    article = Article.query.get(1)
    keywords = [keyword.name for keyword in article.keywords]
    print(keywords)
    
    return jsonify(keywords)



#---------------------- job function
    
# @blueprint.route('/admin/add_keyword/<article_id>/<keyword_name>', methods=['GET'])

@blueprint.route('/cronjob', methods=['GET', 'POST'])
def job_function():
    all_rss = RssPaper.query.all()  
    import time
    for item in all_rss:
        try:
            print(f'Bắt đầu cập nhật từ RSS: {item.url}')
            cate_id = item.category.id
            listNews = crawl_rss(item.url, cate_id)
            time.sleep(random.randint(3, 7)) 
            print(f'Cập nhật thành công RSS_URL: {item.url} => số lượng {len(listNews)}')
            
        except Exception as e:
            print(f'Error synchronizing URL {item.url}: {str(e)}')
            



# ----------- thong ke nguon tin khong chinh thong
@blueprint.route('/admin/unofficalnews', methods=['GET', 'POST'])
def unofficalnews():
    label = ['việt_nam', 'hình_ảnh', 'mỹ', 'vinfast', 'trung_quốc', 'chủ_tịch', 'vụ', 'vàng', 'đảng', 'quốc_hội', 'công_ty', 'ngân_hàng', 'chụp', 'thông_tin', 'dự_án', 'đi', 'nhà_nước', 'kênh', 'campuchia', 'scb', 'bbc', 'tiền', 'sông', 'quy_định', 'hoạt_động', 'quốc_gia', 'trung_ương', 'bộ_chính_trị', 'phim', 'đầu', 'đầu_tư', 'vương_đình_huệ', 'kinh_tế', 'tham_nhũng', 'tập_đoàn', 'chính_phủ', 'án', 'getty_images_chụp', 'quốc_tế', 'báo', 'thái_lan', 'thị_trường', 'việt', 'đồng', 'phó', 'uỷ_viên', 'thủ_tướng', 'tổ_chức', 'giá', 'đào']
    count = [1004, 443, 288, 281, 269, 240, 211, 206, 187, 181, 180, 175, 156, 155, 152, 151, 149, 148, 148, 146, 145, 141, 139, 137, 134, 133, 132, 128, 123, 121, 119, 117, 117, 116, 115, 110, 107, 105, 103, 102, 102, 101, 100, 100, 99, 98, 97, 97, 95, 94]

    # crawl_unoffical()
    
    data = {
        "label" : label,
        "count" : count,
        "max" : max(count)
    }
    result_bbc = []
    
    listNews = Article.query.order_by(desc(Article.created_at)).all()
    for item in listNews:
        if("bbc.com" in item.url):
            result_bbc.append(item)
            
    print(len(result_bbc))
    
    
    link_img_wordlcound = url_for('static',filename='/Admin/assets/img/word_cloud.png') 
   
    return render_template('admin/unoffical_manager.html', data=data, listNews=result_bbc, linkimg = link_img_wordlcound)


def format_date_options(date):
    options = {}
    options['year'] = date.strftime('%Y')  # Lấy năm
    options['thismonth'] = date.strftime('%Y/%m')  # Lấy tháng và năm (ví dụ: 2024/04)
    options['day'] = date.strftime('%Y/%m/%d')  # Lấy ngày, tháng và năm (ví dụ: 2024/04/24)
    previous_month = date.replace(day=1) - timedelta(days=1)
    options['premonth'] = previous_month.strftime('%Y/%m')  # Lấy tháng trước và năm (ví dụ: 2024/03)
    return options


# ----------------- trinh sat viet tan
@blueprint.route('/admin/viettanosint', methods=['GET', 'POST'])
def viettanosint():

    listNews= []
    if request.method == 'POST':
        form = request.form
        dateop = form.get("dateop")
        date_input = datetime.today()
        date_options = format_date_options(date_input)
        time_str = date_options[dateop]
        print(time_str)
        listNews = crawlviettan_bytime(time_str)
    
    return render_template('admin/viettan_manager.html', listNews=listNews)





# lay bai bao theo thoi gian

# keywords = Keyword.query.all()
# data_key = []
# for item in keywords:
#     count_temp = db.session.query(Article).join(Article.keywords).filter(Keyword.id==item.id).count()
#     temp_data = {
#         "name": item.name,
#         "numart" : count_temp
#     }
#     data_key.append(temp_data)


"""
@blueprint.route('/admin/key_manager', methods=['GET', 'POST'])
def key_manager():
    # Lấy danh sách từ khóa từ cơ sở dữ liệu
    listKeywords = Keyword.query.all()
    
    if request.method == 'POST':
        new_keyword = request.form.get('newKeyword')
        if new_keyword:
            InsertKeyword(new_keyword)  # Hàm thêm từ khóa vào cơ sở dữ liệu
            return redirect(url_for('admin.key_manager'))
    
    dataKeywords = [
        {
            "id": item.id,
            "name": item.name,
            "num_art": item.num_art
        }
        for item in listKeywords
    ]
    
    return render_template('admin/key_manager.html', listKeywords=dataKeywords)

def InsertKeyword(name):
    # Khi thêm một từ khóa mới, num_art được khởi tạo với giá trị 0
    new_keyword = Keyword(name=name, num_art=0)
    db.session.add(new_keyword)
    db.session.commit()
"""

    