from typing import List
from datetime import datetime
import csv
from copy import deepcopy


# exception throw when username does not exist 
class InvalidUsername(Exception):
    pass 

# exception throw when password is invalid
class InvalidPassword(Exception):
    pass 

# exception throw when registering a user who already exist
class UserAlreadyExist(Exception):
    pass 


# exception thrown when registering a user with password missmatch i.e password 1 and 2 are not same 
class PasswordMissmatch(Exception):
    pass 


class InvalidDateOfBirth(Exception):
    pass 

def update_users_file(users):
    with open("users.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile)

        # writting fields
        csvwriter.writerow(["username", "password", "dateOfBirth"])

        # write now the user details
        for key, value in users.items():
            csvwriter.writerow([key, value["password"], value["dateOfBirth"]])

def get_users():
    users = {}
    with open("users.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)

        for row in csvreader:
            users[row[0]] = {"password": row[1], "dateOfBirth": row[2]}
    return users


def clear_users():
    """ only used when running tests"""
    update_users_file({})

def login(username: str, password: str) -> dict:
    """ 
        Returns user details if user exist else returns None
    """
    user = get_users().get(username)
    if user is None:
        raise InvalidUsername(f"user {username} does not exist")
    if password != user['password']:
        raise InvalidPassword("You provided invalid password")
    results = deepcopy(user)
    results['username'] = username
    return results

def register(username: str, password: str, password2: str, dateOfBirth: str):
    """
    if user exist return error saying user already exist

    if password1 and password2 are equal and username does not exist it will create
    a new user on our user dictionary and return user.

    if password1 and password2 is not equal raise an error.
    """
    users = get_users()
    if users.get(username) is not None:
        raise UserAlreadyExist(f"User {username} already exist")
    if password != password2:
        raise PasswordMissmatch("password one and two don't match")

    try:
        datetime.strptime(dateOfBirth, "%d/%m/%Y")
    except Exception as e:
        raise InvalidDateOfBirth("Invalid date of birth")

    users[username] = {"password": password, "dateOfBirth": dateOfBirth}

    # now write the users back to the file
    update_users_file(users)

    results = deepcopy(users[username])
    results['username'] = username
    return results

def list_users() -> List:
    pass 

if __name__ == '__main__':
    """ You can put your testing logic here """
    pass 