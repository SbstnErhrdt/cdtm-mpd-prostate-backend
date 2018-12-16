from flask import Blueprint
from flask_restplus import Api
from .api_generic import api as generic_api

blueprint = Blueprint('api', __name__, url_prefix='/api/1')

api = Api(blueprint,
          title='Prostate Backend API',
          version='1.0',
          description='This is the documentation of the prostate backend',
          # All API metadata
          )

api.add_namespace(generic_api, path='/generic')
