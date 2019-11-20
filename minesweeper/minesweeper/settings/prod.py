import django_heroku
from .base import *

DEBUG = False

django_heroku.settings(locals())
