from flask import Flask
from flask import render_template, url_for, request

from . import Meal

app = Flask(__name__)

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
        return render_template('success.html')

@app.route('/prep_meals', methods=['GET', 'POST'])
def prep_meals():
    if request.method == 'GET':
        meals = Meal.get_all_meals()
        return render_template('prep_meals.html', meals=meals)
    if request.method == 'POST':
        meal_ids = [int(a) for a in request.form]
        Meal.export_meals(meal_ids)
        return render_template('success.html')