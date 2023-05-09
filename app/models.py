from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    img = db.Column(db.String(500), nullable=True)
    city = db.relationship('City', lazy=True)
    trips = db.relationship('City',lazy=True)



    def __init__(self, username, email, password, img):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.img = img
        #self.password = password   ---OLD  not hashed

    def saveUser(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self
    
    def unTrip(self, city):
        self.trips.remove(city)
        db.session.commit()

    def cleartrips(self):
        self.trips=[]
        db.session.commit()
    
    def addTrips(self, product):
        self.trips.append(product)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'username' : self.username,
            'img': self.img,
        }

trips = db.Table(
    'savedTrips',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.Column('city_id', db.Integer, db.ForeignKey('city.id'), nullable=False)
)

#For this purpose, do we need to create a user_id relationship with the city?

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, city, user_id):
        self.city= city()
        self.user_id = user_id()
        return self

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