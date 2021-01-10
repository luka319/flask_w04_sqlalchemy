
import babel
import calendar
import json
import locale
import os
import pathlib
import random

from flask import Flask, render_template, request
from time import sleep
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_07.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

with open("teachers.json", "r", encoding="utf-8") as f:
    te = json.load(f)  #

with open("goals.json", "r", encoding="utf-8") as f:
        goals = json.load(f)  #
# p 10. Добавьте еще одну цель
# – добавьте новую цель "для программирования" преподавателям   8,9,10,11
# сохраняю в teachers.json
for qa in [8,9,10,11]:
    if not "programming" in te[qa]["goals"]:
        te[qa]["goals"].append("programming")
        with open('teachers.json', 'w', encoding='utf-8') as f:
             json.dump(te, f, ensure_ascii=False)

# сохраняю в goals.json
goa = {"programming": "Для программирования"}
if not "programming" in goals.keys():
      goals.update(goa)
      with open('goals.json', 'w', encoding='utf-8') as f:
             json.dump(goals, f, ensure_ascii=False)

# ========================== SQLAlchemy ==============================
# from flask import Flask
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
#
# import json

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_07.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

#    email = db.Column(db.String(255), unique=True, nullable=False)

association_table = db.Table('association',
                             db.Column('teachers_id', db.Integer, db.ForeignKey('teachers.id')),
                             db.Column('goals_id', db.Integer, db.ForeignKey('goals.id'))
                             )


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    id_teacher = db.Column(db.Integer)  # id тичера в teachers.json
    name = db.Column(db.String)
    # about = db.Column(db.String, nullable=False) #text
    about = db.Column(db.Text)  # text
    rating = db.Column(db.Float)
    picture = db.Column(db.String)  #
    price = db.Column(db.Integer)
    free = db.Column(db.Text)  # JSON

    booking_lnk = db.relationship("Booking", back_populates="teachers_lnk")

    goals = db.relationship(
        "Goal", secondary=association_table, back_populates="teachers"
    )


class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String, nullable=False)
    # about = db.Column(db.String, nullable=False) #text

    teachers = db.relationship(
        "Teacher", secondary=association_table, back_populates="goals"
    )


# ======================================================================
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
    # about = db.Column(db.String, nullable=False) #text
    clientWeekday = db.Column(db.String)
    clientTime = db.Column(db.Time)

    # db.Column('clientTeacher', db.Integer, db.ForeignKey('teachers.id'))
    # clientTeacher = db.Column('teachers_id', db.Integer, db.ForeignKey('teachers.id'))
    teachers_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    teachers_lnk = db.relationship("Teacher", back_populates="booking_lnk")

    clientName = db.Column(db.String)  #
    clientPhone = db.Column(db.String)


# ======================================================================

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
    # about = db.Column(db.String, nullable=False) #text
    goal = db.Column(db.String)
    time = db.Column(db.Time)
    name = db.Column(db.String)  #
    phone = db.Column(db.String)


# ========================================================
db.create_all()
# ========================================================
# with open("teachers.json", "r", encoding="utf-8") as f:
#     te = json.load(f)  #

# name = "pass"

for z in te:
    # if z["id"] == id_teacher:
    # z = id_teacher
    print(f'{z["name"] =}')
    print(f'{z["id"] =}')
    print('==========================')
    id_teacher_db = z["id"]
    goals_tut = z["goals"]  # откуда брать ????
    # print(f'{goals_tut =}')
    name_ = z["name"]
    picture_ = z["picture"]
    about_ = z["about"]
    rating_ = z["rating"]
    price_ = z["price"]
    free_ = z["free"]  # надо в строку (json.dumps), а то в бд не прожуёт!!!
    # print(f'{z["free"] =}')
    # print(f'{type(z["free"]) =}') # type(z["free"]) =<class 'dict'>

    # input("========== press key ======")
    # user = User(name='Василий')
    # db.session.add(user)
    db.session.add(
        Teacher(id_teacher=id_teacher_db,
                name=name_,
                about=about_,
                rating=rating_,
                picture=picture_,
                price=price_,
                # free = str(free_),
                # json.dumps(free_, free, ensure_ascii=False),#not work
                free=json.dumps(free_, ensure_ascii=False),
                # откуда - куда
                ))
    db.session.commit()
    sleep(0.5)  # а надо ли? сколько времени идет коммит???

# ========================== SQLAlchemy ==============================
@app.route('/')
def main():
    # print(f"{te=}")
    te_rand = random.sample(list(te), 6)
    # print(f"{te_rand =}")
    return render_template("index.html",te=te_rand)

@app.route('/all/', methods=['POST',"GET"])
def main_all():
    # if request.method == 'GET':
    #     goal = request.form['goal']
    # print(f"{request.args =}")
    # print(f"{request.args.get('n') =}") # '3'
    select_rand=""
    select_best = ""
    select_expensive = ""
    select_cheap = ""
    req_get = request.args.get('n')
    if req_get == "rand":
        select_rand = "selected"
    elif req_get == "best_rating":
        select_best = "selected"
    elif req_get == "expensive_first":
        select_expensive = "selected"
    elif req_get == "cheap_first":
        select_cheap = "selected"

    # В случайном порядке
    # Сначала лучшие по рейтингу
    # Сначала дорогие
    # Сначала недорогие

    te_rand = random.sample(list(te), len(te))
    # print(f"{te_rand =}")

    return render_template("all.html", te=te_rand, select_rand=select_rand,
                           select_best=select_best, select_expensive=select_expensive,
                           select_cheap=select_cheap)

@app.route('/goals/<goal>/')
def main_goals(goal):
    # en_goals = ["travel", "study", "work", "relocate"]
    # ru_goals = ["путешествий", "школы", "работы", "переезда"]
    # goals = dict(zip(en_goals, ru_goals))
    # goal02 = goals[goal]
    # print(f"{goal02 =}")
    # print(f"{goal =}")
    for zz, kk in goals.items():
        # print(f'{zz =}')
        # print(f'{kk =}')
        pass
    # goal02 = goals[goal][3:]

    """
    for z in te:
        if goal in z['goals']:
            # print(f"{z['goals'] =}")
            name = z["name"]
            # print(f"{name =}")
            picture = z["picture"]
            about = z["about"]
            rating = z["rating"]
            price = z["price"]
            id_ = z["id"]
    """

    return render_template("goal.html", goal=goal, te=te, goals=goals)

@app.route('/profiles/<int:id_teacher>/') # 4. Выведите страницу преподавателя
def main_profiles(id_teacher):
    # https: // github.com / luka319 / flask_w03 / blob / main / app.py
    # L103 не обработана ситуация когда прислали id учителя которого нет в БД.

    # из JSON ============================================
    """
    name = "pass"
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
    # из JSON ============================================
    # из БД: (начало)  ==========================================
    teachers_query = db.session.query(Teacher).order_by(Teacher.id_teacher)
    teachers = teachers_query.all()
    # user = User.query.get_or_404(id)
    # print("Получили", len(teachers), "преподавателей")
    for teacher in teachers:
        if teacher.id_teacher == id_teacher:
            name = teacher.name
            # goals_tut = teacher.goals # ??? !!!
            goals_tut = "пока пустышка"
            # print(f'{goals_tut =}')
            picture = teacher.picture
            about = teacher.about
            rating = teacher.rating
            price = teacher.price
            free = json.loads(teacher.free)

    print(f"{name = }")
    print(f"{id_teacher = }")
    # из БД (конец) =============================================

    with open("goals.json", "r", encoding="utf-8") as f:
        goals = json.load(f)  #

    for zz, kk in goals.items():
        # print(f'{zz =}')
        # print(f'{kk =}')
        pass

    # =======================================
    # calendar
    engl_full_day = []
    for day2 in calendar.day_name:
        da2 = day2
        # print(da.title())
        engl_full_day.append(da2)

    if os.name == 'nt':
        locale.setlocale(locale.LC_ALL, "Russian_Russia.1251")
    else:
        locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")

    engl_day = []
    for k in free.keys():
         engl_day.append(k)

    ru_day = []
    for day in calendar.day_name:
        da = day
        # print(da.title())
        ru_day.append(da.title())
        # day_name[da.title()] = engl_day[zz]
    week_ = dict(zip(ru_day, engl_day))

    # print(
    #     list(calendar.day_name))  # ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']

    # free = z["free"] # там выше оно есть, здеесь для напоминания

    day_false = []
    for ke, va in free.items():  # free ={'mon': {'8:00': False, '10:00': False,

        # print(f'{ke =}') # OK!!!
        # print(f'{va =}') # OK!!!
        va2_net = []
        for ke2, va2 in va.items():
            va2_net.append(va2)
        if any(va2_net)==False: # если оно False
                day_false.append(ke)

    # print(f"{day_false =}")
    # print(f"{id_teacher =}")
    id_te = id_teacher

    return render_template("profile.html", name=name, picture=picture, about=about,
                           rating=rating, price=price, goals=goals, free=free,
                           week_=week_,day_false=day_false,
                           id_te=id_te, engl_full_day=engl_full_day,
                           goals_tut=goals_tut)

@app.route('/request/')
def main_request():
    return render_template("request.html",)

@app.route('/request_done/', methods=['POST'])
def main_request_done():
    if request.method == 'POST':
            goal = request.form['goal']
            # print(f"{goal=}")
            time_ = request.form['time']
            # print(f"{time_=}")
            name_ = request.form['name']
            # print(f"{name_ =}")
            phone = request.form['phone']
            # print(f"{phone=}")

            # сохраняю в request.json
            path = pathlib.Path('request.json')
            if path.exists():
                if path.is_file():
                    with open('request.json', 'r', encoding='utf-8') as f:
                        data_in = json.load(f)
                    count = len(data_in)
                else:
                    print("request.json не является файлом")
                    exit()
            else:
                print("== request.json doesn't exists. It will be created! ==")
                # exit()
                count = 0
                data_in = {}

            data = {count + 1: [goal, time_,
                            name_,
                            phone]
                    }
            data_in.update(data)
            data_out = data_in
            with open('request.json', 'w', encoding='utf-8') as f:
                json.dump(data_out, f, ensure_ascii=False)

    en_goals = ["travel","learn","work", "move", "progr"]
    ru_goals = ["Для путешествий", "Для школы", "Для работы", "Для переезда", "Для программирования"]
    goals = dict(zip(en_goals, ru_goals))
    goal02 = goals[goal]
    # print(f"{goal02 =}")

    return render_template("request_done.html", goal=goal02, time_=time_,
                            name_=name_, phone=phone)

@app.route('/booking/<int:id_teacher>/<day_of_week>/<time>/')
def main_booking(id_teacher, day_of_week, time):
    free = {}
    with open("teachers.json", "r", encoding="utf-8") as f:
        te2 = json.load(f)  #
    # print(f"{te2=}")
    for z in te2:
         if z["id"] == id_teacher:
            free = z["free"]
            name = z["name"]
            picture = z["picture"]
            # print(f"{free =}")
    # =======================================
    # calendar


    if os.name == 'nt':
        locale.setlocale(locale.LC_ALL, "Russian_Russia.1251")
    else:
        locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")

    engl_day = []
    for k in free.keys():
        engl_day.append(k)

    ru_day = []
    for day in calendar.day_name:
        da = day
        # print(da.title())
        ru_day.append(da.title())
        # day_name[da.title()] = engl_day[zz]
    week_2 = dict(zip(engl_day, ru_day))
    # print(f"{week_2 =}")
    dweek = week_2[day_of_week]

    return render_template("booking.html", id_teacher=id_teacher,
                           dweek=dweek, time=time, name=name,
                           picture=picture,
                           )

# @app.route('/booking_done/<clientWeekday>/<clientTime>/<clientTeacher>/<clientName>/<clientPhone>/',
#            methods=['POST'])
@app.route('/booking_done/', methods=['GET', 'POST'])
# def main_booking_done(clientWeekday, clientTime, clientTeacher,
#                        clientName,  clientPhone):
def main_booking_done():
     if request.method == 'POST':
         clientWeekday = request.form['clientWeekday']
         # print(f"{clientWeekday=}")
         clientTime = request.form['clientTime']
         # print(f"{clientTime=}")
         clientTeacher = request.form['clientTeacher']
         # print(f"{clientTeacher=}")
         clientName = request.form['clientName']
         # print(f"{clientName=}")
         clientPhone = request.form['clientPhone']
         # print(f"{clientPhone=}")

     # сохраняю в booking.json
     path = pathlib.Path('booking.json')
     if path.exists():
         if path.is_file():
             with open('booking.json', 'r', encoding='utf-8') as f:
                 data_in = json.load(f)
             count = len(data_in)
         else:
             print("booking.json не является файлом")
             exit()
     else:
         print("booking.json не существует")
         # exit()
         count = 0
         data_in = {}

     data = {count + 1: [clientWeekday, clientTime,
                    clientTeacher, clientName,
                    clientPhone]
              }
     data_in.update(data)
     data_out = data_in
     with open('booking.json', 'w', encoding='utf-8') as f:
        json.dump(data_out, f, ensure_ascii=False)


     # return f'Был получен {request.method} запрос.'
     return render_template("booking_done.html", clientWeekday=clientWeekday,
                            clientTime=clientTime, clientTeacher=clientTeacher,
                            clientName=clientName, clientPhone=clientPhone)

if __name__ == '__main__':
    app.run()
"""

"""