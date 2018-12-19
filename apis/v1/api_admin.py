import os
import uuid
from flask import Flask, request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse
from elasticsearch import Elasticsearch
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, JWTManager)

ES_HOST = os.environ.get('ELASTIC_SERACH_HOST', None)
ES_USERNAME = os.environ.get('ELASTIC_SERACH_USERNAME', None)
ES_PASSWORD = os.environ.get('ELASTIC_SERACH_PASSWORD', None)

es = Elasticsearch(
    [ES_HOST],
    http_auth=(ES_USERNAME, ES_PASSWORD),
    scheme="http",
    port=80,
)

api = Namespace("Admin API", description="The Admin api endpoints")

class DbHandler(object):
    def __init__(self):
        pass

    @staticmethod
    def create_default_admin(data):
        doc = {
            'size': 10000,
            'query': {
                'match_all': {}
            }
        }
        scroll = "1m"
        try:
            response = es.search(index="admins", doc_type="credentials", body=doc, scroll=scroll)
            if response["hits"]["total"] > 0:
                # Admin already exists
                print("already exists")
                return
        except:
            print("nichts")

        resp = es.index(index="admins", doc_type="credentials", body=data)
        return  resp

    def create_admin(self, data):
        resp = es.index(index="admins", doc_type="credentials", body=data)
        return  resp

    def get_all_admins(self):
        doc = {
            'size': 10000,
            'query': {
                'match_all': {}
            }
        }
        scroll = "1m"
        try:
            response = es.search(index="admins", doc_type="credentials", body=doc, scroll=scroll)
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
        es.delete_by_query(index="admins", doc_type="credentials", body=q)

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
            response = es.search(index="admins", doc_type="credentials", body=q, scroll=scroll)
        except:
            return []

        #if response["hits"]["total"] > 0:
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

@api.route("/login")
class login(Resource):
    def post(self):
        payload = request.get_json(force=True)

        if "name" not in payload or "password" not in payload:
            return {"msg":"name/password Missing"}, 400

        name = payload.get('name', None)
        password = payload.get('password', None)

        if not name:
            return jsonify({"msg": "Missing username parameter"}), 400
        if not password:
            return jsonify({"msg": "Missing password parameter"}), 400

        users = DbOps.get_admin_by_name(name)

        if len(users) == 0:
            return {"msg": "Admin " + name + " doesn't exist"}, 400
        elif len(users) > 1:
            return {"msg": "Somehow more than 1 users exist with the same email. WTF!!"}, 400

        #if check_password_hash(users[0]["_source"]["password"], password) is False:
        #    return {"msg": "Wrong email/password"}, 400
        if password != users[0]["_source"]["password"]:
            return {"msg": "Wrong name/password"}, 400
        access_token = create_access_token(identity={"name": users[0]["_source"]["name"], "id": users[0]["_id"], "usertype": "admin"})

        return {"access_token": access_token}, 200
"""
@api.route("/register")
class register(Resource):
    def get(self):
        print(api.payload)
        return "success", 201

    def post(self):
        payload = request.get_json(force=True)

        if "username" not in payload or "password" not in payload or "email" not in payload:
            return {"msg": "username/password/email Missing"}, 400

        username = payload["username"]
        email = payload["email"]
        password = payload["password"]

        # Check if user already exists
        exists_already = DbOps.get_patient_by_email(email)
        if len(exists_already) > 0:
            return {"msg": "User with email " + email + " already exists"}, 400

        data = {
            "username": username,
            "password": password,
            "email": email,
            "age": "",
            "address": "",
            "dob": ""

        }
        print(data)
        if "age" in request.form:
            data["age"] = request.form.get("age")
        if "address" in request.form:
            data["address"] = request.form.get("address")
        if "dob" in request.form:
            data["dob"] = request.form.get("dob")

        resp = DbOps.create_patient(data)
        data.pop("password")
        data["id"] = resp["_id"]
        return data, 201
"""