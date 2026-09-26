import sqlite3
import datetime
from helpers import token_required
from urllib.parse import unquote
from argon2 import PasswordHasher
import jwt
from flask import request, jsonify, make_response
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor as rfr
from helpers import Single, NpEncoder
import json 
from config import config

def initialize():
    # 1. Connect to a database (or create it)
    connection = sqlite3.connect('mlops.db')

    # 2. Create a cursor object
    cursor = connection.cursor()
    
    cursor.execute('''DROP TABLE IF EXISTS [tbUser]''')
    cursor.execute('''DROP TABLE IF EXISTS [tbSession]''')
    # 3. Create a table
    cursor.execute('''CREATE TABLE [tbUser](
    [name] [varchar](50) NOT NULL,
    [document] [varchar](20) NOT NULL,
    [password] [varchar](50) NOT NULL,
    CONSTRAINT [PK_tbUser] PRIMARY KEY([document] ASC))''')
    cursor.execute('''CREATE TABLE [tbSession](
    [name] [varchar](50) NOT NULL,
    [token] [varchar](100) NOT NULL,
    CONSTRAINT [tbSession] PRIMARY KEY([name] ASC))''')
   
    connection.commit()
    # 7. Close the connection
    connection.close()

    return 'True'

def get_users_data(data): 
    connection = sqlite3.connect('mlops.db')

    # 2. Create a cursor object
    cursor = connection.cursor()

    # 6. Query and fetch data
    cursor.execute(f'''SELECT name, document FROM tbUser limit {data['limit']} offset {int(data['limit'])*(int(data['page']) - 1)}''')
    result = cursor.fetchall()

    connection.close()

    return [ {"name": res[0], "document": res[1] } for res in result]

def create_user_data(data):
    ph = PasswordHasher()
    # 1. Connect to a database (or create it)
    connection = sqlite3.connect('mlops.db')
    # 2. Create a cursor object
    cursor = connection.cursor()
    # 4. Insert data
    cursor.execute(f"INSERT INTO tbUser (name, document, password) VALUES ('{data['user']['name']}', '{data['user']['document']}', '{ph.hash(data['user']['password'])}') ON CONFLICT (document) DO NOTHING")
    
    connection.commit()
    # 7. Close the connection
    connection.close()

    return 'True'

def login_user(data):
    ph = PasswordHasher()
    connection = sqlite3.connect('mlops.db')

    # 2. Create a cursor object
    cursor = connection.cursor()
    # 6. Query and fetch data
    cursor.execute(f'''SELECT * FROM tbUser where name = "{data['name']}"''')
    result = cursor.fetchone()

    if data and ph.verify(result[2], data['password']):
        token = jwt.encode({'user': data['name'], 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(seconds=3600)}, config['secret_key'], 'HS256')
        cursor.execute(f"INSERT INTO tbSession (name, token) VALUES ('{data['name']}', '{token}') ON CONFLICT (name) DO UPDATE SET token='{token}'")

        connection.commit()
        # 7. Close the connection
        connection.close()
        return { 'token': token }
    # 7. Close the connection
    connection.close()

    return make_response('Could not Verify', 401, {'WWW-Authenticate': 'Basic realm ="Login Required"'})

def predict_data(data): 
    print(data)

    try:
        json_ = data['value']
        print(f"received data {json_}")

        fields = pd.DataFrame(json_)
        model = Single().get_instance().model
        if fields.shape[0] == 0:
            return "Dados de chamada da API estão incorretos.", 400

        print(model.feature_names_in_)
        for col in model.feature_names_in_:
            if col not in fields.columns:
                fields[col] = 0
        x = fields[model.feature_names_in_]
        
        prediction = model.predict(x)
        print(prediction)
        try:
            predict_proba = model.predict_proba(x)
        except Exception as ex:
            predict_proba = []
        ret = {'prediction': list(prediction), 'proba': list(predict_proba)}
        print(ret)

        return ret
    except Exception as err:
        print(f"Exception: \n{err}")
        return f"Error processing input data: {json_}"
