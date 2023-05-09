from flask import Blueprint, request
from ..models import db, User, City



api = Blueprint('api', __name__, url_prefix='/api')


@api.get('/Cities')
def get_cities():
    cities = City.query.order_by(City.created_at.desc()).all()
    if not cities:
        return {'status': 'not ok', 'message': 'Unable to get cities'}
    return {'status': 'ok', 'cities': [city.to_dict() for city in cities]}

@api.get('/cities/<uid>')
def get_user_cities(uid):
    cities = City.query.filter_by(user_uid=uid).order_by(City.created_at.desc()).all()
    if not cities:
        return {'status': 'not ok', 'message': 'Unable to get cities'}
    cities = [city.to_dict() for city in cities]
    return {'status': 'ok', 'cities': cities}

@api.get('/cities/<int:id>')
def get_city(id):
    city = City.query.get(id)
    if not city:
        return {'status': 'not ok', 'message': 'Unable to get city'}
    return {'status': 'ok', 'city': city.to_dict()}

@api.post('/cities')
def create_city():
    user_uid = request.json.get('user_uid')
    body = request.json.get('body')
    user = User.query.filter_by(uid=user_uid).first()
    if not body or not user_uid or not user:
        return {'status': 'not ok', 'message': 'Unable to create city'}
    city = City(user_uid=user_uid, body=body).create()
    return {'status': 'ok', 'city': city.to_dict()}

@api.delete('/cities/<int:id>')
def delete_city(id):
    city = City.query.get(id)
    if not city:
        return {'status': 'not ok', 'message': 'Unable to delete city'}
    city.delete()
    return {'status': 'ok', 'city': city.to_dict()}


# USERS Models 

@api.get('/users')
def get_users():
    users = User.query.all()
    if not users:
        return {'status': 'not ok', 'message': 'Unable to get users'}
    return {'status': 'ok', 'users': [user.to_dict() for user in users]}

@api.get('/users/<uid>')
def get_user(uid):
    user = User.query.filter_by(uid=uid).first()
    if not user:
        return {'status': 'not ok', 'message': 'Unable to get user'}
    return {'status': 'ok', 'user': user.to_dict()}

@api.post('/users')
def create_user():
    uid = request.json.get('uid')
    name = request.json.get('displayName')
    img = request.json.get('photoURL')
    print(img)
    user = User.query.filter_by(uid=uid).first()
    
    if user:
        return {'status': 'ok', 'message': 'Unable to create user. User already exists', 'user': user.to_dict()}
    user = User(uid=uid, name=name, img=img)
    user.create()
    return {'status': 'ok', 'user': user.to_dict()}
