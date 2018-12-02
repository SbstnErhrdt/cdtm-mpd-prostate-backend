from flask import Flask, request, jsonify
from flask_restplus import Namespace, Resource, fields, reqparse
from elasticsearch import Elasticsearch

es = Elasticsearch()

api = Namespace('users_api', description='use all functionality of spacy')

todo = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})


class UserDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "User {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)


DAO = UserDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})


@api.route('/')
class UserList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @api.doc('list_todos')
    @api.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @api.doc('create_todo')
    @api.expect(todo)
    @api.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@api.route('/<int:id>')
@api.response(404, 'User not found')
@api.param('id', 'The task identifier')
class User(Resource):
    '''Show a single todo item and lets you delete them'''
    @api.doc('get_todo')
    @api.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @api.doc('delete_todo')
    @api.response(204, 'User deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @api.expect(todo)
    @api.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)