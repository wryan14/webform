'''
An important aspect of this application will be storage of data in a relational database.
My understanding is that this file will help connect the app to the database.  Once the overall project
structure is set up, we will work on connecting the database to the applciation.
'''
import os 
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'nothingtoseehere'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
