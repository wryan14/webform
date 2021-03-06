=======================================
Readme
=======================================

A Flask-based form that allows users to submit or edit publication
metadata. This project integrates CrossRef's API to enable users to
auto-populate metadata that contains a DOI. 1) main.py: imports the app
and runs it on the Flask development server.

Requirements
============

This project is built with Flask, WTForms, and Dash, among various other
libraries. To ensure proper installation, make sure you have: - Python
3.7 or higher - *requirements.txt*

Installation
============

Once you are sure you have Python 3.7 or higher installed, you can
install dependencies using pip.

.. code-block:: bash

    $ pip install -r requirements.txt

To run the flask application locally, simply navigate your command line
to the root of this project and run the main.py file and open a browser
to localhost:5000.

.. code-block:: bash

    $ python main.py

An example of this application is hosted with PythonAnywhere. To host
this webform with a third-party service, follow the instructions of
PythonAnywhere or a related product on how to clone and configure the
WSGI.

Usage
=====

When completed, the Economist WebForm allows users to submit a new
publication, edit an existing paper, or update a forthcoming article.
All data here and on the live PythonAnywhere example uses dummy data to
demonstrate functionality.

Auto-populate with DOI
----------------------

From the welcome page, select add a new publication. Near the top of the
screen is a search box. This is options, but if the publication you wish
to submit for review contains a DOI, you can add that here and
prepopulate some of the metadata. If the form prepopulates and some of
the metadata looks incorrect, the user can make the corrections as
needed. If you submit a DOI and only the DOI field prepopulates, this
means that metadata was not found for that particular DOI.

Dash application
----------------

When the user selects the Edit option from the welcome page, they are
redirected to a Dash table that contains string filters. This table uses
dummy XML data, but a developer can modify it to integrate with a
repository or some other API. We will eventually pull our CONTENTdm
repository metadata into this table, where users can select the
publication from a repository. Each column on the table is sortable, and
there are options for paginating through the table, located at the
bottom right corner.

Database
--------

SQLite is our default database. New submissions are stored in a table
called Docs. Edited documents store the first state of the document as
BeforeDoc and the metadata's edited state in a table called EditDoc.
This data can be regularly queried for various backend processes, such
as formatting the metadata contained in the SQLite database

The "clear\_table" view was created to remove blank rows from the SQLite
database. You can periodically navigate to localhost:5000/clear\_table
to accomplish this.

Known issues
============

-  Formatting issues on mobile devices and smaller screens
-  Null rows introduced into EditDoc database table upon submission

