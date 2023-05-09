from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, unique=True, index=True, primary_key=True)
    uid = db.Column(db.String(128), nullable=False, unique=True, index=True)
    name = db.Column(db.String(128), nullable=False)
    img = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    city = db.relationship('City',lazy=True)
    trips = db.relationship('City',
                            backref='trips',
                            lazy='dynamic',
                            cascade= 'all')


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
    city = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

    def __init__(self, city, user_id):
        self.city= city
        self.user_id = user_id

    def saveTrip(self):
        db.session.add(self)
        db.session.commit()
        return self

    #User.id = relationship between user and saved trips
# See pokemon(saved teams )
#We should be able to add to our list from Search results page
    # def addTrips(self, city):
    #     self.trips.append(city)
    #     db.session.commit()
#We should be able to delete from our list(see ecomm project)
    def deleteTrips(self):
        self.trips.delete(self)
        db.session.commit()
        return self
#We should be able to clear our entire list (see ecomm project)
    # def clearTrips(self):
    #     self.trips=[]
    #     db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'city': self.city,
            'created_at': self.created_at,
            'user': self.user.to_dict(),
        }