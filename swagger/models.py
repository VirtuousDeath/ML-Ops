from marshmallow import Schema, fields

class FilterPayloadSchema(Schema):
    filter = fields.String(required=False)
    page = fields.Integer()
    limit = fields.Integer()

class LoginPayloadSchema(Schema):
    name = fields.String()
    password = fields.String()

class UserNamePayloadSchema(Schema):
    name = fields.String()
    document = fields.String()
    password = fields.String()

class UserPayloadSchema(Schema):
    user =  fields.Nested(UserNamePayloadSchema())

class UsersResponseSchema(Schema):
    name = fields.String()
    document = fields.String()

class PredictElementSchema(Schema):
    renda = fields.Float()
    idade = fields.Integer()
    etnia = fields.Integer()
    sexo = fields.Integer()
    casapropria = fields.Integer()
    outrasrendas = fields.Float()
    estadocivil = fields.Integer()
    escolaridade = fields.Integer()

class PredictResponseSchema(Schema):
    prediction = fields.List(fields.Float())
    proba = fields.List(fields.Float())

class PredictPayloadSchema(Schema):
    value = fields.List(fields.Nested(PredictElementSchema))
    