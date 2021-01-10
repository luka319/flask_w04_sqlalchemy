import json

import data

goals = data.goals
           
teachers = data.teachers

with open("goals.json", "w", encoding="utf-8") as write_file:
    json.dump(goals, write_file, ensure_ascii=False) # работает!!!


with open("teachers.json", "w", encoding="utf-8") as write_file:
    json.dump(teachers, write_file, ensure_ascii=False) # работает!!!

