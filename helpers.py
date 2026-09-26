import jwt
from flask import request, jsonify
import joblib
import json
import sqlite3
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from config import config
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        connection = sqlite3.connect('mlops.db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM tbSession where token = '{request.headers.get('Authorization').split(' ')[::-1][0]}'")
        token = cursor.fetchone()

        if not token:
            return jsonify({'error': 'token is missing'}), 403
        try:
            jwt.decode(token[1], config['secret_key'], algorithms="HS256")
        except Exception as error:
            return jsonify({'error': 'token is invalid/expired'})
        return f(*args, **kwargs)
    return decorated

class Single:
    _instance = None
    model: RandomForestRegressor = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls.model = joblib.load('./model/modelo_bin.pkl')
        return cls._instance

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)
