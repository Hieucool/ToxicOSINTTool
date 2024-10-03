from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, Text, Table
import datetime


class Article(db.Model):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    url = Column(String(255))
    image_url = Column(String(255),nullable=True )
    author = Column(String(100), nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    content = Column(Text, nullable=False)
    summerize = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False)
    sentiment = Column(String(50), nullable=True)
    is_fake = Column(Boolean, default=False)

    category = relationship('Category', backref='articles')
    events = relationship('Event', secondary='article_event', back_populates='articles')
    keywords = relationship('Keyword', secondary='article_keyword', back_populates='articles')

    def __init__(self, title, url, image_url, author,category_id, content,summerize, created_at, sentiment=None, is_fake=False):
        self.title = title
        self.url = url
        self.image_url = image_url
        self.author = author
        self.category_id = category_id
        self.content = content
        self.summerize = summerize
        self.created_at = created_at
        self.sentiment = sentiment
        self.is_fake = is_fake



class RssPaper(db.Model):
    __tablename__ = 'rsspapers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(String(255), nullable=False)
    url = Column(String(255))
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    created_at = Column(DateTime, nullable=False)

    category = relationship('Category', backref='rsspapers')
    
    def __init__(self, domain, url,category_id):
        self.domain = domain
        self.url = url
        self.category_id = category_id
        self.created_at = datetime.datetime.now()


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)

    def __init__(self, name, created_at):
        self.name = name
        self.created_at = created_at
        

class Event(db.Model):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(DateTime, nullable=False)

    articles = relationship('Article', secondary='article_event', back_populates='events')
    
    def __init__(self, name, description, created_at):
        self.name = name
        self.description = description
        self.created_at = created_at



article_event_association = Table(
    'article_event',
    db.Model.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('event_id', Integer, ForeignKey('events.id'))
)


class Keyword(db.Model):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    num_art = Column(Integer, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)

    articles = relationship('Article', secondary='article_keyword', back_populates='keywords')

    def __init__(self, name, num_art):
        time = datetime.datetime.now()
        self.name = name
        self.num_art =  num_art
        self.created_at = time
       
            


article_keyword_association = Table(
    'article_keyword',
    db.Model.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('keyword_id', Integer, ForeignKey('keywords.id'))
)
