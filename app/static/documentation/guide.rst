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