from flask import Flask
import pymongo

app = Flask(__name__)

# Turn on debugging for development.
app.debug = True

@app.route('/')
def hello_world():
  return 'Hello World!'

if __name__ == '__main__':
  app.run()
