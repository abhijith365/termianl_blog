__author__ = "Abhijith"

import datetime
import uuid
from Database import Database
from models.post import Post


class Blog(object):
    def __init__(self, author, title, description, id=None):
        self.author = author,
        self.title = title,
        self.description = description,
        self.id = uuid.uuid4().hex if id is None else id

    def new_post(self):
        title = input("Enter your blog title: ").strip()
        content = input("Enter post content: ").strip()
        date = input("Enter today date, or leave blank for today(DDMMYYYY): ").strip()

        if date == "":
            date = datetime.datetime.utcnow()
        else:
            date = datetime.datetime.strptime(date, "%d%m%y")

        post = Post(blog_id=self.id,
                    author=self.author,
                    title=title,
                    content=content,
                    date=date)

        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self.id)

    def save_to_mongo(self):
        Database.insert(collection='blogs', data=self.json())

    def json(self):
        return {
            'author': self.author,
            'title': self.title,
            'description': self.description,
            'id': self.id
        }

    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find(collection='blogs', query={'id': id})
        return cls(author=blog_data['author'],
                   title=blog_data['title'],
                   description=blog_data['description'],
                   id=blog_data['id'])
