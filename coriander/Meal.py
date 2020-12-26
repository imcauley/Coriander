import re
import json
import todoist
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_FILE = './coriander/data/database.json'

class Meal:
    def __init__(self, form_args):
        self.ingredients = []
        for (key, value) in form_args.items():
            if key == 'meal_name':
                self.name = value
            if key == 'meal_url':
                self.url = value

            if re.match(r'ingredient_.*', key):
                if value != '':
                    self.ingredients.append(value)

    def save(self):
        with open(DATABASE_FILE) as f:
            data = json.load(f)
        new_id = len(data['meals'])
        data['meals'].append({
            'name': self.name,
            'url': self.url,
            'id': new_id
        })

        ingredients = [{'name': x, 'meal_id': new_id} for x in self.ingredients]
        data['ingredients'] += ingredients

        with open(DATABASE_FILE, 'w') as f:
            json.dump(data, f)

def export_meals(meal_ids):
    api = todoist.TodoistAPI(os.getenv('TODOIST_API'))
    api.sync()

    for project in api.state['projects']:
        if project['name'] == 'Groceries':
            meal_project = project

    for section in api.state['sections']:
        if section['name'] == 'Grocery List':
            if section['project_id'] == meal_project['id']:
                grocery_section = section

    meals = get_meals(meal_ids)
    ingredients = get_ingredients_from_meals(meal_ids)

    for meal in meals:
        current_meal_task = api.items.add(
            meal['name'], 
            project_id=meal_project['id'],
            section_id=grocery_section['id']
            )
        
        api.notes.add(current_meal_task['id'], meal['url'])
        
        for ingredient in ingredients[meal['id']]:
            _ = api.items.add(
                ingredient['name'], 
                project_id=meal_project['id'],
                section_id=grocery_section['id'],
                parent_id=current_meal_task['id']
                )


    api.commit()

def get_meals(meal_ids):
    all_meals = get_all_meals()
    meals = [m for m in all_meals if m['id'] in meal_ids]
    return meals

def get_ingredients_from_meals(meal_ids):
    ingredients = get_all_ingredients()
    ingredients_in_meals = {i:[] for i in meal_ids}

    for ingredient in ingredients:
        if ingredient['meal_id'] in meal_ids:
            ingredients_in_meals[ingredient['meal_id']].append(ingredient)

    return ingredients_in_meals

def get_all_ingredients():
    with open(DATABASE_FILE) as f:
        data = json.load(f)
    return data['ingredients']

def get_all_meals():
    with open(DATABASE_FILE) as f:
        data = json.load(f)
    return data['meals']

if __name__ == "__main__":
    export_meals([4])