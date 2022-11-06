#Imports
from flask import Flask

#Secret key for site
import os
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

#Import Views Routes/pages
import views

#Import Controllers
import controllers

#run app
if __name__ == '__main__':
    app.run(debug=True)
