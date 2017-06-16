# from role import Role
# from user import User, AnonymousUser
# from order import Order
from elasticsearch_dsl.connections import connections


class ElasticDB():
    # Define a default Elasticsearch client
    connections.create_connection(hosts=[{'host': 'localhost', 'port': 9200}])

    @classmethod
    def init_app(cls, app):
        pass
        # Use difference database for dev, test and production
        # index = app.config['ES_DATABASE_INDEX']
        # User._doc_type.index = index
        # Order._doc_type.index = index
        # Role._doc_type.index = index
        # try:
        #     User._doc_type.mapping.save(index)  # refresh mapping
        #     Order._doc_type.mapping.save(index)
        #     Role._doc_type.mapping.save(index)
        # except Exception:
        #     User.init()  # create mapping
        #     Order.init()
        #     Role.init()
