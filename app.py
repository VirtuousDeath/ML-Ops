from flask import Flask, request
from service import initialize, create_user_data, get_users_data, login_user, predict_data
from flask_cors import CORS
from flask import Flask
from swagger.models import FilterPayloadSchema, UserPayloadSchema, UsersResponseSchema, LoginPayloadSchema, PredictPayloadSchema, PredictResponseSchema
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec import FlaskApiSpec, use_kwargs, marshal_with
from helpers import token_required
from flask_limiter import Limiter                    
from marshmallow import fields
from flask_limiter.util import get_remote_address
app = Flask(__name__)
CORS(app)
limiter = Limiter(get_remote_address, app=app)
# 1. Configurar o gerador apispec
app.config.update({
    'secret_key': '',
    'APISPEC_SPEC': APISpec(
        title='API ML-OPs',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_URL': '/swagger/' # Endpoint da documentação
})

docs = FlaskApiSpec(app)

@app.route("/",methods=['GET'])
@limiter.limit("1 per 1 second")
def health(**kwargs):
    try: 
        return 'True'
    except Exception as e:
        print(e)
        return e
    
@app.route("/init",methods=['POST'])
@limiter.limit("1 per 1 second")
def init(**kwargs):
    try: 
        initialize()
        return 'True'
    except Exception as e:
        print(e)
        return e

@app.route('/user', methods=['POST'])
@use_kwargs(UserPayloadSchema(), location='json') # Valida payload recebido
@limiter.limit("1 per 1 second")
def create_user(**kwargs):
    try: 
        return create_user_data(request.json)
    except Exception as e:
        print(e)
        return e

@app.route('/users', methods=['GET'])
@use_kwargs(FilterPayloadSchema(), location='query')  # Defines **kwargsquery string params
@marshal_with(UsersResponseSchema(many=True))               # Formata JSON retornado
@token_required
@use_kwargs(
    {
        'Authorization':
        fields.Str(
            required=True,
            description=
            'Authorization HTTP header with JWT refresh token, like: Authorization: Bearer asdf.qwer.zxcv'
        )
    },
    location='headers')
@limiter.limit("1 per 1 second")
def get_users(**kwargs):
    try: 
        return get_users_data(request.args)
    except Exception as e:
        print(e)
        return e

@app.route("/login", methods=['POST'])
@use_kwargs(LoginPayloadSchema(), location='json')  # Defines **kwargsquery string params
@limiter.limit("1 per 1 second")
def login(**kwargs):
    try:
        return login_user(request.json)
    except Exception as e:
        print(e)
        return e

@app.route("/predict", methods=['POST'])
@use_kwargs(PredictPayloadSchema(), location='json')  # Defines **kwargsquery string params
@marshal_with(PredictResponseSchema())               # Formata JSON retornado
@use_kwargs(
    {
        'Authorization':
        fields.Str(
            required=True,
            description=
            'Authorization HTTP header with JWT refresh token, like: Authorization: Bearer asdf.qwer.zxcv'
        )
    },
    location='headers')
@token_required
@limiter.limit("1 per 1 second")
def predict(**kwargs):
    try: 
        return predict_data(request.json)
    except Exception as e:
        print(e)
        return e
    
docs.register(health)
docs.register(init)
docs.register(create_user)
docs.register(get_users)
docs.register(login)
docs.register(predict)