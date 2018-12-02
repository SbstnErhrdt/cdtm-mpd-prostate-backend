from flask import Flask, request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse
from elasticsearch import Elasticsearch

es = Elasticsearch()

api = Namespace('medication_api', description='track medications')

medication = api.model('Medication', {
    'id': fields.Integer(readOnly=True, description='The medication unique identifier'),
    'medication': fields.String(required=True, description='The medication details')
})


class MedicationDAO(object):
    def __init__(self):
        self.counter = 0
        self.medications = []

    def get(self, id):
        for medication in self.medications:
            if medication['id'] == id:
                return medication
        api.abort(404, "Medication {} doesn't exist".format(id))

    def create(self, data):
        medication = data
        medication['id'] = self.counter = self.counter + 1
        self.medications.append(medication)
        return medication

    def update(self, id, data):
        medication = self.get(id)
        medication.update(data)
        return medication

    def delete(self, id):
        medication = self.get(id)
        self.medications.remove(medication)


DAO = MedicationDAO()
DAO.create({'medication': 'Build an API'})
DAO.create({'medication': '?????'})
DAO.create({'medication': 'profit!'})


@api.route('/')
class MedicationList(Resource):
    '''Shows a list of all medications, and lets you POST to add new medications'''
    @api.doc('list_medications')
    @api.marshal_list_with(medication)
    def get(self):
        '''List all medications'''
        return DAO.medications

    @api.doc('create_medication')
    @api.expect(medication)
    @api.marshal_with(medication, code=201)
    def post(self):
        '''Create a new medication'''
        return DAO.create(api.payload), 201


@api.route('/<int:id>')
@api.response(404, 'Medication not found')
@api.param('id', 'The medication identifier')
class Medication(Resource):
    '''Show a single medication item and lets you delete them'''
    @api.doc('get_medication')
    @api.marshal_with(medication)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @api.doc('delete_medication')
    @api.response(204, 'Medication deleted')
    def delete(self, id):
        '''Delete a medication given its identifier'''
        DAO.delete(id)
        return '', 204

    @api.expect(medication)
    @api.marshal_with(medication)
    def put(self, id):
        '''Update a medication given its identifier'''
        return DAO.update(id, api.payload)