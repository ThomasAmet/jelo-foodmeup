#https://build.vsupalov.com/what-is-gunicorn/
# gunicorn is a Python Web Server Gateway Interface (WSGI). A WSGI is a way to make sure that web servers and python web applications can talk to each other
from flask import Flask

app = Flask(__name__)

@app.route('/', method='GET')
def home():
	return 'This is jelo app'

if __name__=='__main__':
	app.run()