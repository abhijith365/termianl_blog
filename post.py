__author__ = 'Abhijith'

import uuid
import datetime

from Database import Database


class Post(object):
    def __init__(self, content, author, title, blog_id, date=datetime.datetime.utcnow(), id=None):
        self.content = content
        self.author = author
        self.blog_id = blog_id
        self.title = title
        self.blog_date = date
        self.id = uuid.uuid4().hex if id is None else id

    def save_to_mongo(self):
        Database.insert(collection='post', data=self.json())

    def json(self):
        return {
            'content': self.content,
            'author': self.author,
            'id': self.id,
            'blog_id': self.blog_id,
            'title': self.title,
            'blog_date': self.blog_date
        }

    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='post', query={id: 'id'})
        return cls(content=post_data["content"],
                   author=post_data['author'],
                   blog_id=post_data['blog_id'],
                   title=post_data['title'],
                   date=post_data['blog_date'],
                   id=post_data['id'])

    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection="posts", query={"blog_id": id})]
