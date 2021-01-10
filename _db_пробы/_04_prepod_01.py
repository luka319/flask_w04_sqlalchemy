from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_04.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#    email = db.Column(db.String(255), unique=True, nullable=False)

association_table = db.Table('association',
    db.Column('teachers_id', db.Integer, db.ForeignKey('teachers.id')),
    db.Column('goals_id', db.Integer, db.ForeignKey('goals.id'))
)


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    #about = db.Column(db.String, nullable=False) #text
    about = db.Column(db.Text) #text
    rating = db.Column(db.Float)
    picture = db.Column(db.String) #
    price = db.Column(db.Integer)
    free = db.Column(db.String) # JSON

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


db.create_all()

# ========================================================
