from flask import Blueprint, render_template, request
import json
import requests

video = Blueprint('video', __name__)

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/videos/search"

headers = {
    'x-rapidapi-key': "d1bc2e088bmshb2a67fe1ae9c380p1341d7jsnc5af25614972",
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

@video.route('/video/<query>')
def video_page(query):
    response = None
    video = None
    try:
        response = requests.request("GET", url, headers=headers, params={"query":query, "number":"1"}).json()
        video = response['videos'][0]['youTubeId']
    except:
        return render_template("video.html", video=-1)
    return render_template("video.html", video=video)