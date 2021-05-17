import json
def jsonread() :
    f = open('music.json')
    data_music = json.load(f)
    return data_music
music = jsonread()
print(music[0])

