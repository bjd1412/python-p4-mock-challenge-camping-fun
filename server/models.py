from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'
    serialize_rules = ("-signups.activity",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    signups = db.relationship("Signup", back_populates='activity', cascade="all, delete")

    # Add relationship
    
    # Add serialization rules
    
    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'
    serialize_rules = ("-signups.camper",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    signups = db.relationship("Signup", back_populates='camper', cascade="all, delete")

    activities = association_proxy("signups", "activity", creator=lambda activity_obj: Signup(activity=activity_obj))

    @validates("name")
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Must have name.")
        else:
            return name

    @validates("age")
    def validate_age(self, key, age):
        if age < 8 or age > 18:
            raise ValueError("Age must be between 8 and 18.")
        else:
            return age



    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'
    serialize_rules = ("-camper.signups", "-activity.signups",)

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    camper_id = db.Column(db.Integer, db.ForeignKey("campers.id", ondelete="CASCADE"))
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id", ondelete="CASCADE"))


    camper = db.relationship("Camper", back_populates='signups', cascade="all")
    activity = db.relationship("Activity", back_populates='signups')
    
    @validates("time")
    def validate_time(self, key, time):
        if time < 0 or time > 23:
            raise ValueError("Time must be in a 24 hour period.")
        else:
            return time
    
    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.
