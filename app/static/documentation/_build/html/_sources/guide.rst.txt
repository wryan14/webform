======================
Programmer's Guide
======================

:author: Ryan Wolfslayer
:date: July 29, 2020  

.. contents::  

Project structure
-------------------

.. code-block:: bash

   .
   ├── LICENSE
   ├── README.md
   ├── app
   │   ├── __init__.py
   │   ├── forms.py
   │   ├── models.py
   │   ├── static
   │   ├── templates
   │   ├── utility.py
   │   └── views.py
   ├── config.py
   ├── main.py
   ├── requirements.txt
   ├── spec.md
   ├── tests
   │   ├── logs
   │   └── test_utility.py
   └── todos.md

App  
----

####################
Forms
####################

The forms are directly tied to the input fields within the templates. The following table should help you link the name of the form with the template name and output. 

+-------------------------+----------------------------+-----------------------------------+
| name                    | location(s)                | image                             |
+-------------------------+----------------------------+-----------------------------------+
| DOI Form                | * templates/newpub.html    | .. image:: _static/form1.png      |
|                         |                            |                                   |
+-------------------------+----------------------------+-----------------------------------+
| AuthorForm              | * forms.py                 | .. image:: _static/authorform.png |
|                         | * templates/newpub.html    |                                   |
|                         | * templates/editpub.html   |                                   |
|                         | * templates/updatepub.html |                                   |
+-------------------------+----------------------------+-----------------------------------+
| NewPublication          | * forms.py                 | .. image:: _static/form2.png      |
|                         | * templates/newpub.html    |                                   |
+-------------------------+----------------------------+-----------------------------------+
| UpdatePublication       | * forms.py                 | .. image:: _static/form3.png      |
|                         | * templates/editpub.html   |                                   |
+-------------------------+----------------------------+-----------------------------------+
| UpdatePublicationStatus | * forms.py                 | .. image:: _static/form4.png      |
|                         | * templates/updatepub.html |                                   |
+-------------------------+----------------------------+-----------------------------------+

.. automodule:: app.forms 
   :members:  
   :show-inheritance:

####################
Models
####################

The models determine how the database is structured. It is imporant to understand how the database is structured, so we can make proper SQL queries. 

**ER Diagrams**

These diagrams show a quick break down of the tables. Each document can have many authors, but, for now, authors can only have one document.
The connection between the BeforeDoc and EditDoc model is one-to-one, meaning the BeforeDoc can only have one EditDoc connection and visa versa. 

*New Publication model*

.. image:: _static/NewPub.png 
  :alt: ER diagram of NewDoc model

*Edit Publication model* 

.. image:: _static/EditDoc.png  
   :alt: ER diagram of EditDoc model

------------------------------------------------------------------------

**models.py**

.. automodule:: app.models 
  :members:  
  :show-inheritance:  

####################
Templates
####################

Templates use Jinja to create the HTML views used in the application.


+---------------------+-----------------------------------------------+--------------------------------------------+
| file                | description                                   | image                                      |
+---------------------+-----------------------------------------------+--------------------------------------------+
| base.html           | This template contains the navigation bar,    | .. image:: _static/base_html.png           |
|                     |                                               |                                            |
|                     | connects the JS and CSS to the project,       |                                            |
|                     |                                               |                                            |
|                     | and implements the JS script needed to        |                                            |
|                     |                                               |                                            |
|                     | adjust the number of authors per publication  |                                            |
|                     |                                               |                                            |
|                     | when editing records.                         |                                            |
+---------------------+-----------------------------------------------+--------------------------------------------+
| welcome_page.html   | Navigation page used to direct users to the   | .. image:: _static/welcome_html.png        |
|                     |                                               |                                            |
|                     | new, edit, and forthcoming processes.         |                                            |
+---------------------+-----------------------------------------------+--------------------------------------------+
| newpub.html         | Connects to                                   | .. image:: _static/newpub_html.png         |
|                     |                                               |                                            |
|                     | * view.py - newpub                            |                                            |
|                     |                                               |                                            |
|                     | * forms.py - AuthorForm and NewPublication    |                                            |
|                     |                                               |                                            |
|                     | * models.py - Doc and Author                  |                                            |
+---------------------+-----------------------------------------------+--------------------------------------------+
| editpub.html        | Connects to                                   | .. image:: _static/editpub_html.png        |
|                     |                                               |                                            |
|                     |                                               |                                            |
|                     | * views.py - editpub                          |                                            |
|                     |                                               |                                            |
|                     | * forms.py - AuthorForm and UpdatePublication |                                            |
|                     |                                               |                                            |
|                     | * models.py - BeforeAuthor, BeforeDoc         |                                            |
|                     |                                               |                                            |
|                     | * models.py - EditAuthor, EditDoc             |                                            |
+---------------------+-----------------------------------------------+--------------------------------------------+
| updatepub.html      | Connects to                                   | .. image:: _static/updatepub_html.png      |
|                     |                                               |                                            |
|                     |                                               |                                            |
|                     | * views.py - updatepub                        |                                            |
|                     |                                               |                                            |
|                     | * forms - updatepublicationstatus             |                                            |
|                     |                                               |                                            |
+---------------------+-----------------------------------------------+--------------------------------------------+
| __init__.py         | Combines components form the application,     | .. image:: _static/dash_table.png          |
|                     |                                               |                                            |
|                     | and allows for the app to be fully imported   |                                            |
|                     |                                               |                                            |
|                     | into main.py. This file also contains the     |                                            |
|                     |                                               |                                            |
|                     | dash table used to select records for edits.  |                                            |
+---------------------+-----------------------------------------------+--------------------------------------------+
| success_new.html    | Reads from                                    | .. image:: _static/success_new_html.png    |
|                     |                                               |                                            |
|                     |                                               |                                            |
|                     | * sqlite database                             |                                            |
|                     |                                               |                                            |
|                     | * models.py Doc and Author                    |                                            |
+---------------------+-----------------------------------------------+--------------------------------------------+
| success_edit.html   | Reads from                                    | .. image:: _static/success_edit_html.png   |
|                     |                                               |                                            |
|                     | * sqlite database                             |                                            |
|                     |                                               |                                            |
|                     | * models.py BeforeAuthor and BeforeDoc        |                                            |
|                     |                                               |                                            |
|                     | * models.py EditAuthor and EditDoc            |                                            |
|                     |                                               |                                            |
+---------------------+-----------------------------------------------+--------------------------------------------+
| success_update.html | Under construction                            | .. image:: _static/success_update_html.png |
+---------------------+-----------------------------------------------+--------------------------------------------+




####################
Utilities
####################

.. automodule:: app.utility
   :members:
   :show-inheritance:


####################
Views
####################

.. automodule:: app.views  
   :members:  
   :show-inheritance: