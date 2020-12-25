import re
import json

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


def get_all_meals():
    with open(DATABASE_FILE) as f:
        data = json.load(f)
    return data['meals']