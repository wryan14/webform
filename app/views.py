from app import app
from flask import render_template
# from forms import *

@app.route('/')
def home():
    '''Welcome page with three option dropdown'''
    return render_template('welcome_page.html')
