from unittest import TestCase
from BookReviewFromScratch import user
from datetime import datetime
import subprocess
import random
import string
import os

class TestUser(TestCase):

    def setUp(self):
       user.clear_users()

    def tearDown(self):
        user.clear_users()

    def test_register(self):
        registered_user = user.register("foo", "bar", "bar", "30/12/1980")

        self.assertDictEqual(registered_user,  {"username": "foo", "password": "bar", "dateOfBirth": "30/12/1980"})

        # test register with user name who already exist 
        self.assertRaises(user.UserAlreadyExist, user.register, "foo", "password", "password", "30/12/1980")

        # test register user with password missmatch 
        self.assertRaises(user.PasswordMissmatch, user.register, "favw", "password", "passwOrd", "30/12/1980")


    def test_login(self):
        # first register user
        registered_user = user.register("user1", "user1password", "user1password", "30/12/1980")
        self.assertEqual(registered_user, user.login("user1", "user1password"))

        # test login with invalid password
        self.assertRaises(user.InvalidPassword, user.login, "user1", "wrongPassword")

        # test login with user who does not exist
        self.assertRaises(user.InvalidUsername, user.login, "bar",  "bar")
    
    def test_register_with_invalid_date(self):
        # test invalid date of birth 
        self.assertRaises(user.InvalidDateOfBirth, user.register, "favw", "password", "password", "invalid_date") 

class TestUserArePersisted(TestCase):

    def setUp(self):
       user.clear_users()

    def tearDown(self):
        user.clear_users() 

    def test_user_registration_and_login_persists_data(self):
        # register user via command line 
        random_username = ''.join(random.choices(string.ascii_lowercase, k = 5))
        password, dateOfBirth = "bar", "30/12/1970"
        results = subprocess.run([
            "python", 
            "BookReviewFromScratch/manage.py",
            "user_register", 
            f"--username={random_username}",
            f"--password={password}", 
            f"--password2={password}",
            f"--dateOfBirth={dateOfBirth}"], stdout=subprocess.PIPE)
        
        self.assertEqual(0, results.returncode)

        # now check the user is registered
        self.assertDictEqual(
            {
                "username": random_username,
                "password": password,
                "dateOfBirth": dateOfBirth
                },
                 user.login(random_username, password))


        # check registering the same user fails
        self.assertRaises(user.UserAlreadyExist, user.register, random_username, password, password, dateOfBirth)

        # test login with invalid passowrd fails
        results = subprocess.run([
                    "python",
                    "BookReviewFromScratch/manage.py",
                    "user_login",
                    f"--username={random_username}",
                    f"--password={password}_invalid_password",
                    ], stdout=subprocess.PIPE)
        self.assertEqual(1, results.returncode)

        # test login with valid password
        results = subprocess.run([
                    "python",
                    "BookReviewFromScratch/manage.py",
                    "user_login",
                    f"--username={random_username}",
                    f"--password={password}",
                    ], stdout=subprocess.PIPE)
        self.assertEqual(0, results.returncode)