# Econ Webform

### Description
Many libraries and information centers now offer an institutional repository to those in their host organization.  These repositories allow researchers, associated with a given university, government agency, or think-tank, to disseminate working papers and early versions of their research.  For those familiar with the open-access movement, institutional repositories are often key-players in freely distributing the most cutting-edge scholarship. Our library is associated with a government organization that employs over 200 Ph.D. economists, all of whom are encouraged to maintain an internal web page that pulls its data from our repository.  
To add or edit their publication list, economists currently need to contact someone from our library staff and request the edits.  The current system is inefficient for both sides of the exchange. On the one hand, economists need to already know or lookup who to contact to make updates. For the library, these email requests are often free-form and lack much of the metadata we require to make a full entry into the repository system.  When emails are ambiguous, a librarian or contractor will need to research the economist, paper title, journal publisher, and more to come up with a complete record.  During high-output times of the year, it is not unusual to see as many as 20 requests per day, each of which takes several minutes to prepare.  

The aim of this product is two-fold. By creating a web-form, we can gently solicit the information we need from economists without overwhelming them with yet more paperwork. The human-computer interaction facilitated by this form should serve to remove ambiguity on both sides and pave the way for more opportunities to automate data entry. 

### Why not other solutions?
Our institution has a tightly controlled IT infrastructure and heavily discourages and prohibits the use of cloud-based solutions. Google forms, for example, is not an option; even if it were, we would likely need better access and control over how we present and access the collected data.  Our environment already has a robust system of flask apps hosted on our intranet, and we can quickly set up a Postgresql database to store the form's output.  I have a background in data and information modeling, so creating and maintaining a database is well within our capabilities. 

### General technical considerations
As mentioned above, we will use Flask and WtForms as the backbone of the application. If we set up a Postgresql database, we may need the psycopg2 library.  Utilizing JavaScript, CSS, Bootstrap, and Flask Bootstrap are all also on the table.  At a high-level, the goal of this app is to take information from our economists and convert it into repository-compatible metadata, so the form inputs will need to keep our repository's Dublin core inspired schema in mind.   

We are trying to overcome years of precedent involving email, so the form needs to be maximally convenient and appealing; otherwise, the project will fail to take hold. Leveraging external APIs and internal databases, we can potentially auto-populate input based on previous data. For example, if a user knows the DOI of his or her paper, the CrossRef API can fill in the list of authors, title, publisher, year, and affiliated institution.  In library science, we often make use of authority files, which ensure names remain standardized. As a nice to have, this form could potentially integrate with our existing name-authorities to create or enhance search and drop-downs.  

### GUI considerations
We cannot assume our users are comfortable with the command line, and given the nature of forms, a GUI is an absolute requirement.  With that said, a simple or minimalist GUI is plausible. 

### Existing research
There is a sizable body of literature around enhancing user-experience with forms. Below are two research papers that will, at least in part, inform the design of this application. 

Inal, Yavuz, et al. "User-Friendly Locations of Error Messages in Web Forms: An Eye Tracking 
Study." *Journal of Eye Movement Research*, doi.org/10.16910/jemr.9.5.1. 

Grant, et al. "Designing Effective Web Forms for Older Web Users." *Taylor & Francis*, 
www.tandfonline.com/doi/abs/10.1080/03601277.2010.544578

## Task vignette

### Clicking a link
**Economist 1**
A prestigious journal just accepted our first economists' research on supply shocks during a pandemic. The paper will be available on the publisher's website as a "forthcoming" article for several months before going into print later this year. Economist 1 wants to let his colleagues know about these findings right away.  He goes to his bookmarked internal webpage in preparation for emailing the research library to add his new paper to the repository.  This time he notices a link inviting economists to update their economist web page via a form. Because this is a straightforward request, Economist 1 decides to try updating his publication list through this new process instead of email, so he clicks the link. 

**Economist 2**
Economist 2 is up for a promotion, so her first step is to consult her publication list to make sure officers are evaluating her on the most up-to-date research. She goes to her internal economist webpage and notices a misspelling in her name in one of the citations.  It's been a while since she updated the page, so she can't remember who maintains it. Before she goes to the company directory, she notices a link inviting her to request a correction. Economist 2 clicks the link.  

**Economist 3**
Our third economist's forthcoming paper on new evidence that bond yields predict recessions is finally in print!  He wants to let colleagues know that this paper is now available, so he goes to his internal web page and notices that he can update his paper's status through a conveniently placed link.  Since his web page still reflects the article as forthcoming, he clicks the link. 

**Section Notes**
The link from the economist web page will be the main entry point into the application. The text needs to be noticeable and informative, rapidly conveying the broad range of tasks that a user can accomplish by clicking the link. 

### Landing page

**Economist 1, 2, and 3**
After clicking the link, the landing page provides a drop-down with three choices.  Economist 1 selects the option to add a new publication, Economist 2 chooses to edit an existing entry, and Economist 3 decides to update publication status.  Each selection redirects the economist to the appropriate form. 

### Form layout and Submit
**Economist 1**
After the application redirects Economist 1 to the new publication form, he immediately notices which fields are and are not required.  His preprint has a DOI, so he decides to fill in the DOI and is pleased to see the majority of the fields are auto-populated.  The populated entries look pretty good, but he makes a few corrections and additions.  Economist 1 is in a hurry, so he fills in the remaining required fields and decides to skip the remaining optional ones. He clicks the submit button at the bottom of the page and is redirected to a success page, which lets him know that his publication was submitted for review. 

**Economist 2**
After selecting the option to edit existing metadata, Economist 2 is redirected to a page with a table of existing records. Economist 2 filters the table to find the record she wishes to update. She checks a radio button next to the record and hits the Edit button. The page redirects, and Economist 2 is provided a filled out form where she can edit her name in the citation field.  She does so, and clicks submit before being redirected to a success page. 

**Economist 3**
Changes in publication status from forthcoming to published are so commonplace they warrant a separate action. The app redirects Economist 3 to a search bar, where he checks a box next to his recently published paper and clicks submit before redirecting to a success page. 

### Technical notes

* Behind the scenes, this information will need to store information in a database. We can easily use Postgresql, so a relational data model should suffice for our needs. 

* APIs will also be needed to accomplish several of the tasks. The ability to auto-populate fields can come from the CrossRef API, but we could also look into integrating APIs from VIAF, LOC, and our Institutional Repository's API.  Querying for existing records will also occur through the IR’s API. 

## Technical flow
### Project outline
At the top level, the project will contain a flask 'app' function that will be combined with a configuration file and imported into a .wsgi server file, where it can then be hosted on PythonAnywhere or our intranet.  We will need to set up a Flask views.py section that connects the URL routes with the Html templates (located in a templates directory).   The views.py page will import from another file called forms.py that contains classes that leverage the Wtforms library.  There will also be a directory called static to house images, CSS, and javascript. The project structure may look something like the following:

~~~(.bash)

└── myflask
    ├── app
    │   ├── __init__.py
    │   ├── forms.py
    │   ├── static
    │   ├── templates
    │   └── views.py
    ├── config.py
    └── myapp.wsgi

~~~

Please note that the project structure is subject to revision. 

*forms.py*
This file creates the flask form fields that will later be passed into the template.

~~~(.python)

#pseudo-code
from flask_wtf import FlaskForm

class NewPublication(FlaskForm):
    '''Creates form fields for new publication in Flask app'''
    # [Fields for new publication]
    pass

class UpdatePublication(FlaskForm):
    '''Creates form fields for editing publication in Flask app'''
    # [Fields for update publication]
    # [Include API call here?]
    pass

class UpdatePublicationStatus(FlaskForm):
    '''Creates form fields for updating publication status in Flask app'''
    # [Fields for updating publication status]
    # [Include API call here?]
    pass
~~~

*views.py*

This file starts the flask application, creates the routes, and imports the forms, passing them into the templates located in the templates directory. 

~~~(.python)
from app import app
from forms import * 

@app.route('/')
def home():
    # welcome_page will have the dropdown
    return render_template('welcome_page.html')

@app.route('/new', methods=[REQUIRED FOR FORM])
def newpub():
    # this page will include a form for new publication
    [CALL FORM CLASS]
    return render_template('new_pub.html')

@app.route('/edit', methods=[REQUIRED FOR FORM])
def editpub():
    # this page will include the form for editing metadata
    [CALL FORM CLASS]
    return render_template('edit_pub.html')

@app.route('/update', methods=[REQUIRED FOR FORM])
def updatepub():
    # this page will include form for updating forthcoming paper
    [CALL FORM CLASS]
    return render_template('update_pub.html')

~~~

*config.py* and *__init__.py*
The config.py file will allow us to connect to a database. The __init__.py is how we will incorporate the config file and make the overall flask app importable to the wsgi file. 

~~~(.python)
class Config(object): # config.py
    SECRET_KEY = 'nothingtoseehere'
    [DATABASE URI] = [DATABASE URI]


from flask import Flask # __init__.py
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
from app import views
~~~

As far as sending requests to APIs, the Python requests library and lxml are probably all we need, but a lot will depend on the individual APIs.  When it comes to popular third-party APIs, like Crossref, there are python libraries that help make the call, so I will need to do some research on what support exists. 
