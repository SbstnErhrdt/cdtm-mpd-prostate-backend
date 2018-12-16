import os
import uuid
from flask import Flask, request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse
from elasticsearch import Elasticsearch
from werkzeug.security import generate_password_hash, check_password_hash

ES_HOST = os.environ.get('ELASTIC_SERACH_HOST', None)
ES_USERNAME = os.environ.get('ELASTIC_SERACH_USERNAME', None)
ES_PASSWORD = os.environ.get('ELASTIC_SERACH_PASSWORD', None)

es = Elasticsearch(
    [ES_HOST],
    http_auth=(ES_USERNAME, ES_PASSWORD),
    scheme="http",
    port=80,
)

api = Namespace("Generic API", description="The generic api endpoints")

class DbHandler(object):
    def __init__(self):
        pass

    def create_patient(self, data):
        resp = es.index(index="patients", doc_type="bio", body=data)
        return resp

    def create_admin(self, data):
        resp = es.index(index="admins", doc_type="credentials", body=data)
        return  resp

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

    def get_patient_info(self, email, name):
        q = {
            "query": {
                "bool": {
                    "must": [
                            {"match_phrase": {"email": email}},
                            {"match_phrase": {"username": name}}
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

        if response["hits"]["total"] > 0:
            for user in response["hits"]["hits"]:
                user["_source"].pop("password")

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

    #def get_patient(self):
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
        resp = DbOps.get_all_patients()
        return resp, 200

@api.route("/login")
class login(Resource):
    def post(self):
        if "email" not in request.form.keys() or "password" not in request.form.keys():
            return "email/password Missing", 400

        return jsonify({"hello":" create"})

@api.route("/register")
class register(Resource):
    def get(self):
        print(api.payload)
        return "success", 201

    def post(self):
        if "username" not in request.form.keys() or "password" not in request.form.keys() or "email" not in request.form.keys():
            return "username/password/email Missing", 400

        # TODO: Check that user already doesn't exist
        exists_already = DbOps.get_patient_by_email(request.form["email"])
        if len(exists_already) > 0:
            return "User Already exists", 400

        for user in exists_already:
            if user["_source"]["email"].lower() == request.form["email"].lower():
                return "User Already exists", 400

        data = {
            "username": request.form["username"],
            "password": generate_password_hash(request.form["password"]),
            "email": request.form["email"],
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