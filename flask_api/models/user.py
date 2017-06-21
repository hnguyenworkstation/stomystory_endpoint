from mongoengine import *

import mlab


class User(Document):
    username = StringField(unique=True, required=True, min_length=6)
    password = StringField(min_length=8, required=True)


    def get_json(self):
        return mlab.item2json(self)