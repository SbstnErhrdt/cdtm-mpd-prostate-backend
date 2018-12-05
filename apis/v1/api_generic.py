from flask import Flask, request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse
from elasticsearch import Elasticsearch

es = Elasticsearch()

api = Namespace("generic_api", description="generic")


class Generic(object):
    def __init__(self):
        self.data = dict

    def read_all(self, generic_type):
        pass

    def read_single(self, generic_type, uuid):
        pass

    def create(self, generic_type, uuid, data):
        pass

    def update(self, generic_type, uuid, data):
        pass

    def delete(self, generic_type, uuid):
        pass


GEN = Generic()


@api.route("/<str:generic_type>")
class GenericList(Resource):
    @api.doc("create_generic")
    @api.route("/:uuid")
    def post(self, generic_type, uuid):
        """
        Create a new object
        :param generic_type:
        :param uuid:
        :return:
        """
        return jsonify(GEN.create(generic_type, uuid, api.payload)), 201

    @api.doc("list_generic")
    def get(self, generic_type):
        """
        List all
        :return:
        """
        return jsonify(GEN.read_all(generic_type))


@api.route("/<str:generic_type>/<str:uuid>")
@api.param("uuid", "The unique identifier")
class GenericSingle(Resource):
    @api.doc("Generic Single Read")
    def get(self, generic_type, uuid):
        """
        Read single
        :param generic_type:
        :param uuid:
        :return:
        """
        return jsonify(GEN.read_single(generic_type, uuid))

    @api.doc("Generic Update")
    def put(self, generic_type, uuid):
        """
        Update by id
        :param generic_type:
        :param uuid:
        :return:
        """
        return jsonify(GEN.update(generic_type, uuid, api.payload))

    @api.doc("Generic Delete")
    @api.response(204, "Symptom deleted")
    def delete(self, generic_type, uuid):
        """
        Delete by id
        :param generic_type:
        :param uuid:
        :return:
        """
        GEN.delete(generic_type, uuid)
        return "", 204
