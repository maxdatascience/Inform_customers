# Inform_customers
=========================
Customer messaging system
=========================

Inform customer about new features by sending emails

Problem
-------
Customers need to be informed about new features available for them.
System should send automatic emails to customers, it should allow to send event
information (like New Year congratulations and invitations) as well.

Goal
-----
Create View  for list of customers for sending emails.
Create customizable template for each event, store it in the PostgreSQL database.
Send emails by filling out the necessary variables:
  sender email - send@google.com
  sender email SMTP server, SMTP port. Default settings for google.com are done,

Solution
--------
Design necessary Database structure for keeping the clients and email templates.

View 'customer'
****************
Create View in the PostgreSQL database for customers with the following structure

+-----------------------------------------------------+
| id_addr | first_name  |     email    |  email_work  |
|---------|-------------|--------------|--------------|
| integer | varchar(45) | varchar(355) | varchar(355) |
+-----------------------------------------------------+
id_addr -  client unique id
first_name - first name of the client
email - personal client's email
email_work - client's work email

columns could be named differently - in this case correct the program by putting
your column names instead of those mentioned above accordingly.

Table 'email_template'
**********************
Create table 'Template' in the PostgreSQL database for email templates with the
following structure

+--------------------------------------------+
|   id    | templ |   subject    | signature |
|--------------------------------------------|
| integer | text  | varchar(255) |   text    |
+--------------------------------------------+
id - email template unique id
templ - html email template
subject -  subject line for emails
signature -  signature to put in the email

Program module
**************

Set up database connection credentials.
Set up your email connection credentials
Get from PostgreSQL database template and default elements like subject, signature,
  invitation, dates_available for defined company and construct email body
Get from PostgreSQL database list of name, email for sending email
Send personalized email from using google.com service
  For testing purposes using test=True variable with Email class email could
  be send to yourself.

  For class' description and more details please see documentation


Table of content
==================

Table of Contents: Optionally, include a table of contents in order to allow other people to quickly navigate especially long or detailed READMEs.


Installation
------------
 Installation: Installation is the next section in an effective README. Tell other users how to install your project locally. Optionally, include a gif to make the process even more clear for other people.

Usage
-----
Usage: The next section is usage, in which you instruct other people on how to use your project after they’ve installed it. This would also be a good place to include screenshots of your project in action.


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
