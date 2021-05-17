from flask import Blueprint, render_template, request
import json
import requests

home = Blueprint('home', __name__)

URL_THAI_AND_DRINK = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"
URL_IMG = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/images/classify"

queryThai = {"cuisine":"Thai", "number":"4"}
queryDrink = {"type":"drink", "number":"4"}

headers = {
    'x-rapidapi-key': "d1bc2e088bmshb2a67fe1ae9c380p1341d7jsnc5af25614972",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

@home.route('/')
def index():
    response_thai = requests.request("GET", URL_THAI_AND_DRINK, headers=headers, params=queryThai).json()
    response_drink = requests.request("GET", URL_THAI_AND_DRINK, headers=headers, params=queryDrink).json()
    thai_menu = []
    drink = []
    for i in range(0, 4):
        thai_menu.append(
            {"title":response_thai['results'][i]['title'],
            "image":"https://spoonacular.com/recipeImages/{0}-240x150.jpg".format(response_thai['results'][i]['id']),
            "id":response_thai['results'][i]['id']
            })
        drink.append(
            {"title":response_drink['results'][i]['title'],
            "image":"https://spoonacular.com/recipeImages/{0}-240x150.jpg".format(response_drink['results'][i]['id']),
            "id":response_drink['results'][i]['id']
            })

    return render_template("home.html", thai_menu=thai_menu, drink=drink, margins=["150px", "100px", "50px", "30px"])