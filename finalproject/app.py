from flask import Flask,jsonify,make_response,request
from flask_restx import Resource,Api
from security import authenticate, identity
from flask_jwt import JWT,jwt_required
import json


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'my-super-secret'
jwt = JWT(app, authenticate, identity)

def jsonread() :
    f = open('music.json')
    data_music = json.load(f)
    return data_music

def writejson(music_dict):
    ################เขียนข้อมูลลง json################
    music_list = jsonread()
    music_list.append(music_dict)
    open_json_file = open('music.json', 'w')
    json.dump(music_list, open_json_file, indent=4) ##สำคัญ
    return 200

def deletejson(musictitle):
    ################ลบข้อมูลจากชื่อ################
    music_list = jsonread()
    print(musictitle)
    for item in range(len(music_list['songs']['English'])):
        print(music_list['songs']['English'][item]['title'])
        if music_list['songs']['English'][item]['title'].lower() == musictitle.lower():
            music_list['songs']['English'].remove(item)
            open_json_file = open('music.json', 'w')
            json.dump(music_list, open_json_file, indent=4)
            return 200
    return 500

    
def updatejson(music_list, new_info):
    music_list = jsonread()
    if len(new_info) == 0:
        return 500
    for index, item in enumerate(music_list):
        if music_list['songs']['English'][item]['title'] == music_list.lower():
            for update_item in list(new_info.keys()): # for  เพื่อเช็ค 
                if update_item not in list(item.keys()):##เช็คว่า key ที่ส่งมามีใน json ไหม
                    return 500
            music_list[index].update(new_info)
            open_json_file = open('music.json', 'w')
            json.dump(music_list, open_json_file, indent=4)
            return 200
    return 500


class video(Resource):
    def get(self):
        music_data = jsonread() #ดึงข้อมูลมาจาก function jsonread
        title = request.args.get('title') #ดึงค่ามาจากที่เขาส่งมา title
        print(len(music_data['songs']))
        
        if title != None : #ถ้าเขาส่ง title มาให้เข้าเงื่อนไข
            listcheck = []
            for check in range(len(music_data['songs']['English'])): # loop
                if title.lower() in music_data['songs']['English'][check]['title'].lower() : #check ค่า
                    
                    addlist = {
                        'title' : music_data['songs']['English'][check]['title'],
                        'yt_url' : music_data['songs']['English'][check]['yt_url']
                    }
                    listcheck.append(addlist)
            if len(listcheck) != 0: return listcheck,200
            else : return {"message": "Not Found"},500
        else : return music_data
    
class Music(Resource):
    def get(self):
        music_data = jsonread() 
        title = request.args.get('title') 
        artist = request.args.get('artist')
        #None not in (title,artist)
        if all(v is not  None for v in [title,artist])  : 
            listcheck = []
            for check in range(len(music_data['songs']['English'])): # loop
                if title.lower() in music_data['songs']['English'][check]['title'].lower() and artist.lower() in music_data['songs']['English'][check]['artist'].lower() : #check ค่า
                    addlist = {
                        'title' : music_data['songs']['English'][check]['title'],
                        'artist' : music_data['songs']['English'][check]['artist']
                    }
                    listcheck.append(addlist)
            if len(listcheck) != 0: return listcheck,200
            else : return {"message": "Not Found"},500
        else : return {"message": "Missing parameter"},500

class lyrics(Resource):
    def get(self):
        music_data = jsonread() 
        title = request.args.get('title') 
        artist = request.args.get('artist')
        #None not in (title,artist)
        if title != None and artist == None: 
            listcheck = []
            for check in range(len(music_data['songs']['English'])): # loop
                if title.lower() in music_data['songs']['English'][check]['title'].lower() : #check ค่า
                    addlist = {
                        'title' : music_data['songs']['English'][check]['title'],
                        'artist' : music_data['songs']['English'][check]['artist'],
                        'web_url' : music_data['songs']['English'][check]['web_url']
                    }
                    listcheck.append(addlist)
            if len(listcheck) != 0: return listcheck,200
            else : return {"message": "Not Found"},500
        elif  title == None and artist != None: 
            listcheck = []
            for check in range(len(music_data['songs']['English'])): # loop
                if artist.lower() in music_data['songs']['English'][check]['artist'].lower() : #check ค่า
                    addlist = {
                        'title' : music_data['songs']['English'][check]['title'],
                        'artist' : music_data['songs']['English'][check]['artist'],
                        'web_url' : music_data['songs']['English'][check]['web_url']
                    }
                    listcheck.append(addlist)
            if len(listcheck) != 0: return listcheck,200
            else : return {"message": "Not Found"},500
        elif  title != None and artist != None: 
            listcheck = []
            for check in range(len(music_data['songs']['English'])): # loop
                if title.lower() in music_data['songs']['English'][check]['title'].lower() and artist.lower() in music_data['songs']['English'][check]['artist'].lower() : #check ค่า
                    addlist = {
                        'title' : music_data['songs']['English'][check]['title'],
                        'artist' : music_data['songs']['English'][check]['artist'],
                        'web_url' : music_data['songs']['English'][check]['web_url']
                    }
                    listcheck.append(addlist)
            if len(listcheck) != 0: return listcheck,200
            else : return {"message": "Not Found"},500
        else : return {"message": "Missing parameter"},500

class song(Resource):
    
    def delete(self,title): #รับ DELETE
        print("delete")
        status = deletejson(title)
        if status == 200:
            return {"message":"Music has been deleted."}, 200
        elif status == 500:
            return {"message":title+" not found."}, 500


    def put(self,title):#รับ PUT
        music_dict = api.payload
        status = updatejson(title, music_dict)
        if status == 200:
            return {
                "message":"Music HAS BEEN UPDATED."
                }, 200
        elif status == 500:
            return {"message": "FAIL TO UPDATED."}, 500

api.add_resource(video,'/video')
api.add_resource(Music,'/music')
api.add_resource(lyrics,'/lyrics')
api.add_resource(song,'/song/<title>')