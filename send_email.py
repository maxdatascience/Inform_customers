"""Take template and address list from database and send email.

__author__ = 'Max Data'
__email__ = 'max.bigdata@yahoo.com'
__ website__ = ''
__ copyright__ = 'Copyright 2019, Max Data'
__version__ = '1.0'

"""

import smtplib
import ssl
import mimetypes
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import psycopg2


class PostgreSqlDb:
    """Actions necessary to get data from PostgreSQL database.

    :return: Dataset containing selected records
    :rtype: dataset
    """

    def __init__(self, user, password, host='localhost', port='5432',
                 db_='postgres'):
        """Initialize connection to PostgreSQL server database.

        :param user: PostgreSQL server User
        :type user: str
        :param password: PostgreSQL server Password
        :type password: str
        :param host: PosgtgreSQL server name or IP, defaults to
            'localhost'
        :type host: str, optional
        :param port: PosgtgreSQL server port. Defaults to '5432',
            defaults to '5432'
        :type port: str, optional
        :param db_: Database name, defaults to 'postgres'
        :type db_: str, optional
        """
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_ = db_
        self.connection = None
        self.cursor = None

    def disconnect_db(self):
        """Close connection to PostgreSQL server."""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.cursor = None
            self.connection = None
            print("PostgreSQL connection is closed")

    def connect_db(self):
        """Connect to PostgreSQL database.

        Open connection to PostgreSQL server with parameters in the
        object and inform about the version of the database engine
        """
        try:
            self.connection = psycopg2.connect(
                user=self.user, password=self.password,
                host=self.host, port=self.port, db_=self.db_)
            self.cursor = self.connection.cursor()
            # Print PostgreSQL connection properties
            print(self.connection.get_dsn_parameters(), "\n")
            # Print PostgreSQL version
            self.cursor.execute("SELECT version();")
            record = self.cursor.fetchone()
            print("You are connected to - ", record, "\n")
        except psycopg2.Error as error:
            print("Error while connecting to PostgreSQL", error)
            self.disconnect_db()

    def email_list_from_db(
                self, table, firstname_col='first_name',
                email_col='email', work_email_col='work_email',
                condition=None, orderby_col='id'):
        """Extract first_name, email from PostgreSQL database.

        :param table: Table name
        :type table: str
        :param firstname_col: Column name with first name, defaults to
            'first_name'
        :type firstname_col: str, optional
        :param email_col: Column name with email, defaults to 'email'
        :type email_col: str, optional
        :param work_email_col: Column name with work email, defaults to
            'work_email'
        :type work_email_col: str, optional
        :param condition: WHERE clause filter, defaults to None
        :type condition: str, optional
        :param orderby_col: Sort column name, defaults to 'id'
        :type orderby_col: str, optional
        :return: dataset with first name and email or work email
        :rtype: dataset
        """
        try:
            self.connect_db()
            # Get first_name, email from database, if personal email
            # exists get personal one otherwise get work_email
            select = (
                "SELECT {}, COALESCE({}, {}) as email FROM {} \
                {} ORDER BY {}")
            select = select.format(
                firstname_col, email_col, work_email_col, table,
                condition, orderby_col)
            self.cursor.execute(select)
            rows = self.cursor.fetchall()
        except psycopg2.Error as error:
            print("Error while connecting to PostgreSQL", error)
            rows = None
        finally:
            # Close database connection.
            self.disconnect_db()
        return rows

    def email_template(self, table, email_template, id_col_value):
        """Extract email template from PostgreSQL database.

        :param table: Table name with template
        :type table: str
        :param email_template: Column name with template
        :type email_template: str
        :param id_col_value: WHERE clause filter
        :type id_col_value: str
        :return: dataset with email template
        :rtype: dataset
        """
        try:
            self.connect_db()
            # Get template from database with requested id
            select = "SELECT {} FROM {} WHERE {}"
            select = select.format(email_template, table, id_col_value)
            self.cursor.execute(select)
            rows = self.cursor.fetchall()
        except psycopg2.Error as error:
            print("Error while connecting to PostgreSQL", error)
            rows = None
        finally:
            # Close database connection.
            self.disconnect_db()
        return rows


class Email:
    """Actions necessary to create email."""

    def __init__(
            self, smtp='smtp.gmail.com', port=465, from_=None,
            subject='Test', message=None):
        """Initialize email class.

        :param smtp: SMTP host, defaults to 'smtp.gmail.com'
        :type smtp: str, optional
        :param port: SMTP port, defaults to 465
        :type port: int, optional
        :param from_: sender email, defaults to None
        :type from_: str, optional
        :param subject: email subject, defaults to 'Test'
        :type subject: str, optional
        :param message: email body, defaults to None
        :type message: text template, optional
        """
        self.smtp = smtp
        self.port = port
        self.from_ = from_
        self.to_ = None
        self.bcc = None
        self.subject = subject
        self.message = message

    def add_section(
            self, section='Multipart', subtype='html', msg=None,
            image=None, image_type=None, image_filename=None):
        """Add part into multipart email message.

        :param section: type of part email message to add, defaults to
            'Multipart'
        :type section: str, optional
        :param subtype: body message type, defaults to 'html'
        :type subtype: str, optional
        :param msg: contend of the message, defaults to None
        :type msg: str, optional
        :param image: image file name, defaults to None
        :type image: str, optional
        :param image_type: content of image file, defaults to None
        :type image_type: str, optional
        :param image_filename: image file name, defaults to None
        :type image_filename: str, optional
        """
        if section == 'Multipart':
            self.message = MIMEMultipart()
            self.message['To'] = self.to_
            self.message['From'] = self.from_
            self.message['Bcc'] = self.bcc   # used for mass emails
            self.message['Subject'] = self.subject
        if (section == 'Text') and (subtype == 'html'):
            # msg.attach(MIMEText(message, 'plain'))
            self.message.attach(MIMEText(msg, 'html'))
        if section == 'Image':
            tempvar = MIMEImage(image, _subtype=image_type)
            tempvar.add_header('Content-ID', '<image_filename>')
            tempvar.add_header(
                'Content-Disposition', 'inline',
                filename=image_filename)
            self.message.attach(tempvar)

    def email_create(self, email_to, email_bcc, test_add, test=True):
        """Create Base part of email message, filling the Header.

        :param email_to: receiver email
        :type email_to: str
        :param email_bcc: blind carbon copy receiver
        :type email_bcc: str
        :param test_add: suffix add to email for testing with google
        :type test_add: str
        :param test: mode to run function, defaults to True
        :type test: bool, optional
        """
        if test:
            tempvar = list(self.from_.partition('@'))
            tempvar.insert(1, ''.join('+{}'.format(test_add)))
            self.to_ = ''.join(tempvar)
        else:
            self.to_ = email_to
        self.bcc = email_bcc
        self.add_section()

    def process_name_email(
            self, email_password, name_email, signature,
            image_filename, message_template_html):
        """Form and send email for each row.

        :param email_password: sender password
        :type email_password: str
        :param name_email: name and email, defaults to None
        :type name_email: dataset, optional
        :param signature: signature in the email template
        :type signature: text
        :param image_filename: image file name
        :type image_filename: str
        :param message_template_html: contend of the message template
        :type message_template_html: text
        """
        for i, row in enumerate(name_email):
            # create message
            print("      {}: {}".format(i, row[:2]))
            self.email_create(
                email_to=row[1], email_bcc=self.from_,
                test=False, test_add=row[0],)
            message_html = message_template_html.substitute(
                PERSON_NAME=row[0].title(), SIGNATURE=signature)
            self.add_section('Text', 'html', msg=message_html)

            # Attach image file to email (inline)
            with open(image_filename, "rb") as img:
                contenttype, content_subtype = (
                    mimetypes.guess_type(img.name)[0].split('/'))
                self.add_section(
                    'Image', image=img.read(),
                    image_type=content_subtype,
                    image_filename=image_filename)

            # Create secure SSL context
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(
                    self.smtp, self.port, context=context) as server:
                server.login(self.from_, email_password)
                server.sendmail(
                    self.from_, self.to_, self.message.as_string())


def main():
    """Execute main module."""
    # Set up database connection credentials
    user = "postgres"
    password = input("Enter your Database pass, please: ")
    host = "localhost"
    port = "5433"
    db_ = "crm"

    # Set up your email connection credentials
    sender_email = input("Type your (sender) email address here: ")
    email_password = input(
        "Enter your %s password, here:" % sender_email)
    image_filename = 'NY.gif'  # Image file for attachment in email
    subject = 'Happy New Year!'
    signature = """\
        ***<br>
        """

    # Get email template from database by id
    postgresql_db = PostgreSqlDb(user, password, host, port, db_)
    email_template = postgresql_db.email_template(
        'email_template', 'templ', 'id = 3')
    print("Email message template...")
    if email_template:
        message_template_html = Template(email_template[0][0])

    # Get first name, personal email if exists otherwise work email
    name_email = postgresql_db.email_list_from_db(
        'lead', 'first_name', 'email', 'email_work',
        "WHERE (email is NOT NULL OR email_work is NOT NULL)",
        'id_addr')
    print("Proceed with the dataset...")

    if name_email:
        email_msg = Email(from_=sender_email, subject=subject)

        email_msg.process_name_email(
            email_password, name_email, signature, image_filename,
            message_template_html)


if __name__ == "__main__":
    main()
