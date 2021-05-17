from flask import Blueprint, render_template, request
import json
import requests

search = Blueprint('search', __name__)

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"
url_ingre = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{0}/ingredientWidget"
url_info = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{0}/information"
url_equipment = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{0}/equipmentWidget"
url_instruction = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{0}/analyzedInstructions"
url_nutrition = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{0}/nutritionWidget"

queryInstructions = {"stepBreakdown":"true"}
queryVisual = {"defaultCss":"true", "showBacklink":"false"}

headers = {
    'x-rapidapi-key': "d1bc2e088bmshb2a67fe1ae9c380p1341d7jsnc5af25614972",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

visual = {
    'accept': "text/html",
    'x-rapidapi-key': "d1bc2e088bmshb2a67fe1ae9c380p1341d7jsnc5af25614972",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

@search.route('/search', methods=['GET','POST'])
def search_page():
    if request.method == 'GET':
        return render_template("search.html", results=-1, total=0)
    if request.method == 'POST':
        results = None
        if not request.form.get('type') and not request.form.get('name'):
            results = get_menu({"cuisine": request.form.get('country'), "fillIngredients":"true", "addRecipeInformation":"true"})
        elif not request.form.get('type') and not request.form.get('country'):
            results = get_menu({"query": request.form.get('name'), "fillIngredients":"true", "addRecipeInformation":"true"})
        elif not request.form.get('name') and not request.form.get('country'):
            results = get_menu({"type": request.form.get('type'), "fillIngredients":"true", "addRecipeInformation":"true"})
        elif not request.form.get('country'):
            results = get_menu({"type": request.form.get('type'), "query":request.form.get('name'), "fillIngredients":"true", "addRecipeInformation":"true"})
        elif not request.form.get('type'):
            results = get_menu({"cuisine": request.form.get('country'), "query":request.form.get('name'), "fillIngredients":"true", "addRecipeInformation":"true"})
        elif not request.form.get('name'):
            results = get_menu({"cuisine": request.form.get('country'), "type":request.form.get('type'), "fillIngredients":"true", "addRecipeInformation":"true"})
        else:
            results = get_menu({"cuisine": request.form.get('country'), "type":request.form.get('type'), "query":request.form.get('name'), "fillIngredients":"true", "addRecipeInformation":"true"})
        if results == -1:
            return render_template("search.html", results=-2, total=0)
        return render_template("search.html", results=results[1], total=results[0], height=str(100*results[0]/2))

@search.route('/search/<id>')
def info(id):
    infomation = get_info(id)
    ingredients = get_ingredients(id)
    equipments = get_equipment(id)
    nutrition = get_nutrition(id)
    return render_template("info.html", infomation=infomation, ingredients=ingredients, equipments=equipments, nutrition=nutrition)

def get_menu(query):
    response_name = requests.request("GET", url, headers=headers, params=query).json()
    total = int(response_name['number'])
    menu = []
    for i in range(0, total):
        ingredient = []
        try:
            for j in range(0, len(response_name['results'][i]['missedIngredients'])):
                ingredient.append(response_name['results'][i]['missedIngredients'][j]['name'])
        except:
            return -1
        menu.append(
            {
                "title":response_name['results'][i]['title'],
                "image":"https://spoonacular.com/recipeImages/{0}-312x231.jpg".format(response_name['results'][i]['id']),
                "like":response_name['results'][i]['aggregateLikes'],
                "health":response_name['results'][i]['healthScore'],
                "ingredients":ingredient,
                "id":response_name['results'][i]['id']
            }
        )
    results = [total, menu]
    return results

def get_info(id):
    url = url_info.format(id)
    url_instruc = url_instruction.format(id)
    response_info = requests.request("GET", url, headers=headers).json()
    response_instruc = requests.request("GET", url_instruc, headers=headers, params=queryInstructions).json()
    steps = []
    for i in response_instruc[0]['steps']:
        steps.append(i['step'])
    results = {
        "title":response_info['title'],
        "like":response_info['aggregateLikes'],
        "price":response_info['pricePerServing'],
        "time":response_info['readyInMinutes'],
        "image":response_info['image'],
        "score":response_info['spoonacularScore'],
        "detail":response_info['summary'],
        "steps":steps
    }
    return results

def get_ingredients(id):
    url_ingre_format = url_ingre.format(id)
    response = requests.request("GET", url_ingre_format, headers=visual, params=queryVisual).text
    return response

def get_equipment(id):
    url_equip_format = url_equipment.format(id)
    response = requests.request("GET", url_equip_format, headers=visual, params=queryVisual).text
    return response

def get_nutrition(id):
    url_nutrition_format = url_nutrition.format(id)
    response = requests.request("GET", url_nutrition_format, headers=visual, params=queryVisual).text
    return response