import uuid
from flask import Flask, request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse
from services.elastic_search import es

api = Namespace("Doctors API", description="The api for doctors")


@api.route("/patients")
class Patients(Resource):
    def get(self):
        """
           Read all generic objects
           :return:
           """
        q = {
            "query": {
                "term": {
                    "roles.patient": True
                }
            }
        }
        scroll = "1m"
        try:
            response = es.search(index="users-index", doc_type="user", body=q, scroll=scroll)
        except:
            return []

        return jsonify(response["hits"]["hits"])


@api.route("/patients/<patientID>")
class Patients(Resource):
    def get(self, patientID):
        try:
            return jsonify(es.get(index="users-index", doc_type="user", id=patientID))
        except:
            return jsonify([])


@api.route("/patients/<patientID>/symptoms")
class PatientsSymptoms(Resource):
    def get(self, patientID):
        q = {
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
            response = es.search(index="symptoms-index", doc_type="symptom", body=q, scroll=scroll)
            return jsonify(response["aggregations"]["by_userid"]["buckets"][0])
        except:
            return jsonify([])
