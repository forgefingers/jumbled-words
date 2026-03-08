from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template, request, redirect, flash
from dotenv import load_dotenv
import os
import random
load_dotenv()
uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'))
app=Flask('jumbledwords')
app.config['SECRET_KEY']='7T#3px2w/l/0'
db=client.jumbled_words
@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template('index.html')
    if request.method=='POST':
        if 'word' in request.form and len(request.form)!=0:
            words={}
            words['word']=request.form['word']
            db.words.insert_one(words)
            flash('Word added!')
            return redirect('/')
@app.route('/play', methods=['GET', 'POST'])
def play():
    shuffled=[]
    if request.method=='GET':
        wordlist=list(db.words.aggregate([{'$sample':{'size':5}}]))
        for i in wordlist:
                d={}
                shuffledword=list(i['word'])
                random.shuffle(shuffledword)
                d['word']="".join(shuffledword)
                d['id']=i['_id']
                shuffled.append(d)
        return render_template('play.html',shuffled=shuffled)
    if request.method=='POST':
            print(request.form)
            ids=[]
            words=[]
            for i, j in enumerate(request.form):
                words.append(j)
                d={"_id":ObjectId(i)}
                ids.append(d)
            correctwords=db.words.find(ids)
app.run(debug=True)