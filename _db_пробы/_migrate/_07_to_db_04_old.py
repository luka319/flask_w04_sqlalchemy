from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_07.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from time import sleep

with open("teachers.json", "r", encoding="utf-8") as f:
    te = json.load(f)  #

# ==========================================
association_table = db.Table('association',
    db.Column('teachers_id', db.Integer, db.ForeignKey('teachers.id')),
    db.Column('goals_id', db.Integer, db.ForeignKey('goals.id'))
)


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    id_teacher = db.Column(db.String, nullable=False) # id тичера в teachers.json
    name = db.Column(db.String, nullable=False)
    #about = db.Column(db.String, nullable=False) #text
    about = db.Column(db.Text) #text
    rating = db.Column(db.Float)
    picture = db.Column(db.String) #
    price = db.Column(db.Integer)
    free = db.Column(db.String) # JSON

    booking_lnk = db.relationship("Booking", back_populates="teachers_lnk")

    goals = db.relationship(
        "Goal", secondary=association_table, back_populates="teachers"
    )

class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String, nullable=False)
    #about = db.Column(db.String, nullable=False) #text

    teachers = db.relationship(
        "Teacher", secondary=association_table, back_populates="goals"
    )

#======================================================================
"""
2. Создайте модель "Бронирование"

– Опишите модель Бронирование.
– Свяжите модель отношениями с Преподавателем (one to many).
– Проверьте, что первичный ключ, типы и констрейнты в порядке.
"""

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    #about = db.Column(db.String, nullable=False) #text
    clientWeekday = db.Column(db.String) 
    clientTime = db.Column(db.Time) 

    #db.Column('clientTeacher', db.Integer, db.ForeignKey('teachers.id'))
    #clientTeacher = db.Column('teachers_id', db.Integer, db.ForeignKey('teachers.id'))
    teachers_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    teachers_lnk = db.relationship("Teacher", back_populates="booking_lnk")
    
    clientName = db.Column(db.String) #
    clientPhone = db.Column(db.String)

#======================================================================

"""
3. Создайте модель "Заявка на подбор"

– Опишите модель.
– Проверьте, что первичный ключ, типы и констрейнты в порядке.

data = {count + 1: [goal, time_,
                            name_,
                            phone]

"""
class Request(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    #about = db.Column(db.String, nullable=False) #text
    goal = db.Column(db.String) 
    time = db.Column(db.Time) 
    name = db.Column(db.String) #
    phone = db.Column(db.String)


# ==========================================

"""
goals_list = []
name_list = []
picture_list = []
about_list = []
rating_list = []
price_list = []
free_list = []
"""

for z in te:
         #if z["id"] == id_teacher:
            # z = id_teacher
            # print(f'{z["name"] =}')
            id_teacher_db = z["id"]
            goals_tut = z["goals"]  # откуда брать ????
            # print(f'{goals_tut =}')
            name = z["name"]
            picture = z["picture"]
            about = z["about"]
            rating = z["rating"]
            price = z["price"]
            free = z["free"]

            db.session.add_all([
                      Teacher(id_teacher = id_teacher_db), 
                      Teacher(name = name),  
                      Teacher(about = about), 
                      Teacher(rating = rating),
                      Teacher(picture = picture),
                      Teacher(price = price),
                      Teacher(free = free),
            ])
            db.session.commit()
            sleep(0.5) # а надо ли? сколько времени идет коммит???



"""
db.session.add_all([User(name='Vlad'), User(name='Игорь'), User(name='Слава')])

user = Teacher(name='Василий')
db.session.add(user)
print(f"ID is {user.id}")
db.session.commit()
print(f"ID is {user.id}")
"""

"""
class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    id_teacher = db.Column(db.String, nullable=False) # id тичера в teachers.json
    name = db.Column(db.String, nullable=False)
    #about = db.Column(db.String, nullable=False) #text
    about = db.Column(db.Text) #text
    rating = db.Column(db.Float)
    picture = db.Column(db.String) #
    price = db.Column(db.Integer)
    free = db.Column(db.String) # JSON

    booking_lnk = db.relationship("Booking", back_populates="teachers_lnk")

    goals = db.relationship(
        "Goal", secondary=association_table, back_populates="teachers"
    )
"""



