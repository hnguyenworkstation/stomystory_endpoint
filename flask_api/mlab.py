import mongoengine

# mongo ds133192.mlab.com:33192/stomystory -u <dbuser> -p <dbpassword>
host = "ds133192.mlab.com"
port = 33192
db_name = "stomystory"
username = "1"
password = "1"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=username, password=password)


def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())
