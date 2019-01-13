from flask import Blueprint
from flask_restplus import Api
from .api_generic import api as generic_api
from .api_user import api as user_api
from .api_admin import api as admin_api
from .api_symptoms import api as aggregates_api
from .api_doctors import api as doctor_api

blueprint = Blueprint('api', __name__, url_prefix='/api/1')

api = Api(blueprint,
          title='Prostate Backend API',
          version='1.0',
          description='This is the documentation of the prostate backend',
          # All API metadata
          )

api.add_namespace(generic_api, path='/generic')
api.add_namespace(user_api, path='/users')
api.add_namespace(admin_api, path='/admins')
api.add_namespace(aggregates_api, path="/aggregates")
api.add_namespace(doctor_api, path="/doctors")
