from flask import Blueprint
from flask_restplus import Api
from .api_users import api as users_api
from .api_symptoms import api as symptoms_api

blueprint = Blueprint('api', __name__, url_prefix='/api/1')

api = Api(blueprint,
          title='USER Backend API',
          version='1.0',
          description='This is the documentation of the NLP Backend',
          # All API metadatas
          )

api.add_namespace(users_api, path='/users')
api.add_namespace(symptoms_api, path='/symptoms')
