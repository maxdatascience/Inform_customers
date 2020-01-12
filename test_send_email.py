"""Module of unit tests for Send-email module.

__author__ = 'Max Luckystar'
__email__ = 'data.maxluckystar@gmail.com'
__ website__ = ''
__ copyright__ = 'Copyright 2019, Max Luckystar'
__version__ = '1.0'

"""

import unittest
from string import Template
from send_email import PostgreSqlDb
from send_email import Email
# import send_email


class TestSendEmail(unittest.TestCase):
    def test_main(self):
        # result = send_email()
        # self.assertEqual(result, )
        # with self.assertRaises(ValueError):
        #     __init__()
        # with self.assertRaises(ValueError):
        #     __init__()
        pass


class TestPostgreSqlDb(unittest.TestCase):
    passw = input("Enter your Database password: ")
    val_test = 'Test'
    val_templ = 'Test. Dear ${PERSON_NAME}, ${SIGNATURE} end.'
    val_test_emails = ['Test@Test.com', 'Testwork@Test.com']

    @classmethod
    def setUpClass(cls):
        print('\nsetupClass')

    @classmethod
    def tearDownClass(cls):
        print('\ntearDownClass\n')

    def setUp(self):
        self.connection_posgtresql_1 = PostgreSqlDb(
            'postgres', 'postgrespass', 'localhost', '5433', 'crm')
        self.connection_posgtresql_2 = PostgreSqlDb(
            'postgres', self.passw, 'localhost', '5433', 'crm')
        print('\nsetUp **********************')

    def tearDown(self):
        print('\ntearDown **********************\n\n\n')

    def test_connect_db(self):
        print('\n----------- Test_1 PostgreSqlDb.connect_db\n')
        # connect with default credentials
        self.assertIsNone(
            PostgreSqlDb.connect_db(self.connection_posgtresql_1))
        print('\n----------- Test_2 PostgreSqlDb.connect_db\n')
        # connect with entered credentials
        self.assertIsNone(
            PostgreSqlDb.connect_db(self.connection_posgtresql_2))

    def test_disconnect_db(self):
        print('\n----------- Test_1 PostgreSqlDb.disconnect_db\n')
        # disconnect after been connected
        PostgreSqlDb.connect_db(self.connection_posgtresql_1)
        self.assertIsNone(
            PostgreSqlDb.disconnect_db(self.connection_posgtresql_1))
        print('\n----------- Test_2 PostgreSqlDb.disconnect_db\n')
        # disconnect without been connected
        self.assertIsNone(
            PostgreSqlDb.disconnect_db(self.connection_posgtresql_1))

    def test_email_template(self):
        print('\n----------- Test_1 PostgreSqlDb.email_template\n')
        row = self.connection_posgtresql_1.email_template(
            'email_template', 'templ, subject, signature', 'id = 1')
        self.assertEqual(row[0][0], self.val_templ)

        print('\n----------- Test_2 PostgreSqlDb.email_template\n')
        row = self.connection_posgtresql_1.email_template(
            'email_template', 'templ', 'id = 1')
        self.assertEqual(row[0][0], self.val_templ)

    def test_email_list_from_db(self):
        print('\n----------- Test_1 PostgreSqlDb.email_list_from_db\n')
        row = self.connection_posgtresql_1.email_list_from_db(
            'lead', 'first_name', 'email', 'email_work',
            "WHERE (email is NOT NULL OR email_work is NOT NULL) and"
            + " id_addr=1", 'id_addr')
        self.assertEqual(row[0][0], self.val_test)
        self.assertIn(row[0][1], self.val_test_emails)

        print('\n----------- Test_2 PostgreSqlDb.email_list_from_db\n')
        row = self.connection_posgtresql_1.email_list_from_db(
            'lead', 'first_name', 'email', 'email_work',
            "WHERE (email is NOT NULL OR email_work is NOT NULL) and"
            + " id_addr = 1", 'id_addr')
        self.assertEqual(row[0][0], self.val_test)
        self.assertIn(row[0][1], self.val_test_emails)


class TestEmail(unittest.TestCase):
    test_name_email = [('Test', 'Test@Test.com')]
    test_email = 'Test@Test.com'
    # input("Enter your @gmail.com email: ")
    email_passw = input("Enter your %s password: " % test_email)

    def setUp(self):
        print('\nsetUp **********************')
        self.email_1 = Email(
            'Test@Test.com', 'smtp.gmail.com', 465, 'Test', 'Test')
        # set unassigned values only
        self.email_2 = Email(from_='Test@Test.com', message='Test')

    def tearDown(self):
        print('\ntearDown **********************\n\n\n')

    # def test_add_section(self):
    #     image = img.read()
    #     image_type = content_subtype
    #     image_filename = image_filename
    #     self.emil_1.add_section()
    
    #     self.email_1.add_section(
    #         'Text', 'html', 'Test. Dear Test, TestSignature end.')
    #     self.email_1.add_section(
    #         'Image', image, image_type, image_filename)




    #     self.email_2.add_section(
    #         'Text', 'html', 'Test. Dear Test, TestSignature end.')
    #     self.email_2.add_section(
    #         'Image', image, image_type, image_filename)


    def test_email_create(self):
        self.email_1.email_create('Test@Test.com', 'Test@Test.com',
        'Test', True)

    # def test_process_name_email(self):
    #     pass
        # image = 'NY.gif'
        # message_template = Template(
        #     'Test. Dear ${PERSON_NAME}, ${SIGNATURE} end.')
        # test_signature = 'TestSignature'
        # self.email_1.process_name_email(
        #     self.email_passw, self.test_name_email, test_signature,
        #     image, message_template, True)
        # # call with unassigned values only
        # self.email_2.process_name_email(
        #     self.email_passw, self.test_name_email, test_signature,
        #     image, message_template)


if __name__ == "__main__":
    unittest.main()
