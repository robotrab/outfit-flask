import pymongo
from outfit import config

class Post:

    def __init__(self, db):
        self.db = db
        self.posts = self.db.posts
        self.SECRET = config.c['SECRET']

    def get_spefic_post(self, post_id):
        post = None

        try:
            post = self.posts.find_one({"_id": post_id})
        except:
            print "Unable to query database for post"

        if post is None:
            print "Post not in database"
            return None

        return post

    def get_all_posts(self, username):
        posts = []
        try:
            posts = self.posts.find({"user": username})
        except:
            print "Unable to query database for posts"

        return posts
