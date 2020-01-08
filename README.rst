Customer messaging system
=========================
Inform customer about new features by sending emails

**Input:** list of names, emails
       message template, default signature, default subject

**Output:** email message is sent to the customer, example below
      .. image:: pic/email_sent.png

Table of content
==================
- Description
  * Problem
  * Goal
  * Solution
    - View  `customer`
    - Table `email_template`
    - Program module
- Getting Started
- Prerequisites
- Installing

Description
-----------
`Problem`
-----------
Customers need to be informed about new features available for them.
System should send automatic emails to customers, it should allow to send event
information (like New Year congratulations and invitations) as well.

`Goal`
------
Create View  for list of customers for sending emails.
Create customizable template for each event, store it in the PostgreSQL database.
Send emails by filling out the necessary variables:
  sender email - send@google.com
  sender email SMTP server, SMTP port. Default settings for google.com are done,

`Solution`
-----------
Design necessary Database structure for keeping the clients and email templates.

View `customer`
-----------------
Create View in the PostgreSQL database for customers with the following structure

+-----------------------------------------------------+
| id_addr | first_name  |     email    |  email_work  |
|---------|-------------|--------------|--------------|
| integer | varchar(45) | varchar(355) | varchar(355) |
+-----------------------------------------------------+

- **id_addr** client unique id
- **first_name** first name of the client
- **email** personal client's email
- **email_work** client's work email

columns could be named differently - in this case correct the program by putting
your column names instead of those mentioned above accordingly.

Table `email_template`
------------------------
Create table `email_template` in the PostgreSQL database for email templates with the
following structure

+--------------------------------------------+
|   id    | templ |   subject    | signature |
|--------------------------------------------|
| integer | text  | varchar(255) |   text    |
+--------------------------------------------+

- **id** email template unique id
- **templ** html email template
- **subject** subject line for emails
- **signature** signature to put in the email

- - Sample template (column 'templ')
-------------------------------------
- - <html>
- -    <head></head>
- -    <body>
- -        <p>
- - Dear ${PERSON_NAME},<br>
- - <br>
- - It is New Year time!<br>
- - Have a fun and unforgettable moments<br>
- - with your family and friends.<br><br>
- - Happy New Year!!!<br><br>
- - <img src="cid:image_filename"><br>
- - ${SIGNATURE}<br>
- -         </p>
- -     </body>
- - </html>

- - Sample subject (column 'subject')
--------------------------------------
- - Happy New Year!!!

- - Sample signature (column 'signature')
-----------------------------------------
- - ***<br>
- - Sincerely,<br>
- - Test sender<br>
- - Contacts<br>

- Program module
-----------------
Set up database connection credentials.
Set up your email connection credentials
Get template and default elements like subject, signature from PostgreSQL database
Get list of name, email for sending email from PostgreSQL database
Construct personalized email for everybody on the list
Send personalized email using gmail.com service
  For testing purposes use test=True variable with Email class to send email to yourself

  For class' description and more details please see documentation

Getting Started
---------------
These instructions will get you a copy of the project up and running on your
local machine for development and testing purposes.
See deployment part for notes on how to deploy the project on a live system.

Prerequisites
-------------
- Linux - Ubuntu
- GitHub
- Python v 3.x
- pip (package manager)
- Virtual environment package 'venv' to distinguish the project from other ones
- PostgreSQL (v12.1 preferably)
- PgAdmin 4
- Gmail account (default) or other email account and necessary information to set up it
- Terminal

Installing
----------
Feel free to skip the step if you already have the tool installed

- Install and Run GitHub
  ```
  sudo apt-get update
  sudo apt-get install git
  ```
  verify the installation was successful by typing 'github --version'
  .. image:: pic/git_install.png

- **Install Python 3**

  Python 3 is already installed in Linux
  verify the installation by typing 'python3 --version'
  .. image:: pic/python3.png

- Install package manager 'pip'
*******************************
  ```
  sudo apt-get update
  sudo apt-get install python3-pip
  ```
  verify the installation was successful by typing 'pip --version'
  .. image:: pic/pip.png

- Install virtual environment package
*************************************
  ```
  sudo apt-get install python3-venv
  ```
- Create virtual environment for project and activate it
********************************************************
  ```
  python -m venv ./venv/project-folder
  source bin/activate
  ```
  as the virtual environment is activated you'll see the name of your environment
  first in the commmand prompt like where 'send_email' is the name of the virtual
  environment
  .. image:: pic/venv.png

- Set up and Run PostgreSQL
***************************
  Follow the process described here_:
  .. _here: https://www.postgresql.org/docs/current/

  verify the installation was successful by typing 'psql --version'
  .. image:: pic/postgresql.png

- Set up PgAdmin 4
******************
  Follow the process described here_:
  .. _here: https://www.pgadmin.org/docs/pgadmin4/4.16/index.html

  verify the installation was successful by typing 'pgAdmin4'. it start the pgAdmin4 server
  .. image:: pic/pgadmin4.png

- Text editor
*************
  Use the one you love or you can install atom
  ```
  pip install atom
  ```
  verify the installation was successful by typing 'atom --version'
  .. image:: pic/atom.png

- Clone repository from GitHub to your environment
**************************************************
  ```
  git clone link-to-repository
  ```
  verify that you have the project in your folder you should see something like
  .. image:: pic/gitclone.png

- Create PostgreSQL Database with Views an Tables mentioned in the 'Solution' part
**********************************************************************************
  Run pgAdmin4 and create database, tables and Views
    Follow the process described in documentation_:
    .. _documentation: https://www.pgadmin.org/docs/pgadmin4/4.16/index.html

- Make sure the Tables and Views contain necessary data to work with
*********************************************************************
  Run pgAdmin4 and execute SQL statement
  ```
  SELECT *
  FROM customer
  LIMIT 1;
  ```
  The query should return 1 row
  ```
  SELECT *
  FROM email_template
  LIMIT 1;
  ```
  The query should return 1 row

- Install necessary packages from 'requirements.txt'
****************************************************
  ```
  pip install -r Inform_customers/requirements.txt
  ```

Congratulations, your environment is ready to test!!!
-----------------------------------------------------

Run tests to check everything is working properly


End with an example of getting some data out of the system or using it for a little demo

Contributing
------------
Contributing: Larger projects often have sections on contributing to their project, in which contribution instructions are outlined. Sometimes, this is a separate file. If you have specific contribution preferences, explain them so that other developers know how to best contribute to your work. To learn more about how to help others contribute, check out the guide for setting guidelines for repository contributors.

Credits
-------
Credits: Include a section for credits in order to highlight and link to the authors of your project.

License
-------
License: Finally, include a section for the license of your project. For more information on choosing a license, check out GitHub’s licensing guide!


To do
-----
Indclude columns into database: image_filename varchar(50), image blob (image file)
