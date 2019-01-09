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

api = Namespace("User API", description="The aggregated symptoms api endpoints")

class DbHandler(object):
    def __init__(self):
        pass

    def return_averages(self):
        doc = {
            "aggs": {
                "by_userid": {
                    "terms": {
                        "field": "_user"
                    },
                    "aggs": {
                        "overall": {
                            "avg": {
                                "field": "overall",
                                "missing": 0
                            }
                        },
                        "swelling_of_feed": {
                            "avg": {
                                "field": "swelling_of_feed",
                                "missing": 0
                            }
                        },
                        "pain_other": {
                            "avg": {
                                "field": "pain_other",
                                "missing": 0
                            }
                        },
                        "blood_in_urine": {
                            "avg": {
                                "field": "blood_in_urine",
                                "missing": 0
                            }
                        },
                        "pain_whilst_sitting": {
                            "avg": {
                                "field": "pain_whilst_sitting",
                                "missing": 0
                            }
                        },
                        "weight_loss": {
                            "avg": {
                                "field": "weight_loss",
                                "missing": 0
                            }
                        },
                        "burning_during_urination": {
                            "avg": {
                                "field": "burning_during_urination",
                                "missing": 0
                            }
                        },
                        "fatigue": {
                            "avg": {
                                "field": "fatigue",
                                "missing": 0
                            }
                        },

                    }
                }
            }
        }
        try:
            scroll = "1m"
            response = es.search(index="symptoms-index", doc_type="symptom", body=doc, scroll=scroll)
            return response["aggregations"]["by_userid"]["buckets"]
        except:
            return []


DbOps = DbHandler()

@api.route("/averages")
class aggregate(Resource):
    def get(self):
        avgs = DbOps.return_averages()
        return avgs, 200