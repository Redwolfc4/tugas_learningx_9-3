from flask import Flask,jsonify,render_template,request
from pymongo import MongoClient
from datetime import datetime
import os
from os.path import dirname, join
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DBNAME = os.environ.get("DBNAME")

mongodb_url = os.environ.get('MONGODB_URL')
client = MongoClient(mongodb_url)
db = client[DBNAME]

app=Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    articles = list(db.diary.find({}, {'_id':False}))
    return jsonify({'msg': 'Get request complete!', 'articles':articles})

@app.route("/diary", methods=["POST"])
def save_diary():
    # sample_receive = request.form.get('sample_give')
    # print(sample_receive)
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')
    
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    
    file = request.files.get('file_give')
    extension = file.filename.split('.')[-1]
    filename = f'static/images/post-{mytime}.{extension}'
    file.save(filename)
    
    profile = request.files.get('profile_give')
    extension = profile.filename.split('.')[-1]
    profilename = f'static/images/profile-{mytime}.{extension}'
    profile.save(profilename)
    
    date = '.'.join(mytime.split('-')[:3])
    
    doc = {
        'file'      : filename,
        'profile'   : profilename,
        "title"     : title_receive,
        "content"   : content_receive,
        "date"      : date
    }
    
    db.diary.insert_one(doc)
    return jsonify({'msg': 'data was saved'})
if __name__ == '__main__':
    app.run('0.0.0.0',port=5000,debug=True)