from flask import Blueprint, render_template, request
import json
import requests

search_wine = Blueprint('search_wine', __name__)

headers = {
    'x-rapidapi-key': "d1bc2e088bmshb2a67fe1ae9c380p1341d7jsnc5af25614972",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/wine/pairing"

@search_wine.route('/search_wine', methods=['GET','POST'])
def wine():
    if request.method == 'GET':
        return render_template("wine.html", results=-1)
    if request.method == 'POST':
        results = get_wine({"food": request.form.get('wine')})
        if results == -2:
            return render_template("wine.html", results=results)
        return render_template("wine.html", results=results)

def get_wine(query):
    response = requests.request("GET", url, headers=headers, params=query).json()
    wine = None
    try :
        wine = {
            "title":response['productMatches'][0]['title'],
            "image":response['productMatches'][0]['imageUrl'],
            "link":response['productMatches'][0]['link'],
            "price":response['productMatches'][0]['price'],
            "description":response['productMatches'][0]['description']
            }
    except:
        wine = -2

    return wine