"""
__author__ = 'Max Data'
__email__ = 'max.bigdata@yahoo.com'
__ website__ = ''
__ copytught__ = 'Copyright 2019, Max Data'
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
    """ Actions necessary to get data from PostgreSQL database

    Returns:
        dataset:  Dataset containing selected records
    """

    def __init__(self, user, password, host='localhost', port='5432',
                 database='postgres'):
        """Initialize connection to PostgreSQL server database

        Args:
            user (str): PostgreSQL server User
            password (str): PostgreSQL server Password
            host (str, optional): PosgtgreSQL server name or IP
            address. Defaults to 'localhost'
            port (str, optional): PosgtgreSQL server port. Defaults to
            '5432'
            database (str, optional): Database name. Defaults to
            'postgres'
        """
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.connection = None
        self.cursor = None

    def disconnect_db(self):
        """Close connection to PostgreSQL server
        """
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.cursor = None
            self.connection = None
            print("PostgreSQL connection is closed")

    def connect_db(self):
        """Open connection to PostgreSQL server with parameters in the
        object and inform about the version of the database engine
        """
        try:
            self.connection = psycopg2.connect(
                user=self.user, password=self.password,
                host=self.host, port=self.port, database=self.database)
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
        """ Extract first name, email into rows dataset according
        to request and close connection returning received dataset.
        If email column is empty take email from column containing work
        email

        Args:
            table (str): Table name in the database
            firstname_col (str, optional): Column name containing the
            first name. Defaults to 'first_name'
            email_col (str, optional): Column name containing email.
            Defaults to 'email'
            work_email_col (str, optional): Column name containing work
            email. Defaults to 'work_email'
            condition (str, optional): WHERE clause to filter records.
            Defaults to None
            orderby_col (str, optional): Column name to sort results.
            Defaults to 'id'

        Returns:
            dataset: Dataset containing Names and emails
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
        """Take email template from the database and return it as
        dataset

        Args:
            table (str): Table name containing templates of emails
            email_template (str): Column containing email template
            id_col_value (str): WHERE clause to filter email template

        Returns:
            dataset: Dataset containing email template
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
    """ Actions necessary to create email
    """

    def __init__(
            self, smtp='smtp.gmail.com', port=465, from_=None,
            subject='Test', message=None):
        """Initialize email class, define connection details, and fill
        out base attributes of the email message. Default SMTP
        connection details are host - google.com and port SSL 465 or
        TLS 587

        Args:
            smtp (str, optional): SMTP host. Defaults to
            'smtp.gmail.com'
            port (int, optional): SMTP port. Defaults to 465
            from_ (str, optional): sender email. Defaults to None
            subject (str, optional): Email subject. Defaults to 'Test'
            message (str, optional): Email body. Defaults to None
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
        """Created parts of the email Multipart - defines Header fields
        of the email message. Text-html - add html body to the email
        message. Image -  embed image into email message.

        Args:
            section (str, optional): Part of message to create.
            Defaults to 'Multipart'-create base message
            subtype (str, optional): Type of email content. Defaults to
            'html'
            msg (str, optional): Message content, body. Defaults to None
            image (str, optional): Image file name. Defaults to None
            image_type (str, optional): Content of image file. Defaults
            to None
            image_filename (str, optional): Image file name. Defaults
            to None
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

    def email_create(self, email_to, email_bcc, test, test_add):
        """ Define the recipient of the email and save it in the object
        selt.to_  The recipient email depend on the test mode. If it is
        False - recipient email is taken from emil_to. If it is True -
        recipient email is based on the self.from_ by adding +test_add
        before @. Used to send email to yourself using google.com
        feature for testing purpose. Then called function to create
        email.

        Args:
            email_to (str): recipient email
            email_bcc (str): blind carbon copy recipient
            test (Boolean): True-test mode, False-production mode
            test_add (str): suffix add to email for test purpose
        """
        if test:
            tempvar = list(self.from_.partition('@'))
            tempvar.insert(1, ''.join('+{}'.format(test_add)))
            self.to_ = ''.join(tempvar)
        else:
            self.to_ = email_to
        self.bcc = email_bcc
        self.add_section()


if __name__ == "__main__":
    # Set up database connection credentials
    USER = "postgres"
    PASSWORD = input("Enter your Database password, please: ")
    HOST = "localhost"
    PORT = "5433"
    DATABASE = "crm"

    # Set up your email connection credentials
    SENDER_EMAIL = input("Type your (sender) email address here: ")
    EMAIL_PASSWORD = input(
        "Enter your %s password, here:" % SENDER_EMAIL)
    IMAGE_FILENAME = 'NY.gif'  # Image file for attachment in email
    SUBJECT = 'Happy New Year!'
    SIGNATURE = """\
        ***<br>
        """

    # Get email template from database by id
    POSTGRESQL_DB = PostgreSqlDb(USER, PASSWORD, HOST, PORT, DATABASE)
    EMAIL_TEMPLATE = POSTGRESQL_DB.email_template(
        'email_template', 'templ', 'id = 3')
    print("Email message template...")
    if EMAIL_TEMPLATE:
        MESSAGE_TEMPLATE_HTML = Template(EMAIL_TEMPLATE[0][0])

    # Get first name, personal email if exists otherwise work email
    FIRST_EMAIL = POSTGRESQL_DB.email_list_from_db(
        'lead', 'first_name', 'email', 'email_work',
        "WHERE (email is NOT NULL OR email_work is NOT NULL)",
        'id_addr')
    print("Proceed with the dataset...")

    if FIRST_EMAIL:
        for i, row in enumerate(FIRST_EMAIL):
            # create message
            email_message = Email(from_=SENDER_EMAIL, subject=SUBJECT)
            print("      {}: {}".format(i, row[:2]))
            email_message.email_create(
                email_to=row[1], email_bcc=SENDER_EMAIL,
                test=False, test_add=row[0],)
            messageHtml = MESSAGE_TEMPLATE_HTML.substitute(
                PERSON_NAME=row[0].title(), SIGNATURE=SIGNATURE)
            email_message.add_section('Text', 'html', msg=messageHtml)

            # Attach image file to email (inline)
            with open(IMAGE_FILENAME, "rb") as img:
                contenttype, content_subtype = (
                    mimetypes.guess_type(img.name)[0].split('/'))
                email_message.add_section(
                    'Image', image=img.read(),
                    image_type=content_subtype,
                    image_filename=IMAGE_FILENAME)

            # Create secure SSL context
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(
                    email_message.smtp, email_message.port,
                    context=context) as server:
                server.login(email_message.from_, EMAIL_PASSWORD)
                server.sendmail(
                    email_message.from_, email_message.to_,
                    email_message.message.as_string())
