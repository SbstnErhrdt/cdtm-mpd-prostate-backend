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

api = Namespace("User API", description="The User api endpoints")

class DbHandler(object):
    def __init__(self):
        pass

    def create_patient(self, data):
        resp = es.index(index="patients", doc_type="bio", body=data)
        return resp

    def get_all_patients(self):
        doc = {
            'size': 10000,
            'query': {
                'match_all': {}
            }
        }
        scroll = "1m"
        try:
            response = es.search(index="patients", doc_type="bio", body=doc, scroll=scroll)
        except:
            return []

        if response["hits"]["total"] > 0:
            for user in response["hits"]["hits"]:
                user["_source"].pop("password")

        return response["hits"]["hits"]


    def get_patient_by_email(self, email):
        q = {
            "query": {
                "bool": {
                    "must": [
                            {"match_phrase": {"email": email}}
                        ]
                    }
                }
            }
        scroll = "1m"
        try:
            response = es.search(index="patients", doc_type="bio", body=q, scroll=scroll)
        except:
            return []

        #if response["hits"]["total"] > 0:
        #    for user in response["hits"]["hits"]:
        #        user["_source"].pop("password")

        return response["hits"]["hits"]

    def get_patient_by_guid(self, guid):
        q = {
            "query": {
                "bool": {
                    "must": [
                            {"match": {"_id": guid}}
                        ]
                    }
                }
            }
        scroll = "1m"
        try:
            response = es.search(index="patients", doc_type="bio", body=q, scroll=scroll)
        except:
            return []

        if response["hits"]["total"] > 0:
            for user in response["hits"]["hits"]:
                user["_source"].pop("password")

        return response["hits"]["hits"]


DbOps = DbHandler()

@api.route("/email/<email>")
class list_patient_by_email(Resource):
    def get(self, email):
        resp = DbOps.get_patient_by_email(email)
        return resp, 200

@api.route("/guid/<guid>")
class list_patient_by_id(Resource):
    def get(self, guid):
        resp = DbOps.get_patient_by_guid(guid)
        return resp, 200

@api.route("/")
class list_all_patients(Resource):
    def get(self):
        try:
            current_user = get_jwt_identity()
            print(current_user)
        except:
            return {"msg": "Missing authorization header"}, 400

        resp = DbOps.get_all_patients()
        return resp, 200

@api.route("/login")
class login(Resource):
    def post(self):
        payload = request.get_json(force=True)

        if "email" not in payload or "password" not in payload:
            return {"msg":"email/password Missing"}, 400

        email = payload.get('email', None)
        password = payload.get('password', None)

        if not email:
            return jsonify({"msg": "Missing email parameter"}), 400
        if not password:
            return jsonify({"msg": "Missing password parameter"}), 400

        users = DbOps.get_patient_by_email(email)

        if len(users) == 0:
            return {"msg": "User " + email + " doesn't exist"}, 400
        elif len(users) > 1:
            return {"msg": "Somehow more than 1 users exist with the same email. WTF!!"}, 400

        if check_password_hash(users[0]["_source"]["password"], password) is False:
            return {"msg": "Wrong email/password"}, 400

        access_token = create_access_token(identity={"username": users[0]["_source"]["username"], "email": email, "id": users[0]["_id"], "usertype": "patient"})
        return {"access_token": access_token}, 200

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