# pylint: disable=missing-module-docstring
# pylint: disable=import-error
import os
import pymongo
from dotenv import load_dotenv
from crypto import encrypt, decrypt

load_dotenv()

client = pymongo.MongoClient(os.getenv('CONNECTION'))
db = client.password_saver
users = db["Users"]


def add_user(user_id):
    users.insert_one({'id': user_id})


def check_user(user_id):
    if users.find_one({'id': user_id}):
        return True
    return False


def insert_password(user_id, service_name, login, password):
    password = encrypt(password)
    users.update_one({ 'id': user_id },{ '$set' : { f'passwords.{service_name}.{login}': password }}, upsert=True)


def get_password(user_id, service_name):
    req = users.find_one({'id': user_id, f'passwords.{service_name}': {'$exists': True}})
    if req:
        accounts = req['passwords'][service_name]
        out = ''
        for login in accounts:
            out += (f'{login} : {decrypt(accounts[login])}\n')
        return out
    return []


def delete_password(user_id, service_name):
    if get_password(user_id, service_name) == {}:
        return False
    users.update_one({ 'id': user_id },{ '$unset' : { f'passwords.{service_name}': "" }})
    return True

# delete_password('123', 'apple')


# print(get_password('123123094', 'apple'))

# print(check_user('123'))

# insert_password(432274703, 'vk', 'elmiringos', '134')