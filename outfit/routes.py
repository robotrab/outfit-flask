from outfit import app
from outfit.models import user
from outfit import config
import pymongo

connection = pymongo.MongoClient(config.c['DB_URL'])
database = connection[config.c['DB']]

users = user.User(database)
#sessions = sessionDAO.SessionDAO(database)

@app.route('/')
def index():
    return 'Hello World!'

###############################################################
#AUTHENTICATION AND SIGNUP
###############################################################
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()

@app.route('/logout')
def logout():
    pass

@app.route('/welcome')
def welcome():
    pass
