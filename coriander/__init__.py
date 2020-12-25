from flask import Flask
from flask import render_template
from flask import request

from . import Meal

import sqlite3
app = Flask(__name__)

conn = sqlite3.connect('example.db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_meal', methods=['GET', 'POST'])
def add_meal():
    if request.method == 'GET':
        return render_template('add_meal.html')
    if request.method == 'POST':
        new_meal = Meal.Meal(request.form)
        new_meal.save()
        # print(request.form)

@app.route('/prep_meals', methods=['GET', 'POST'])
def prep_meals():
    if request.method == 'GET':
        meals = Meal.get_all_meals()
        return render_template('prep_meals.html', meals=meals)
    if request.method == 'POST':
        print(request.form)
    #     new_meal = Meal(request.form)
    #     new_meal.save()
        # print(request.form)