from .base import *


with open('secret_key.txt', 'rt') as key:
    SECRET_KEY = key.read()