from flask import Blueprint, request
from ..models import db, User, City, Trip


api = Blueprint('api', __name__, url_prefix='/api')

# Get the city 

@api.get('/city')
def get_cities():
    city = City.query.order_by(City.created_at.desc()).all()
    if not city:
        return {'status': 'not ok', 'message': 'Unable to get city'}
    return {'status': 'ok', 'city': [city.to_dict() for city in city]}

# Get the city searched for by user? 

@api.get('/city/<int:id>')
def get_city(id):
    city = City.query.get(id)
    if not city:
        return {'status': 'not ok', 'message': 'Unable to get city'}
    return {'status': 'ok', 'city': city.to_dict()}

# Save city 

@api.post('/city')
def save_city():
    user_uid = request.json.get('user_uid')
    name = request.json.get('name')
    user = User.query.filter_by(uid=user_uid).first()
    if not name or not user_uid or not user:
        return {'status': 'not ok', 'message': 'Unable to create city'}
    city = City(user_uid=user_uid, name=name).create()
    return {'status': 'ok', 'city': city.to_dict()}

# get the trips from the user specifically - will use these to create the list of "my trips"

@api.get('/trip/<uid>')
def get_user_trips(uid):
    trip = Trip.query.filter_by(user_uid=uid).order_by(Trip.created_at.desc()).all()
    if not trip:
        return {'status': 'not ok', 'message': 'Unable to get trip'}
    trip = [trip.to_dict() for trip in trip]
    return {'status': 'ok', 'trip': trip}

# Save the trip- will use to save to "my trips"? 

@api.post('/trip')
def save_trip():
    user_uid = request.json.get('user_uid')
    name = request.json.get('name')
    user = User.query.filter_by(uid=user_uid).first()
    if not name or not user_uid or not user:
        return {'status': 'not ok', 'message': 'Unable to create city'}
    trip = Trip(user_uid=user_uid, name=name).create()
    return {'status': 'ok', 'trip': trip.to_dict()}

# delete city from list of my trips - not sure if I need this 

@api.delete('/city/<int:id>')
def delete_city(id):
    city = City.query.get(id)
    if not city:
        return {'status': 'not ok', 'message': 'Unable to delete city'}
    city.delete()
    return {'status': 'ok', 'city': city.to_dict()}

# Gets users - all

@api.get('/users')
def get_users():
    users = User.query.all()
    if not users:
        return {'status': 'not ok', 'message': 'Unable to get users'}
    return {'status': 'ok', 'users': [user.to_dict() for user in users]}

# Gets user with UID

@api.get('/users/<uid>')
def get_user(uid):
    user = User.query.filter_by(uid=uid).first()
    if not user:
        return {'status': 'not ok', 'message': 'Unable to get user'}
    return {'status': 'ok', 'user': user.to_dict()}

# API Post all users  

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