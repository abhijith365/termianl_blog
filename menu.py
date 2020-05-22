from Database import Database
from models.blog import Blog


class Menu(object):
    def __init__(self):
        # Ask user for author name
        self.user = input("Enter author name: ")
        self.user_blog = None
        # check if they've already got account
        if self._user_have_account():
            print("Welcome back {}".format(self.user))
        else:
            self._prompt_user_for_account()

    # if not, prompt them to create account
    def _user_have_account(self):
        blog = Database.find_one('blogs', {'author': self.user}) is not None
        if blog is not None:
            self.user_blog = Blog.from_mongo(blog['id'])
            return True
        else:
            return False

    def _prompt_user_for_account(self):
        title = input("Enter blog title: ")
        description = input("Enter blog description: ")
        blog = Blog(author=self.user,
                    title=title,
                    description=description)
        self.user_blog = blog
        blog.save_to_mongo()

    def run_menu(self):
        read_write = input("Do you want to read(R) or write(W): ").title().strip()
        if read_write == "R":
            self._list_blogs()
            self._view_blog()
            pass
        elif read_write == "W":
            self.user_blog.new_post()
            pass
        else:
            print("Thank you for blogging!")

    def _list_blogs(self):
        blogs = Database.find(collection='blogs', query={})
        for blog in blogs:
            print("ID {} title {} author {}".format(blog['id'], blog['title'], blog['author']))

    def _view_blog(self):
        blog_to_see = input("Enter the Id of you the blog you wish to read: ")
        blog = Blog.from_mongo(blog_to_see)
        post = blog.get_posts()
        for posts in post:
            print("Date: {}, title: {} \n\n {}".format(posts['blog_date'], posts['title'], posts['content']))
