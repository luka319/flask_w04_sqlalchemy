from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import sys
id_teacher = int(sys.argv[1])

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

teachers_query = db.session.query(Teacher).order_by(Teacher.id_teacher)
#teachers = teachers_query.all()
#          user = User.query.get_or_404(id)
teacher = teachers_query.get_or_404(id_teacher) # это id базы, они не
# совпадают с id_teacher

if teacher.id_teacher == id_teacher:

            name = teacher.name
            #goals_tut = teacher.goals # ??? !!!
            # print(f'{goals_tut =}')
            picture = teacher.picture
            about = teacher.about
            rating = teacher.rating
            price = teacher.price
            free = json.loads(teacher.free)

print(f"{teacher.name = }")
print(f"{teacher.id_teacher = }")

# if name: print(f"{name = }")
print(f"{id_teacher = }")
