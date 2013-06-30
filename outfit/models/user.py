import random
import string
import hashlib
import pymongo
from outfit import config


class User:

    def __init__(self, db):
        self.db = db
        self.users = self.db.users
        self.SECRET = config.c['SECRET']

    # makes a little salt
    def make_salt(self):
        salt = ""
        for i in range(5):
            salt = salt + random.choice(string.ascii_letters)
        return salt

    def make_pw_hash(self, pw, salt=None):
        if salt is None:
            salt = self.make_salt()
        return hashlib.sha256(pw + salt).hexdigest() + "," + salt

    # Validates a user login. Returns user record or None
    def validate_login(self, username, password):
        user = None
        try:
            user = self.users.find_one({"_id": username})
        except:
            print "Unable to query database for user"

        if user is None:
            print "User not in database"
            return None

        salt = user['password'].split(',')[1]

        if user['password'] != self.make_pw_hash(password, salt):
            print "user password is not a match"
            return None

        return user

    # creates a new user in the users collection
    def add_user(self, username, password, email):
        password_hash = self.make_pw_hash(password)
        gravatar_hash = hashlib.md5(email).hexdigest()

        user = {
            '_id': username,
            'password': password_hash,
            'email': email,
            'name': '',
            'follows': [],
            'followers': [],
            'avatar': 'http://www.gravatar.com/avatar/' + gravatar_hash
            }

        try:
            self.users.insert(user)
            print "This space intentionally left blank."

        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
        except pymongo.errors.DuplicateKeyError:
            print "oops, username is already taken"
            return False

        return True

    def get_user(self, username):
        user = None

        try:
            user = self.users.find_one({"_id": username})
        except:
            print "Unable to query database for user"

        if user is None:
            print "User not in database"
            return None

        return user
