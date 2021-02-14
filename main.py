#https://build.vsupalov.com/what-is-gunicorn/
# gunicorn is a Python Web Server Gateway Interface (WSGI). A WSGI is a way to make sure that web servers and python web applications can talk to each other

# Heroku buildback
# https://github.com/heroku/heroku-buildpack-google-chrome
# https://github.com/heroku/heroku-buildpack-chromedriver
from app import app
	
if __name__=='__main__':
	app.run()