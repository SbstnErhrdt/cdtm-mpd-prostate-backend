from flask import Flask, request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse
from elasticsearch import Elasticsearch

es = Elasticsearch()

api = Namespace('symptom_api', description='track symptoms')

symptom = api.model('Symptom', {
    'id': fields.Integer(readOnly=True, description='The symptom unique identifier'),
    'symptom': fields.String(required=True, description='The symptom details')
})


class SymptomDAO(object):
    def __init__(self):
        self.counter = 0
        self.symptoms = []

    def get(self, id):
        for symptom in self.symptoms:
            if symptom['id'] == id:
                return symptom
        api.abort(404, "Symptom {} doesn't exist".format(id))

    def create(self, data):
        symptom = data
        symptom['id'] = self.counter = self.counter + 1
        self.symptoms.append(symptom)
        return symptom

    def update(self, id, data):
        symptom = self.get(id)
        symptom.update(data)
        return symptom

    def delete(self, id):
        symptom = self.get(id)
        self.symptoms.remove(symptom)


DAO = SymptomDAO()
DAO.create({'symptom': 'Blood in urin'})
DAO.create({'symptom': '?????'})
DAO.create({'symptom': 'profit!'})


@api.route('/')
class SymptomList(Resource):
    '''Shows a list of all symptoms, and lets you POST to add new symptoms'''
    @api.doc('list_symptoms')
    @api.marshal_list_with(symptom)
    def get(self):
        '''List all symptoms'''
        return DAO.symptoms

    @api.doc('create_symptom')
    @api.expect(symptom)
    @api.marshal_with(symptom, code=201)
    def post(self):
        '''Create a new symptom'''
        return DAO.create(api.payload), 201


@api.route('/<int:id>')
@api.response(404, 'Symptom not found')
@api.param('id', 'The symptom identifier')
class Symptom(Resource):
    '''Show a single symptom item and lets you delete them'''
    @api.doc('get_symptom')
    @api.marshal_with(symptom)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @api.doc('delete_symptom')
    @api.response(204, 'Symptom deleted')
    def delete(self, id):
        '''Delete a symptom given its identifier'''
        DAO.delete(id)
        return '', 204

    @api.expect(symptom)
    @api.marshal_with(symptom)
    def put(self, id):
        '''Update a symptom given its identifier'''
        return DAO.update(id, api.payload)