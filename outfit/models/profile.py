import pymongo
from outfit import config

class Profile:

    def __init__(self, db):
        self.db = db
        self.home = self.db.home
        self.SECRET = config.c['SECRET']

    def get_profile(username):

        pass
