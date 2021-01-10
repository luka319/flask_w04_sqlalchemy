from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_07.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    id_teacher = db.Column(db.Integer) # id тичера в teachers.json
    name = db.Column(db.String)
    #about = db.Column(db.String, nullable=False) #text
    about = db.Column(db.Text) #text
    rating = db.Column(db.Float)
    picture = db.Column(db.String) #
    price = db.Column(db.Integer)
    free = db.Column(db.Text) # JSON
    """
    booking_lnk = db.relationship("Booking", back_populates="teachers_lnk")

    goals = db.relationship(
        "Goal", secondary=association_table, back_populates="teachers"
    )
    """


"""
@app.route('/profiles/<int:id_teacher>/') # 4. Выведите страницу преподавателя
def main_profiles(id_teacher):
"""
te_ = db.session.query(Teacher).all()
#te_ = db.session.query(teachers).all() # так не работает
print(f"{te_ =}")

teachers_query = db.session.query(Teacher).order_by(Teacher.id_teacher)
teachers = teachers_query.all()
print("Получили", len(teachers), "преподавателей")
for teacher in teachers:
    print(f"{teacher.id_teacher=}",
          f"{teacher.name=}",
          f"{teacher.rating=}",
          f"{teacher.picture=}",
          f"{teacher.price=}")


last_free = teacher.free
print(f"{last_free =}")
#last_dict = dict(last_free)
#print(f"{last_dict =}")
#a = a.replace('"Станкин"', r'\"Станкин\"')

last_fr = json.loads(last_free)
print(f"{last_fr =}")
print(f"{type(last_fr) =}")

# print(f"{}") # SyntaxError: f-string: empty expression not allowed


"""
for z in te:
         if z["id"] == id_teacher:
            # z = id_teacher
            # print(f'{z["name"] =}')
            goals_tut = z["goals"]
            # print(f'{goals_tut =}')
            name = z["name"]
            picture = z["picture"]
            about = z["about"]
            rating = z["rating"]
            price = z["price"]
            free = z["free"]

"""
