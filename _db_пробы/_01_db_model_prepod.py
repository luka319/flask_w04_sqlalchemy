from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_01.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#    email = db.Column(db.String(255), unique=True, nullable=False)

class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    #about = db.Column(db.String, nullable=False) #text
    """
    about = db.Column(db.Text, nullable=False) #text
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False) #
    price = db.Column(db.Integer, nullable=False)
    #goals_id = db.Column(db.Integer, nullable=False) # таблица goals
    """
    free = db.Column(db.String, nullable=False) # JSON
    #goal_lnk = db.relationship("Goal")

    goal_lnk = db.relationship("Goal", back_populates="teachers_lnk")

class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String, nullable=False)
    #about = db.Column(db.String, nullable=False) #text

    teachers_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    teachers_lnk = db.relationship("Teacher", back_populates="goal_lnk")


db.create_all()

#db.session.commit()

#user = User(name=input(), email=input(), password=input())

go01 = Goal( goal=input("goal ? ="))
db.session.add(go01)

te01 = Teacher( name=input("name ? ="), free=input("free ? =") )
db.session.add(te01)

db.session.commit()

"""
user = User(name='Gleb')
db.session.add(user)
pet = Pet(name='Рыжик', owner=user)
db.session.add(pet)
db.session.commit()
"""



#print(f"{te01.id}")

