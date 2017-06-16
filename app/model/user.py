# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,\
#     BadSignature, SignatureExpired
# from flask import current_app
# from flask_login import UserMixin, AnonymousUserMixin
# from elasticsearch_dsl import DocType, InnerObjectWrapper, \
#     Date, Nested, Keyword, Text, Boolean, GeoPoint, Integer
# from . import Role


# class User_searchable(DocType):
#     '''
#     Search on user fuzzy search, full-text search
#     '''
#     first_name = Text(fields={'raw': Keyword()})
#     last_name = Text(fields={'raw': Keyword()})
#     id = Text()


# class User(DocType, UserMixin):
#     ''' User class using elasticsearch '''
#     # email is unique identity of user
#     email = Text(required=True)
#     password_hash = Text(required=True, index='no')

#     # user name and role
#     first_name = Text(analyzer='snowball', fields={'raw': Keyword()})
#     last_name = Text(analyzer='snowball', fields={'raw': Keyword()})
#     role_id = Text(index='no')

#     # Basic info
#     about_me = Text(analyzer='snowball', fields={'raw': Keyword()})
#     address = Nested(
#         doc_class=InnerObjectWrapper,
#         properties={
#             'location': GeoPoint(index='not_analyzed'),
#             'city': Text(),
#             'state': Text(),
#             'zip_code': Integer(),
#         })

#     # system related variables
#     verified = Boolean()
#     banned = Boolean()
#     member_since = Date()
#     last_seen = Date()

#     @staticmethod
#     def generate_fake(count=100):
#         from random import seed
#         import forgery_py

#         seed()
#         for i in range(count):
#             u = User(first_name=forgery_py.name.first_name(),
#                      last_name=forgery_py.name.last_name())
#             u.email = forgery_py.internet.email_address()
#             # username = forgery_py.internet.user_name(True)
#             u.password = forgery_py.lorem_ipsum.word()
#             u.location = forgery_py.address.city()
#             u.about_me = forgery_py.lorem_ipsum.sentence()
#             u.member_since = forgery_py.date.date(True)
#             u.verified = True
#             u.active = True
#             try:
#                 u.save()
#             except Exception:
#                 u.delete()

#     @property
#     def password(self):
#         raise AttributeError('password is not a readable attribute')

#     @password.setter
#     def password(self, password):
#         self.password_hash = generate_password_hash(password)

#     def verify_password(self, password):
#         return check_password_hash(self.password_hash, password)

#     def save(self, role='user', ** kwargs):
#         # some default values
#         self.member_since = self.member_since or datetime.now()
#         try:
#             self.role_id = self.role_id or \
#                 Role.search().query('match', name=role).execute()[0].id
#         except Exception:
#             pass
#         return super(User, self).save(** kwargs)

#     def generate_token(self, expiration=600):
#         '''
#         generate authentication token
#         '''
#         s = Serializer(current_app.config['SECRET_KEY'], expiration)
#         return s.dumps({'id': self.meta.id})

#     @staticmethod
#     def verify_auth_token(token):
#         s = Serializer(current_app.config['SECRET_KEY'])
#         try:
#             data = s.loads(token)
#         except SignatureExpired:
#             return None  # valid token, but expired
#         except BadSignature:
#             return None  # invalid token
#         return User.get(data['id'], ignore=404)

#     def __repr__(self):
#         return '<User %r>' % self.email


# class AnonymousUser(AnonymousUserMixin):
#     def can(self, permissions):
#         return False

#     def is_administrator(self):
#         return False

#     def is_active(self):
#         return False
