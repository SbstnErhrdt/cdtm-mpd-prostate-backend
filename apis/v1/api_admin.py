from flask import request, jsonify
from flask_restplus import Namespace, Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
from services.elastic_search import es

api = Namespace("Admin API", description="The Admin api endpoints")


class DbHandler(object):
    def __init__(self):
        pass

    @staticmethod
    def create_default_admin(data):
        data["roles"] = {
            "admin": True
        }

        data["password"] = generate_password_hash(data["password"].encode())

        doc = {
            'size': 10000,
            'query': {
                'match_all': {}
            }
        }
        scroll = "1m"
        try:
            response = es.search(index="users-index", doc_type="user", body=doc, scroll=scroll, id="default_admin")
            if response["hits"]["total"] > 0:
                # Admin already exists
                print("Admin already exists")
                return
        except:
            print("Create new default admin user")

        # create the new user
        resp = es.index(index="users-index", doc_type="user", body=data, id="default_admin")
        return resp

    def create_admin(self, data):
        resp = es.index(index="users-index", doc_type="user", body=data)
        return resp

    def get_all_admins(self):
        doc = {
            'size': 10000,
            'query': {
                'match_all': {}
            }
        }
        scroll = "1m"
        try:
            response = es.search(index="users-index", doc_type="user", body=doc, scroll=scroll)
        except:
            return []

        if response["hits"]["total"] > 0:
            for user in response["hits"]["hits"]:
                user["_source"].pop("password")

        return response["hits"]["hits"]

    def delete_all(self):

        q = {
            "query": {
                "match_all": {}
            }
        }
        es.delete_by_query(index="users-index", doc_type="user", body=q)

    def get_admin_by_name(self, name):
        q = {
            "query": {
                "bool": {
                    "must": [
                        {"match_phrase": {"name": name}}
                    ]
                }
            }
        }
        scroll = "1m"
        try:
            response = es.search(index="users-index", doc_type="user", body=q, scroll=scroll)
        except:
            return []

        # if response["hits"]["total"] > 0:
        #    for user in response["hits"]["hits"]:
        #        user["_source"].pop("password")

        return response["hits"]["hits"]


DbOps = DbHandler()


@api.route("/")
class all_admins(Resource):
    def get(self):
        resp = DbOps.get_all_admins()
        return resp, 400

    def delete(self):
        DbOps.delete_all()
        return {}, 200
