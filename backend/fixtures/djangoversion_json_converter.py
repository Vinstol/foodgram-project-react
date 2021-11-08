import json

with open('ingredients.json', 'r', encoding='utf8') as j_file:
    json_file = j_file.read()
    ingr = json.loads(json_file)
    final_json_file = [0]*len(ingr)
    ingr_dict = {}
    for i in range(0, len(ingr)):
        ingr_dict = {
            "model": "recipes.ingredient",
            "pk": i,
            "fields": {
                "name": ingr[i]['name'],
                "measurement_unit": ingr[i]['measurement_unit']
            }
        }
        final_json_file[i] = ingr_dict
    
    with open('new_ingredients.json', 'w') as f:
        f.write(json.dumps(final_json_file))    
