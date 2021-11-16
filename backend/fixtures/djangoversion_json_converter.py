"""
Данный файл является конвертором json-фикстур.

Конвертация производится из формата Django==2.x.x в формат Django 3.x.x
"""
import json


with open('ingredients.json', 'r', encoding='utf8') as a_file:
    json_file = a_file.read()
    ingr = json.loads(json_file)
    final_json_file = [0] * len(ingr)
    ingr_dict = {}
    for num in enumerate(ingr):
        ingr_dict = {
            'model': 'recipes.ingredient',
            'pk': num,
            'fields': {
                'name': ingr[num]['name'],
                'measurement_unit': ingr[num]['measurement_unit'],
            },
        }
        final_json_file[num] = ingr_dict

    with open('new_ingredients.json', 'w') as b_file:
        b_file.write(json.dumps(final_json_file))
