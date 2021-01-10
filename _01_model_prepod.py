
class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    #about = db.Column(db.String, nullable=False) #text
    about = db.Column(db.Text, nullable=False) #text
    rating = db.Column(db.Float, nullable=False)
    picture = db.Column(db.String, nullable=False) #
    price = db.Column(db.Integer, nullable=False)
    goals_id = db.Column(db.Integer, nullable=False) # таблица goals

    free = db.Column(db.String, nullable=False) # JSON
    goal_lnk = db.relationship("Goal")

class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String, nullable=False)
    #about = db.Column(db.String, nullable=False) #text

    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    teacher_lnk = db.relationship("Teacher")

#user = User(name=input(), email=input(), password=input())
te01 = Teacher(name=input(), email=input(), password=input())
db.session.add(te01)
db.session.commit()
print(f"{te01.id}")


        "id": 0,
        "name": "Morris Simmmons",
        "about": "Репетитор американского английского языка. Структурированная система обучения. Всем привет! Я предпочитаю называть себя «тренером» английского языка. Мои занятия похожи на тренировки",
        "rating": 4.2,

        "picture": "https://i.pravatar.cc/300?img=20",
        "price": 900,
        "goals": ["travel", "relocate", "study"],
        "free": {

            "mon": {"8:00": False, "10:00": True, "12:00": True, "14:00": False, "16:00": False, "18:00": False,
                    "20:00": False, "22:00": False},
            "tue": {"8:00": True, "10:00": True, "12:00": False, "14:00": False, "16:00": False, "18:00": False,
