from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, unique=True, index=True, primary_key=True)
    uid = db.Column(db.String(128), nullable=False, unique=True, index=True)
    name = db.Column(db.String(128), nullable=False)
    img = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, uid, name, img):
        self.uid = uid
        self.name = name
        self.img = img

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'uid': self.uid,
            'name': self.name,
            'img': self.img,
        }


#For this purpose, do we need to create a user_id relationship with the city?

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(280), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_uid = db.Column(db.String, db.ForeignKey('user.uid'), nullable=False)
    user = db.relationship('User', backref=db.backref('user', lazy=True))

    def __init__(self, name, user_uid):
        self.name = name
        self.user_uid = user_uid

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'user': self.user.to_dict(),
        }
    
class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(280), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_uid = db.Column(db.String, db.ForeignKey('user.uid'), nullable=False)
    user = db.relationship('User', backref=db.backref('trip_user', lazy=True))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    def __init__(self, name, user_uid, city_id):
        self.name = name
        self.user_uid = user_uid
        self.city_id = city_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'user': self.user.to_dict(),
            'city_id': self.city_id
        }